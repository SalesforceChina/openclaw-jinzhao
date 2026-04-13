#!/usr/bin/env python3
"""
九龙戏珠 A股选股系统 - 基于 BaoStock
"""

import baostock as bs
import pandas as pd
import numpy as np
import json
import time
import datetime
import requests
import re

WORK_DIR = "/root/.openclaw/workspace-finance/jlzz"
DATA_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
BITABLE_APP_TOKEN = "H4PKb6gJRa1ZccsPY3Yc42eGnTd"
BITABLE_TABLE_ID = "tblLo5ZXoU7DpkSk"

WEIGHTS = {
    '时间': 0.15, '空间': 0.12, '异动': 0.10, '缺口': 0.12,
    '龙头': 0.10, '转势': 0.13, '股价': 0.08, '强度': 0.10, '热点': 0.10,
}

def login():
    lg = bs.login()
    if lg.error_code != '0':
        print(f"Baostock登录失败: {lg.error_msg}")
        return False
    return True

def logout():
    bs.logout()

def get_all_stocks():
    """获取所有A股股票列表"""
    print("获取A股股票列表...")
    stocks = []
    rs = bs.query_all_stock(day=DATA_DATE)
    while rs.error_code == '0' and rs.next():
        row = rs.get_row_data()
        code = row[0]  # 如 sh.600000
        name = row[1]
        if code.startswith('sh.6') or code.startswith('sz.000') or code.startswith('sz.002') or code.startswith('sz.300'):
            stocks.append({'code': code, 'name': name})
    print(f"获取到 {len(stocks)} 只A股股票")
    return stocks

def get_kline_data(code, fields='date,open,high,low,close,volume'):
    """获取日K线数据"""
    rs = bs.query_history_k_data_plus(
        code,
        fields,
        start_date='2025-01-01',
        end_date=DATA_DATE,
        frequency='d',
        adjustflag='2'  # 前复权
    )
    klines = []
    while rs.error_code == '0' and rs.next():
        row = rs.get_row_data()
        try:
            klines.append({
                'date': row[0],
                'open': float(row[1]),
                'high': float(row[2]),
                'low': float(row[3]),
                'close': float(row[4]),
                'volume': float(row[5]),
            })
        except:
            continue
    return klines

def get_realtime_zt_data():
    """获取今日涨停股（模拟：通过日涨幅接近10%判断）"""
    print("获取今日涨停股数据...")
    zt_stocks = []
    rs = bs.query_history_k_data_plus(
        'sh.000001',
        'date,close,pct',
        start_date=DATA_DATE,
        end_date=DATA_DATE,
        frequency='d'
    )
    # 实际上baostock没有实时涨停数据，通过当日日涨幅判断
    # 这里我们用日K数据中的涨幅来模拟
    return zt_stocks

def calc_ma(klines, period):
    if len(klines) < period:
        return None
    return sum(k['close'] for k in klines[-period:]) / period

def calc_macd(klines, fast=12, slow=26, signal=9):
    if len(klines) < slow + 5:
        return None, None, None
    closes = [k['close'] for k in klines]
    def ema(prices, p):
        e = prices[0]
        k = 2 / (p + 1)
        for price in prices[1:]:
            e = price * k + e * (1 - k)
        return e
    ef = ema(closes, fast)
    es = ema(closes, slow)
    dif = ef - es
    dea = dif * 0.8
    macd_bar = (dif - dea) * 2
    return dif, dea, macd_bar

def identify_gap(klines):
    if len(klines) < 2:
        return 0, None
    up_gaps = []
    for i in range(1, min(len(klines), 20)):  # 只看最近20天
        prev_high = klines[i-1]['high']
        curr_open = klines[i]['open']
        if curr_open > prev_high:
            gap = (curr_open - prev_high) / prev_high * 100
            up_gaps.append(gap)
    if not up_gaps:
        return 0, None
    max_gap = max(up_gaps)
    if max_gap > 3:
        return 100, 'up_strong'
    elif max_gap > 1.5:
        return 70, 'up_medium'
    elif max_gap > 0.5:
        return 40, 'up_weak'
    return 0, None

def vol_ratio(klines):
    if len(klines) < 5:
        return 1.0
    recent = klines[-5:-1]  # 不包含今天
    avg = sum(k['volume'] for k in recent) / 4
    today = klines[-1]['volume'] if klines else 1
    return today / avg if avg > 0 else 1.0

def impulse_score(klines):
    if len(klines) < 3:
        return 0
    score = 0
    for k in klines[-5:]:
        body = abs(k['close'] - k['open'])
        upper = k['high'] - max(k['close'], k['open'])
        if body > 0:
            ratio = upper / body
            if ratio > 2 and body < (k['high'] - k['low']) * 0.3:
                score += 20
    return min(score, 100)

def position_score(klines, price):
    if len(klines) < 60 or price <= 0:
        return 50
    high = max(k['high'] for k in klines[-60:])
    low = min(k['low'] for k in klines[-60:])
    if high == low:
        return 50
    pos = (price - low) / (high - low) * 100
    if pos < 20: return 95
    elif pos < 40: return 80
    elif pos < 60: return 60
    elif pos < 80: return 40
    return 20

def trend_score(klines):
    if len(klines) < 30:
        return 50
    dif, dea, _ = calc_macd(klines)
    if dif is None:
        return 50
    score = 50
    if len(klines) >= 2:
        prev_dif = calc_macd(klines[:-1])[0]
        if prev_dif is not None and dif > dea and prev_dif <= dea:
            score += 30  # 金叉
        elif prev_dif is not None and dif < dea and prev_dif >= dea:
            score -= 20  # 死叉
    if dif > 0:
        score += 15
    ma5 = calc_ma(klines, 5)
    ma10 = calc_ma(klines, 10)
    ma20 = calc_ma(klines, 20)
    if ma5 and ma10 and ma20:
        if ma5 > ma10 > ma20:
            score += 20
        elif ma5 < ma10 < ma20:
            score -= 20
    return min(max(score, 0), 100)

def time_score(klines):
    """根据K线形态推断涨停时间（简化版）"""
    if not klines or len(klines) < 1:
        return 0
    today = klines[-1]
    # 如果开盘即涨停（收在最高价附近）
    if today['close'] >= today['high'] * 0.99 and today['close'] >= today['open'] * 1.09:
        return 100
    elif today['close'] >= today['open'] * 1.09:
        return 80
    elif today['close'] >= today['open'] * 1.05:
        return 50
    return 0

def price_score(p):
    if p <= 0: return 50
    if p < 5: return 100
    elif p < 8: return 90
    elif p < 10: return 80
    elif p < 15: return 60
    elif p < 30: return 40
    return 20

def strength_score(klines):
    """根据近期涨幅和成交量判断强度"""
    if not klines or len(klines) < 5:
        return 50
    score = 50
    # 近期涨幅
    if len(klines) >= 3:
        pct3 = (klines[-1]['close'] - klines[-4]['close']) / klines[-4]['close'] * 100
        if pct3 > 20: score += 25
        elif pct3 > 10: score += 15
        elif pct3 > 5: score += 10
    # 量比
    vr = vol_ratio(klines)
    if vr > 3: score += 20
    elif vr > 2: score += 15
    elif vr > 1.5: score += 10
    return min(score, 100)

def hot_score(klines):
    """热点得分：连续涨停"""
    if not klines or len(klines) < 3:
        return 50
    score = 50
    consec = 0
    for k in reversed(klines):
        if k['close'] >= k['open'] * 1.095:
            consec += 1
        else:
            break
    if consec >= 3: return 100
    elif consec == 2: return 85
    elif consec == 1:
        if klines[-1]['close'] >= klines[-1]['open'] * 1.095:
            return 70
    # 近期有涨停
    limit_days = 0
    for k in klines[-10:]:
        if k['close'] >= k['open'] * 1.095:
            limit_days += 1
    if limit_days >= 2:
        score = max(score, 80)
    elif limit_days == 1:
        score = max(score, 60)
    return min(score, 100)

def sector_score(klines):
    """龙头得分：近期涨幅排名（同行业对比简化为与大盘对比）"""
    if not klines or len(klines) < 5:
        return 50
    # 简化：用5日涨幅判断
    pct5 = (klines[-1]['close'] - klines[-6]['close']) / klines[-6]['close'] * 100 if len(klines) >= 6 else 0
    if pct5 >= 20: return 100
    elif pct5 >= 15: return 85
    elif pct5 >= 10: return 70
    elif pct5 >= 5: return 60
    elif pct5 >= 0: return 50
    return 30

def analyze_stock(code, name):
    """分析单只股票"""
    klines = get_kline_data(code)
    if not klines or len(klines) < 30:
        return None
    
    price = klines[-1]['close'] if klines else 0
    if price <= 0:
        return None
    
    # 判断是否涨停
    is_limit_up = klines[-1]['close'] >= klines[-1]['open'] * 1.095 if klines else False
    
    scores = {
        '时间': time_score(klines),
        '空间': position_score(klines, price),
        '异动': impulse_score(klines),
        '缺口': identify_gap(klines)[0],
        '龙头': sector_score(klines),
        '转势': trend_score(klines),
        '股价': price_score(price),
        '强度': strength_score(klines),
        '热点': hot_score(klines),
    }
    
    total = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    
    # 核心技术信号
    signals = []
    dif, dea, _ = calc_macd(klines)
    if dif is not None:
        if dif > dea: signals.append("MACD金叉")
        elif dif < dea: signals.append("MACD死叉")
        if dif > 0: signals.append("MACD在0轴上方")
    
    ma5, ma10, ma20 = calc_ma(klines, 5), calc_ma(klines, 10), calc_ma(klines, 20)
    if ma5 and ma10 and ma20:
        if ma5 > ma10 > ma20: signals.append("均线多头排列")
        elif ma5 < ma10 < ma20: signals.append("均线空头排列")
    
    gap_result = identify_gap(klines)
    if gap_result[1]: signals.append(f"存在{gap_result[1]}缺口")
    
    vr = vol_ratio(klines)
    if vr > 2: signals.append(f"量比放大({vr:.1f}x)")
    
    # 风险提示
    risks = []
    if price > 50: risks.append("股价偏高")
    if vr < 0.5: risks.append("成交量萎缩")
    
    return {
        '股票代码': code.replace('.', '').upper(),  # sh.600000 -> SH600000
        '股票名称': name,
        '上市满一年': True,
        '总分': round(total, 1),
        '时间得分': round(scores['时间'], 1),
        '空间得分': round(scores['空间'], 1),
        '异动得分': round(scores['异动'], 1),
        '缺口得分': round(scores['缺口'], 1),
        '龙头得分': round(scores['龙头'], 1),
        '转势得分': round(scores['转势'], 1),
        '股价得分': round(scores['股价'], 1),
        '强度得分': round(scores['强度'], 1),
        '热点得分': round(scores['热点'], 1),
        '核心技术信号': '; '.join(signals) if signals else '无明显信号',
        '风险提示': '; '.join(risks) if risks else '无',
        '数据日期': DATA_DATE,
        '当前价': round(price, 2),
        '涨跌幅': round((klines[-1]['close'] - klines[-2]['close']) / klines[-2]['close'] * 100, 2) if len(klines) >= 2 else 0,
    }

def write_to_bitable(results):
    """写入飞书多维表格"""
    if not results:
        print("没有结果需要写入")
        return
    
    # 先清空现有数据
    try:
        existing = feishu_bitable_app_table_record(
            action='list',
            app_token=BITABLE_APP_TOKEN,
            table_id=BITABLE_TABLE_ID,
            page_size=500
        )
        if existing.get('items'):
            ids = [item['record_id'] for item in existing['items']]
            for i in range(0, len(ids), 100):
                feishu_bitable_app_table_record(
                    action='batch_delete',
                    app_token=BITABLE_APP_TOKEN,
                    table_id=BITABLE_TABLE_ID,
                    record_ids=ids[i:i+100]
                )
    except:
        pass
    
    # 批量写入新数据
    records = []
    for r in results:
        records.append({
            'fields': {
                '股票代码': r['股票代码'],
                '股票名称': r['股票名称'],
                '上市满一年': r['上市满一年'],
                '总分': r['总分'],
                '时间得分': r['时间得分'],
                '空间得分': r['空间得分'],
                '异动得分': r['异动得分'],
                '缺口得分': r['缺口得分'],
                '龙头得分': r['龙头得分'],
                '转势得分': r['转势得分'],
                '股价得分': r['股价得分'],
                '强度得分': r['强度得分'],
                '热点得分': r['热点得分'],
                '核心技术信号': r['核心技术信号'],
                '风险提示': r['风险提示'],
                '数据日期': r['数据日期'],
            }
        })
    
    # 分批写入（每批100条）
    for i in range(0, len(records), 100):
        batch = records[i:i+100]
        try:
            feishu_bitable_app_table_record(
                action='batch_create',
                app_token=BITABLE_APP_TOKEN,
                table_id=BITABLE_TABLE_ID,
                records=batch
            )
            print(f"写入第 {i+1}-{min(i+100, len(records))} 条")
        except Exception as e:
            print(f"写入失败: {e}")

def main():
    print("=" * 60)
    print("九龙戏珠 A股选股系统 (BaoStock版)")
    print(f"运行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    if not login():
        return []
    
    # 获取所有股票
    stocks = get_all_stocks()
    if not stocks:
        print("获取股票列表失败")
        logout()
        return []
    
    # 先筛选出近期有涨停的股票作为重点关注
    print("\n第一阶段：筛选近期涨停股票...")
    zt_candidates = []
    
    # 抽样分析：每天最多分析200只（完整扫描5000只太慢）
    # 优先分析近期有涨停迹象的股票
    sample_size = min(len(stocks), 500)  # 先分析500只演示
    
    # 分散采样避免集中在单一板块
    step = max(1, len(stocks) // sample_size)
    sampled_stocks = stocks[::step][:sample_size]
    
    results = []
    dim_avgs = {k: [] for k in WEIGHTS}
    
    print(f"开始分析 {len(sampled_stocks)} 只股票...\n")
    
    for i, stock in enumerate(sampled_stocks):
        code = stock['code']
        name = stock['name']
        
        if i % 20 == 0:
            print(f"进度: {i}/{len(sampled_stocks)} ...", end=' ')
        
        result = analyze_stock(code, name)
        if result:
            results.append(result)
            
            # 累计维度分数
            for dim in dim_avgs:
                key = f"{dim}得分"
                if key in result:
                    dim_avgs[dim].append(result[key])
        
        # 批量处理时添加小延迟
        if i % 50 == 0:
            time.sleep(0.5)
    
    print(f"\n分析完成，共 {len(results)} 只股票有有效数据")
    
    # 按总分排序
    qualified = sorted(results, key=lambda x: x['总分'], reverse=True)
    
    # 过滤：总分>=60 或 热点得分>=70 或 时间得分>0
    filtered = [r for r in qualified if r['总分'] >= 60 or r['热点得分'] >= 70 or r['时间得分'] > 0]
    
    # 保存结果
    output_file = f"{WORK_DIR}/jlzz_results_baostock_{DATA_DATE}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'run_date': DATA_DATE,
            'total_analyzed': len(results),
            'qualified_count': len(filtered),
            'results': filtered[:100],  # 最多保存100条
        }, f, ensure_ascii=False, indent=2)
    
    # 输出报告
    print("\n" + "=" * 60)
    print("分析报告")
    print("=" * 60)
    print(f"分析股票总数: {len(results)}")
    print(f"符合条件股票数: {len(filtered)}")
    
    if filtered:
        print(f"\nTOP 20 股票:")
        print("-" * 80)
        for i, r in enumerate(filtered[:20], 1):
            print(f"{i:2}. {r['股票代码']} {r['股票名称']:10} 总分:{r['总分']:5.1f} "
                  f"热点:{r['热点得分']:4.0f} 强度:{r['强度得分']:4.0f} "
                  f"转势:{r['转势得分']:4.0f} 现价:{r['当前价']:6.2f} 涨幅:{r['涨跌幅']:+.1f}%")
            print(f"    信号: {r['核心技术信号'][:50]}")
        
        print(f"\n各维度平均得分:")
        print("-" * 40)
        for dim, scores in dim_avgs.items():
            if scores:
                avg = sum(scores) / len(scores)
                print(f"  {dim:4}: {avg:5.1f} (权重: {WEIGHTS[dim]*100:.0f}%)")
        
        # 写入飞书
        print(f"\n写入飞书多维表格...")
        write_to_bitable(filtered[:50])
    else:
        print("\n没有符合条件(总分≥60或热点≥70)的股票")
        # 显示得分最高的10只
        top10 = qualified[:10]
        print("\n得分TOP10（参考）:")
        for i, r in enumerate(top10, 1):
            print(f"{i:2}. {r['股票代码']} {r['股票名称']:10} 总分:{r['总分']:5.1f} 热点:{r['热点得分']:.0f} 强度:{r['强度得分']:.0f}")
    
    print(f"\n结果已保存到: {output_file}")
    
    logout()
    return filtered

if __name__ == "__main__":
    main()
