#!/usr/bin/env python3
"""
九龙戏珠 A股选股系统 - 基于 Tushare Pro
"""

import tushare as ts
import pandas as pd
import numpy as np
import json
import time
import datetime
import requests
import re

WORK_DIR = "/root/.openclaw/workspace-finance/jlzz"
DATA_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
TUSHARE_TOKEN = "99b9743f5413c3b2dccd837014ba26972cb2984d1306925325d69484"
BITABLE_APP_TOKEN = "H4PKb6gJRa1ZccsPY3Yc42eGnTd"
BITABLE_TABLE_ID = "tblLo5ZXoU7DpkSk"

WEIGHTS = {
    '时间': 0.15, '空间': 0.12, '异动': 0.10, '缺口': 0.12,
    '龙头': 0.10, '转势': 0.13, '股价': 0.08, '强度': 0.10, '热点': 0.10,
}

# 初始化 Tushare
pro = ts.pro_api(TUSHARE_TOKEN)

def get_all_stocks():
    """获取所有A股股票列表（优先从缓存读取）"""
    import os
    cache_file = f"{WORK_DIR}/stock_list.json"
    
    # 检查缓存是否存在且不超过24小时
    if os.path.exists(cache_file):
        file_age = os.path.getmtime(cache_file)
        import time
        if time.time() - file_age < 86400:  # 24小时内
            with open(cache_file, 'r') as f:
                stocks = json.load(f)
            print(f"从缓存加载 {len(stocks)} 只股票")
            return stocks
    
    # 缓存不存在或过期，从Tushare获取
    print("从Tushare获取A股股票列表...")
    try:
        df = pro.stock_basic(exchange='', list_status='L', 
                              fields='ts_code,symbol,name,area,industry,list_date')
        stocks = []
        for _, row in df.iterrows():
            ts_code = row['ts_code']
            symbol = row['symbol']
            name = row['name']
            list_date = str(row['list_date'])
            industry = str(row.get('industry', ''))
            code = f"sh{symbol}" if ts_code.endswith('.SH') else f"sz{symbol}"
            stocks.append({'ts_code': ts_code, 'code': code, 'name': name, 'list_date': list_date, 'industry': industry})
        
        # 保存缓存
        with open(cache_file, 'w') as f:
            json.dump(stocks, f)
        print(f"获取并缓存 {len(stocks)} 只股票")
        return stocks
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return []

def get_daily_data(ts_code, start_date='20250101', end_date=None):
    """获取日线数据"""
    if end_date is None:
        end_date = datetime.datetime.now().strftime('%Y%m%d')
    try:
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if df is None or len(df) == 0:
            return None
        # 按日期排序
        df = df.sort_values('trade_date')
        klines = []
        for _, row in df.iterrows():
            klines.append({
                'date': row['trade_date'],
                'open': row['open'],
                'close': row['close'],
                'high': row['high'],
                'low': row['low'],
                'volume': row['vol'],
                'pct_chg': row['pct_chg'],
                'amount': row['amount'],
            })
        return klines
    except Exception as e:
        return None

def get_limit_up_stocks(trade_date):
    """获取涨停股列表"""
    try:
        # 尝试不同格式
        for fmt in ['%Y%m%d', '%Y-%m-%d']:
            try:
                td = datetime.datetime.strptime(trade_date, fmt).strftime('%Y%m%d')
                break
            except:
                continue
        df = pro.limit_list_d(trade_date=td)
        if df is not None and len(df) > 0:
            return df
    except:
        pass
    # fallback: 用日涨幅接近10%筛选
    try:
        today = datetime.datetime.now().strftime('%Y%m%d')
        df = pro.daily(trade_date=today)
        if df is not None:
            df = df[df['pct_chg'] >= 9.5]
            return df
    except:
        pass
    return None

def is_listed_over_one_year(list_date, ref_date=None):
    """检查股票是否上市满一年"""
    if ref_date is None:
        ref_date = datetime.datetime.now()
    if list_date is None or list_date == '':
        return True  # 无法确定时假设满一年
    try:
        list_dt = datetime.datetime.strptime(str(list_date), '%Y%m%d')
        days = (ref_date - list_dt).days
        return days >= 365
    except:
        return True

def calc_ma(closes, period):
    if len(closes) < period:
        return None
    return sum(closes[-period:]) / period

def calc_macd(closes, fast=12, slow=26):
    if len(closes) < slow + 5:
        return None, None, None
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
    return dif, dea, (dif - dea) * 2

def identify_gap(klines):
    """识别跳空缺口"""
    if len(klines) < 2:
        return 0, None
    up_gaps = []
    for i in range(1, min(len(klines), 20)):
        prev_high = klines[i-1]['high']
        curr_open = klines[i]['open']
        if curr_open > prev_high:
            gap = (curr_open - prev_high) / prev_high * 100
            up_gaps.append(gap)
    if not up_gaps:
        return 0, None
    max_gap = max(up_gaps)
    if max_gap > 3: return 100, 'up_strong'
    elif max_gap > 1.5: return 70, 'up_medium'
    elif max_gap > 0.5: return 40, 'up_weak'
    return 0, None

def vol_ratio(klines):
    """计算量比"""
    if len(klines) < 5:
        return 1.0
    avg = sum(k['volume'] for k in klines[-5:-1]) / 4
    today = klines[-1]['volume'] if klines else 1
    return today / avg if avg > 0 else 1.0

def impulse_score(klines):
    """检测试盘动作（长上影线）"""
    if len(klines) < 3:
        return 0
    score = 0
    for k in klines[-5:]:
        body = abs(k['close'] - k['open'])
        if body > 0:
            upper = k['high'] - max(k['close'], k['open'])
            ratio = upper / body
            if ratio > 2 and body < (k['high'] - k['low']) * 0.3:
                score += 20
    return min(score, 100)

def position_score(klines, price):
    """股价位置得分"""
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
    """趋势反转得分"""
    if len(klines) < 30:
        return 50
    closes = [k['close'] for k in klines]
    dif, dea, _ = calc_macd(closes)
    if dif is None:
        return 50
    score = 50
    # 金叉死叉
    if len(klines) >= 2:
        prev_closes = [k['close'] for k in klines[:-1]]
        prev_dif, prev_dea, _ = calc_macd(prev_closes)
        if prev_dif is not None:
            if dif > dea and prev_dif <= dea:
                score += 30  # 金叉
            elif dif < dea and prev_dif >= dea:
                score -= 20  # 死叉
    if dif > 0:
        score += 15
    # 均线
    ma5 = calc_ma(closes, 5)
    ma10 = calc_ma(closes, 10)
    ma20 = calc_ma(closes, 20)
    if ma5 and ma10 and ma20:
        if ma5 > ma10 > ma20:
            score += 20
        elif ma5 < ma10 < ma20:
            score -= 20
    return min(max(score, 0), 100)

def time_score(klines):
    """涨停时间得分（根据K线形态）"""
    if not klines or len(klines) < 1:
        return 0
    today = klines[-1]
    close_ratio = today['close'] / today['open'] if today['open'] > 0 else 1
    if close_ratio >= 1.099: return 100
    elif close_ratio >= 1.08: return 80
    elif close_ratio >= 1.05: return 60
    elif close_ratio >= 1.02: return 40
    return 0

def price_score(p):
    """股价得分（偏好低价股）"""
    if p <= 0: return 50
    if p < 5: return 100
    elif p < 8: return 90
    elif p < 10: return 80
    elif p < 15: return 60
    elif p < 30: return 40
    return 20

def strength_score(klines):
    """强度得分"""
    if not klines or len(klines) < 5:
        return 50
    score = 50
    # 3日涨幅
    if len(klines) >= 4:
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
    """热点得分（连续涨停）"""
    if not klines or len(klines) < 3:
        return 50
    score = 50
    # 连续涨停
    consec = 0
    for k in reversed(klines):
        if k['close'] >= k['open'] * 1.095:
            consec += 1
        else:
            break
    if consec >= 3: return 100
    elif consec == 2: return 85
    elif consec == 1 and klines[-1]['close'] >= klines[-1]['open'] * 1.095:
        return 70
    # 近期涨停天数
    limit_days = sum(1 for k in klines[-10:] if k['close'] >= k['open'] * 1.095)
    if limit_days >= 2: score = max(score, 80)
    elif limit_days == 1: score = max(score, 60)
    return min(score, 100)

def sector_score(klines):
    """龙头得分（5日涨幅）"""
    if not klines or len(klines) < 5:
        return 50
    pct5 = 0
    if len(klines) >= 6:
        pct5 = (klines[-1]['close'] - klines[-6]['close']) / klines[-6]['close'] * 100
    if pct5 >= 20: return 100
    elif pct5 >= 15: return 85
    elif pct5 >= 10: return 70
    elif pct5 >= 5: return 60
    elif pct5 >= 0: return 50
    return 30

def analyze_stock(stock_info):
    """分析单只股票"""
    ts_code = stock_info['ts_code']
    code = stock_info['code']
    name = stock_info['name']
    list_date = stock_info['list_date']
    
    # 检查是否上市满一年
    if not is_listed_over_one_year(list_date):
        return None
    
    # 获取日线数据（最近120天）
    klines = get_daily_data(ts_code, start_date='20250101')
    if not klines or len(klines) < 30:
        return None
    
    price = klines[-1]['close']
    if price <= 0:
        return None
    
    pct_today = klines[-1].get('pct_chg', 0)
    is_limit_up = pct_today >= 9.5
    
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
    closes = [k['close'] for k in klines]
    dif, dea, _ = calc_macd(closes)
    if dif is not None:
        if dif > dea: signals.append("MACD金叉")
        elif dif < dea: signals.append("MACD死叉")
        if dif > 0: signals.append("MACD在0轴上方")
    
    ma5, ma10, ma20 = calc_ma(closes, 5), calc_ma(closes, 10), calc_ma(closes, 20)
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
    if not is_limit_up: risks.append("非涨停")
    
    return {
        '股票代码': code.upper(),
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
        '涨跌幅': round(pct_today, 2),
    }

def main():
    print("=" * 60)
    print("九龙戏珠 A股选股系统 (Tushare Pro版)")
    print(f"运行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 获取所有股票
    all_stocks = get_all_stocks()
    if not all_stocks:
        print("获取股票列表失败")
        return []
    
    # 优先获取涨停股作为重点关注
    print("\n获取今日涨停股...")
    limit_df = get_limit_up_stocks(DATA_DATE.replace('-', ''))
    limit_codes = set()
    if limit_df is not None and len(limit_df) > 0:
        for _, row in limit_df.iterrows():
            ts = row['ts_code']
            symbol = ts.split('.')[0]
            if ts.endswith('.SH'):
                limit_codes.add(f"sh{symbol}")
            else:
                limit_codes.add(f"sz{symbol}")
        print(f"今日涨停股: {len(limit_codes)} 只")
    
    # 优先分析涨停股
    zt_stocks = [s for s in all_stocks if s['code'] in limit_codes]
    other_stocks = [s for s in all_stocks if s['code'] not in limit_codes]
    
    # 采样：涨停股全分析 + 其他抽样
    sample_size = min(300, len(other_stocks))
    step = max(1, len(other_stocks) // sample_size)
    sampled_other = other_stocks[::step][:sample_size]
    
    # 合并：涨停股优先
    stocks_to_analyze = zt_stocks + sampled_other
    # 去重保持顺序
    seen = set()
    unique_stocks = []
    for s in stocks_to_analyze:
        if s['code'] not in seen:
            seen.add(s['code'])
            unique_stocks.append(s)
    
    print(f"\n开始分析 {len(unique_stocks)} 只股票（涨停股: {len(zt_stocks)} 只 + 抽样: {len(unique_stocks) - len(zt_stocks)} 只）...\n")
    
    results = []
    dim_avgs = {k: [] for k in WEIGHTS}
    
    for i, stock in enumerate(unique_stocks):
        if i % 50 == 0:
            print(f"进度: {i}/{len(unique_stocks)} ... 当前: {stock['code']} {stock['name']}")
        
        result = analyze_stock(stock)
        if result:
            results.append(result)
            for dim in dim_avgs:
                key = f"{dim}得分"
                if key in result:
                    dim_avgs[dim].append(result[key])
        
        if i % 10 == 0:
            time.sleep(0.15)  # 避免API限流
    
    print(f"\n分析完成，有效数据: {len(results)} 只")
    
    # 排序
    qualified = sorted(results, key=lambda x: x['总分'], reverse=True)
    
    # 筛选：总分>=55 或 热点>=65 或 时间>0 或 涨停
    filtered = [r for r in qualified if r['总分'] >= 55 or r['热点得分'] >= 65 or r['时间得分'] > 0 or '非涨停' not in r['风险提示']]
    
    # 保存
    output_file = f"{WORK_DIR}/jlzz_results_tushare_{DATA_DATE}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'run_date': DATA_DATE,
            'total_analyzed': len(results),
            'qualified_count': len(filtered),
            'limit_up_count': len(zt_stocks),
            'results': filtered[:200],
        }, f, ensure_ascii=False, indent=2)
    
    # 报告
    print("\n" + "=" * 60)
    print("分析报告")
    print("=" * 60)
    print(f"分析股票总数: {len(results)}")
    print(f"今日涨停股数: {len(zt_stocks)}")
    print(f"符合条件股票数: {len(filtered)}")
    
    if filtered:
        print(f"\nTOP 30 股票:")
        print("-" * 100)
        for i, r in enumerate(filtered[:30], 1):
            zt_tag = "🔥" if '非涨停' not in r['风险提示'] else "  "
            print(f"{i:2}. {zt_tag} {r['股票代码']} {r['股票名称']:10} 总分:{r['总分']:5.1f} "
                  f"热点:{r['热点得分']:4.0f} 强度:{r['强度得分']:4.0f} "
                  f"转势:{r['转势得分']:4.0f} 现价:{r['当前价']:6.2f} 涨幅:{r['涨跌幅']:+.1f}%")
        
        print(f"\n各维度平均得分:")
        for dim, scores in dim_avgs.items():
            if scores:
                avg = sum(scores) / len(scores)
                print(f"  {dim:4}: {avg:5.1f} (权重: {WEIGHTS[dim]*100:.0f}%)")
        
        # 核心信号统计
        sig_count = {}
        for r in filtered:
            for sig in r['核心技术信号'].split('; '):
                if sig and sig != '无明显信号':
                    sig_count[sig] = sig_count.get(sig, 0) + 1
        if sig_count:
            print(f"\n核心技术信号TOP10:")
            for sig, cnt in sorted(sig_count.items(), key=lambda x: -x[1])[:10]:
                print(f"  {sig}: {cnt}只")
        
        # 写入飞书
        print(f"\n准备写入飞书...")
        return filtered
    else:
        print("\n没有符合条件股票")
        top10 = qualified[:10]
        for i, r in enumerate(top10, 1):
            print(f"{i:2}. {r['股票代码']} {r['股票名称']:10} 总分:{r['总分']:5.1f}")
        return []

if __name__ == "__main__":
    results = main()
    if results:
        # 保存结果供后续写入飞书使用
        import pickle
        with open(f"/tmp/jlzz_results_temp.pkl", 'wb') as f:
            pickle.dump(results, f)
        print(f"\n结果已暂存，等待写入飞书...")
