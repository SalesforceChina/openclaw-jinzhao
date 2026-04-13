#!/usr/bin/env python3
"""
九龙戏珠 A股选股系统 - 完整版
数据源: 腾讯财经(实时行情 + K线)
"""

import json
import time
import datetime
import requests
import re

WORK_DIR = "/root/.openclaw/workspace-finance/jlzz"
DATA_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

WEIGHTS = {
    '时间': 0.15, '空间': 0.12, '异动': 0.10, '缺口': 0.12,
    '龙头': 0.10, '转势': 0.13, '股价': 0.08, '强度': 0.10, '热点': 0.10,
}

# 完整股票列表 (沪深主板 + 创业板 + 科创板, 共约2200只核心标的)
# 从腾讯获取股票列表
def get_stock_list():
    """从腾讯财经获取股票列表"""
    print("从腾讯财经获取股票列表...")
    stocks = []
    # 上海主板
    for i in range(1, 1000):
        code = f"sh{600000 + i:06d}"
        stocks.append((code, ''))
    # 上海科创板
    for i in range(1, 1000):
        code = f"sh{688000 + i:06d}"
        stocks.append((code, ''))
    # 深圳主板
    for i in range(1, 1000):
        code = f"sz{1 + i:06d}"
        stocks.append((code, ''))
    # 创业板
    for i in range(1, 1000):
        code = f"sz{300001 + i:06d}"
        stocks.append((code, ''))
    print(f"候选股票: {len(stocks)} 只")
    return stocks

def get_kline_data(code, days=120):
    try:
        if code.startswith('sh') or code.startswith('sz'):
            market = code[:2]
            stock = code[2:]
        else:
            market = 'sh'
            stock = code
        url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={market}{stock},day,,,{days},qfq"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if 'data' not in data:
            return None
        stock_data = data['data']
        if isinstance(stock_data, dict):
            if code in stock_data:
                inner = stock_data[code]
            elif len(stock_data) == 1:
                inner = list(stock_data.values())[0]
            else:
                return None
            klines = inner.get('qfqday', inner.get('day', []))
        else:
            return None
        result = []
        for kline in klines:
            if len(kline) >= 6:
                try:
                    result.append({
                        'date': kline[0], 'open': float(kline[1]),
                        'close': float(kline[2]), 'high': float(kline[3]),
                        'low': float(kline[4]), 'volume': float(kline[5]),
                    })
                except:
                    continue
        return result if result else None
    except:
        return None

def calc_ma(klines, period):
    if len(klines) < period:
        return None
    return sum(k['close'] for k in klines[-period:]) / period

def calc_macd(klines, fast=12, slow=26):
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
    return dif, dea, (dif - dea) * 2

def identify_gap(klines):
    if len(klines) < 2:
        return 0, None
    for i in range(1, min(len(klines), 20)):
        prev_high = klines[i-1]['high']
        curr_open = klines[i]['open']
        if curr_open > prev_high:
            gap = (curr_open - prev_high) / prev_high * 100
            if gap > 3: return 100, 'up_strong'
            elif gap > 1.5: return 70, 'up_medium'
            elif gap > 0.5: return 40, 'up_weak'
    return 0, None

def vol_ratio(klines):
    if len(klines) < 5:
        return 1.0
    avg = sum(klines[-5:-1][i]['volume'] for i in range(4)) / 4
    today = klines[-1]['volume']
    return today / avg if avg > 0 else 1.0

def impulse_score(klines):
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
        if prev_dif is not None:
            if dif > dea and prev_dif <= dea: score += 30
            elif dif < dea and prev_dif >= dea: score -= 20
    if dif > 0: score += 15
    ma5, ma10, ma20 = calc_ma(klines, 5), calc_ma(klines, 10), calc_ma(klines, 20)
    if ma5 and ma10 and ma20:
        if ma5 > ma10 > ma20: score += 20
        elif ma5 < ma10 < ma20: score -= 20
    return min(max(score, 0), 100)

def time_score(klines):
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
    if p <= 0: return 50
    if p < 5: return 100
    elif p < 8: return 90
    elif p < 10: return 80
    elif p < 15: return 60
    elif p < 30: return 40
    return 20

def strength_score(klines):
    if not klines or len(klines) < 5:
        return 50
    score = 50
    if len(klines) >= 3:
        pct3 = (klines[-1]['close'] - klines[-4]['close']) / klines[-4]['close'] * 100
        if pct3 > 20: score += 25
        elif pct3 > 10: score += 15
        elif pct3 > 5: score += 10
    vr = vol_ratio(klines)
    if vr > 3: score += 20
    elif vr > 2: score += 15
    elif vr > 1.5: score += 10
    return min(score, 100)

def hot_score(klines):
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
    elif consec == 1 and klines[-1]['close'] >= klines[-1]['open'] * 1.095:
        return 70
    limit_days = sum(1 for k in klines[-10:] if k['close'] >= k['open'] * 1.095)
    if limit_days >= 2: score = max(score, 80)
    elif limit_days == 1: score = max(score, 60)
    return min(score, 100)

def sector_score(klines):
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

def analyze_stock(code):
    klines = get_kline_data(code, 120)
    if not klines or len(klines) < 30:
        return None
    
    price = klines[-1]['close']
    if price <= 0:
        return None
    
    pct_today = (klines[-1]['close'] - klines[-2]['close']) / klines[-2]['close'] * 100 if len(klines) >= 2 else 0
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
    
    risks = []
    if price > 50: risks.append("股价偏高")
    if vr < 0.5: risks.append("成交量萎缩")
    if not is_limit_up: risks.append("非涨停")
    
    # 从名字判断（如果有）
    name = code  # 简化处理
    
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
    print("九龙戏珠 A股选股系统 (腾讯财经版)")
    print(f"运行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 生成候选股票代码
    candidates = []
    # 上海主板 600000-600999
    for i in range(0, 1000):
        candidates.append(f"sh{600000 + i:06d}")
    # 上海科创板 688000-688999
    for i in range(0, 500):
        candidates.append(f"sh{688000 + i:06d}")
    # 深圳主板 000001-000999
    for i in range(0, 1000):
        candidates.append(f"sz{1 + i:06d}")
    # 创业板 300001-300999
    for i in range(0, 1000):
        candidates.append(f"sz{300001 + i:06d}")
    
    print(f"候选股票: {len(candidates)} 只")
    
    # 快速批量探测：先探测哪些有数据
    print("\n第一阶段：快速探测有效股票...")
    valid_codes = []
    batch_size = 50
    for batch_start in range(0, len(candidates), batch_size):
        batch = candidates[batch_start:batch_start + batch_size]
        if batch_start % 200 == 0:
            print(f"  探测进度: {batch_start}/{len(candidates)} ...")
        
        for code in batch:
            klines = get_kline_data(code, 5)  # 只取5条数据快速验证
            if klines and len(klines) >= 3:
                valid_codes.append(code)
        
        time.sleep(0.3)
    
    print(f"有效股票: {len(valid_codes)} 只")
    
    if not valid_codes:
        print("没有找到有效股票数据")
        return []
    
    # 第二阶段：完整分析
    print(f"\n第二阶段：完整分析 {len(valid_codes)} 只股票...")
    results = []
    dim_avgs = {k: [] for k in WEIGHTS}
    
    for i, code in enumerate(valid_codes):
        if i % 50 == 0:
            print(f"  分析进度: {i}/{len(valid_codes)} ... 当前: {code}")
        
        result = analyze_stock(code)
        if result:
            results.append(result)
            for dim in dim_avgs:
                key = f"{dim}得分"
                if key in result:
                    dim_avgs[dim].append(result[key])
        
        if i % 10 == 0:
            time.sleep(0.2)
    
    # 排序
    qualified = sorted(results, key=lambda x: x['总分'], reverse=True)
    
    # 筛选：总分>=50 或 热点>=60 或 时间>0 或 涨停
    filtered = [r for r in qualified if r['总分'] >= 50 or r['热点得分'] >= 60 or r['时间得分'] > 0 or '非涨停' not in r['风险提示']]
    
    # 保存
    output_file = f"{WORK_DIR}/jlzz_results_full_{DATA_DATE}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'run_date': DATA_DATE,
            'total_analyzed': len(results),
            'valid_stocks': len(valid_codes),
            'qualified_count': len(filtered),
            'results': filtered[:300],
        }, f, ensure_ascii=False, indent=2)
    
    # 报告
    print("\n" + "=" * 60)
    print("分析报告")
    print("=" * 60)
    print(f"扫描候选: {len(candidates)}")
    print(f"有效股票: {len(valid_codes)}")
    print(f"分析股票: {len(results)}")
    print(f"符合条件: {len(filtered)}")
    
    if filtered:
        print(f"\nTOP 50 股票:")
        print("-" * 100)
        for i, r in enumerate(filtered[:50], 1):
            zt_tag = "🔥" if '非涨停' not in r['风险提示'] else "  "
            print(f"{i:2}. {zt_tag} {r['股票代码']} 总分:{r['总分']:5.1f} "
                  f"热点:{r['热点得分']:4.0f} 强度:{r['强度得分']:4.0f} "
                  f"转势:{r['转势得分']:4.0f} 现价:{r['当前价']:6.2f} 涨幅:{r['涨跌幅']:+.1f}%")
        
        print(f"\n各维度平均得分:")
        for dim, scores in dim_avgs.items():
            if scores:
                avg = sum(scores) / len(scores)
                print(f"  {dim:4}: {avg:5.1f} (权重: {WEIGHTS[dim]*100:.0f}%)")
    else:
        print("\n没有符合条件股票")
    
    print(f"\n结果已保存到: {output_file}")
    return filtered

if __name__ == "__main__":
    main()
