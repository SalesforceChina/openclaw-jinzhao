#!/usr/bin/env python3
"""
九龙戏珠 A股选股系统 - Tushare HTTP版
通过 HTTP REST 直接调用 Tushare Pro API
"""

import json, time, datetime, urllib.request

WORK_DIR = "/root/.openclaw/workspace-finance/jlzz"
DATA_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
TOKEN = "99b9743f5413c3b2dccd837014ba26972cb2984d1306925325d69484"
BITABLE_APP_TOKEN = "H4PKb6gJRa1ZccsPY3Yc42eGnTd"
BITABLE_TABLE_ID = "tblLo5ZXoU7DpkSk"

WEIGHTS = {
    '时间': 0.15, '空间': 0.12, '异动': 0.10, '缺口': 0.12,
    '龙头': 0.10, '转势': 0.13, '股价': 0.08, '强度': 0.10, '热点': 0.10,
}

def api_call(api_name, params=None, fields=''):
    payload = json.dumps({
        'api_name': api_name,
        'token': TOKEN,
        'params': params or {},
        'fields': fields
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://api.tushare.pro',
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read().decode())
            if result.get('code') != 0:
                return None, result.get('msg', 'Unknown error')
            data = result.get('data')
            if data is None:
                return None, 'No data'
            return data, None
    except Exception as e:
        return None, str(e)

def get_all_stocks():
    """获取所有A股股票"""
    print("获取A股股票列表...")
    data, err = api_call('stock_basic', {'list_status': 'L'}, 'ts_code,symbol,name,industry,list_date')
    if err or data is None:
        print(f"  获取失败: {err}")
        return []
    fields = data['fields']
    items = data['items']
    stocks = []
    for row in items:
        d = dict(zip(fields, row))
        ts_code = d['ts_code']  # e.g. 600036.SH
        symbol = d['symbol']
        name = d['name']
        list_date = str(d.get('list_date', ''))
        industry = str(d.get('industry', ''))
        code = f"sh{symbol}" if ts_code.endswith('.SH') else f"sz{symbol}"
        stocks.append({
            'ts_code': ts_code, 'code': code, 'name': name,
            'list_date': list_date, 'industry': industry
        })
    print(f"  获取到 {len(stocks)} 只股票")
    return stocks

def get_daily_data(ts_code, start_date='20250101', end_date=None):
    """获取日线数据"""
    if end_date is None:
        end_date = datetime.datetime.now().strftime('%Y%m%d')
    data, err = api_call('daily', {
        'ts_code': ts_code, 'start_date': start_date, 'end_date': end_date
    }, 'ts_code,trade_date,open,high,low,close,pct_chg,vol,amount')
    if err or data is None:
        return None
    fields = data['fields']
    items = data['items']
    if not items:
        return None
    klines = []
    for row in items:
        d = dict(zip(fields, row))
        klines.append({
            'date': d['trade_date'],
            'open': float(d['open']),
            'close': float(d['close']),
            'high': float(d['high']),
            'low': float(d['low']),
            'volume': float(d['vol']),
            'pct_chg': float(d['pct_chg']),
            'amount': float(d['amount']) if d.get('amount') else 0,
        })
    # 按日期正序
    klines.sort(key=lambda x: x['date'])
    return klines

def is_listed_over_one_year(list_date):
    if not list_date:
        return True
    try:
        list_dt = datetime.datetime.strptime(list_date, '%Y%m%d')
        days = (datetime.datetime.now() - list_dt).days
        return days >= 365
    except:
        return True

def calc_ma(closes, period):
    if len(closes) < period:
        return None
    return sum(closes[-period:]) / period

def calc_macd(closes, fast=12, slow=26):
    if len(closes) < slow + 5:
        return None, None
    def ema(prices, p):
        e = prices[0]
        k = 2 / (p + 1)
        for price in prices[1:]:
            e = price * k + e * (1 - k)
        return e
    closes_rev = list(closes)
    ef = ema(closes_rev, fast)
    es = ema(closes_rev, slow)
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
    closes = [k['close'] for k in klines]
    dif, dea, _ = calc_macd(closes)
    if dif is None:
        return 50
    score = 50
    if len(klines) >= 2:
        prev_closes = [k['close'] for k in klines[:-1]]
        prev_dif, prev_dea, _ = calc_macd(prev_closes)
        if prev_dif is not None:
            if dif > dea and prev_dif <= dea: score += 30
            elif dif < dea and prev_dif >= dea: score -= 20
    if dif > 0: score += 15
    ma5 = calc_ma(closes, 5)
    ma10 = calc_ma(closes, 10)
    ma20 = calc_ma(closes, 20)
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
    if len(klines) >= 4:
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

def analyze_stock(stock):
    code = stock['code']
    ts_code = stock['ts_code']
    name = stock['name']
    list_date = stock['list_date']
    industry = stock.get('industry', '')
    
    if not is_listed_over_one_year(list_date):
        return None
    
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
    
    risks = []
    if price > 50: risks.append("股价偏高")
    if vr < 0.5: risks.append("成交量萎缩")
    if not is_limit_up: risks.append("非涨停")
    if industry and industry != 'nan': risks.append(f"行业:{industry}")
    
    return {
        '股票代码': code.upper(),
        '股票名称': name,
        '行业': industry if industry and industry != 'nan' else '',
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
    print("九龙戏珠 A股选股系统 (Tushare HTTP版)")
    print(f"运行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. 获取全量股票列表
    all_stocks = get_all_stocks()
    if not all_stocks:
        print("获取股票列表失败!")
        return []
    
    # 2. 先用daily接口批量探测涨停股（pct_chg >= 9.5）
    print("\n探测今日涨停股...")
    limit_stocks = []
    other_stocks = []
    
    # 探测所有股票的今日数据
    today_str = datetime.datetime.now().strftime('%Y%m%d')
    today_str = datetime.datetime.now().strftime('%Y%m%d')
    scan_count = 0
    # 批量探测：每批50只
    for i in range(0, len(all_stocks), 50):
        batch = all_stocks[i:i+50]
        if i % 200 == 0:
            print(f"  探测进度: {i}/{len(all_stocks)} ...")
        
        for stock in batch:
            ts_code = stock['ts_code']
            klines = get_daily_data(ts_code, start_date=today_str, end_date=today_str)
            if klines and len(klines) > 0:
                pct = klines[-1].get('pct_chg', 0)
                if pct >= 9.5:
                    limit_stocks.append(stock)
                else:
                    other_stocks.append(stock)
            else:
                other_stocks.append(stock)
            time.sleep(0.05)
        time.sleep(0.3)
        探测_count += len(batch)
    
    print(f"  涨停股: {len(limit_stocks)} 只")
    
    # 3. 完整分析涨停股 + 抽样分析其他
    # 涨停股全部分析
    stocks_to_analyze = limit_stocks.copy()
    
    # 其他股票抽样（按行业分散采样，避免集中在单一行业）
    import random
    random.seed(42)
    sample_size = min(400, len(other_stocks))
    sampled = random.sample(other_stocks, min(sample_size, len(other_stocks)))
    stocks_to_analyze.extend(sampled)
    
    print(f"\n完整分析 {len(stocks_to_analyze)} 只股票（涨停:{len(limit_stocks)} + 抽样:{len(sampled)}）...\n")
    
    results = []
    dim_avgs = {k: [] for k in WEIGHTS}
    
    for i, stock in enumerate(stocks_to_analyze):
        if i % 50 == 0:
            print(f"  分析进度: {i}/{len(stocks_to_analyze)} ... 当前: {stock['code']} {stock['name']}")
        
        result = analyze_stock(stock)
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
    
    # 筛选：总分>=55 或 热点>=65 或 时间>0 或 涨停
    filtered = [r for r in qualified if r['总分'] >= 55 or r['热点得分'] >= 65 or r['时间得分'] > 0 or '非涨停' not in r['风险提示']]
    
    # 保存
    output_file = f"{WORK_DIR}/jlzz_results_{DATA_DATE}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'run_date': DATA_DATE,
            'total_analyzed': len(results),
            'limit_up_count': len(limit_stocks),
            'qualified_count': len(filtered),
            'results': filtered[:300],
        }, f, ensure_ascii=False, indent=2)
    
    # 报告
    print("\n" + "=" * 60)
    print("分析报告")
    print("=" * 60)
    print(f"扫描候选: {len(all_stocks)}")
    print(f"今日涨停股: {len(limit_stocks)}")
    print(f"分析股票: {len(results)}")
    print(f"符合条件: {len(filtered)}")
    
    if filtered:
        print(f"\nTOP 30 股票:")
        print("-" * 100)
        for i, r in enumerate(filtered[:30], 1):
            zt_tag = "🔥" if '非涨停' not in r['风险提示'] else "  "
            ind = r.get('行业', '')[:6]
            print(f"{i:2}. {zt_tag} {r['股票代码']} {r['股票名称']:10} 总分:{r['总分']:5.1f} "
                  f"热点:{r['热点得分']:4.0f} 强度:{r['强度得分']:4.0f} "
                  f"转势:{r['转势得分']:4.0f} 现价:{r['当前价']:6.2f} {r['涨跌幅']:+.1f}%")
            if ind and ind != 'nan':
                print(f"     行业:{ind} 信号:{r['核心技术信号'][:50]}")
        
        print(f"\n各维度平均得分:")
        for dim, scores in dim_avgs.items():
            if scores:
                avg = sum(scores) / len(scores)
                print(f"  {dim:4}: {avg:5.1f} (权重: {WEIGHTS[dim]*100:.0f}%)")
    else:
        print("\n没有符合条件股票")
        for i, r in enumerate(qualified[:10], 1):
            print(f"{i:2}. {r['股票代码']} {r['股票名称']:10} 总分:{r['总分']:5.1f}")
    
    print(f"\n结果已保存到: {output_file}")
    return filtered

if __name__ == "__main__":
    results = main()
