#!/usr/bin/env python3
"""
九龙戏珠 A股选股系统
数据源: Tushare Pro HTTP API
"""
import json, time, datetime, urllib.request, random

WORK_DIR = "/root/.openclaw/workspace-finance/jlzz"
DATA_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
TOKEN = "99b9743f5413c3b2dccd837014ba26972cb2984d1306925325d69484"

WEIGHTS = {
    '时间': 0.15, '空间': 0.12, '异动': 0.10, '缺口': 0.12,
    '龙头': 0.10, '转势': 0.13, '股价': 0.08, '强度': 0.10, '热点': 0.10,
}

def api_call(api_name, params=None, fields=''):
    payload = json.dumps({
        'api_name': api_name, 'token': TOKEN,
        'params': params or {}, 'fields': fields
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://api.tushare.pro', data=payload,
        headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read().decode())
            if result.get('code') != 0:
                return None
            data = result.get('data')
            if data is None:
                return []
            # HTTP API returns list of lists
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                fields_list = result.get('fields', [])
                rows = []
                for row in data:
                    rows.append(dict(zip(fields_list, row)))
                return rows
            # Python SDK returns dict with fields/items keys
            if isinstance(data, dict):
                fields_list = data.get('fields', [])
                items_list = data.get('items', [])
                rows = []
                for row in items_list:
                    rows.append(dict(zip(fields_list, row)))
                return rows
            return []
    except:
        return None

def get_all_stocks():
    # Try to load from cache first
    cache_file = f"{WORK_DIR}/stock_list.json"
    import os
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            stocks = json.load(f)
        print(f"从缓存加载 {len(stocks)} 只股票")
        return stocks
    # Get from API
    data = api_call('stock_basic', {'list_status': 'L'},
                    'ts_code,symbol,name,industry,list_date')
    if not data: return []
    stocks = []
    for d in data:
        ts = d.get('ts_code', '')
        sym = d.get('symbol', '')
        code = f"sh{sym}" if ts.endswith('.SH') else f"sz{sym}"
        stocks.append({'ts_code': ts, 'code': code,
                      'name': d.get('name', ''),
                      'industry': str(d.get('industry', '')),
                      'list_date': str(d.get('list_date', ''))})
    # Save cache
    with open(cache_file, 'w') as f:
        json.dump(stocks, f)
    print(f"获取并缓存 {len(stocks)} 只股票")
    return stocks

def get_klines(ts_code, start='20250101', end=None):
    if not end:
        end = datetime.datetime.now().strftime('%Y%m%d')
    data = api_call('daily', {'ts_code': ts_code,
                               'start_date': start, 'end_date': end},
                    'ts_code,trade_date,open,high,low,close,pct_chg,vol')
    if not data or not data.get('items'): return None
    klines = []
    for row in zip(*[data['items'][i] for i in range(len(data['items']))]):
        d = dict(zip(data['fields'], row))
        try:
            klines.append({'date': d['trade_date'],
                           'open': float(d['open']),
                           'close': float(d['close']),
                           'high': float(d['high']),
                           'low': float(d['low']),
                           'volume': float(d['vol']),
                           'pct_chg': float(d.get('pct_chg', 0))})
        except: continue
    klines.sort(key=lambda x: x['date'])
    return klines if klines else None

def is_old(list_date):
    if not list_date: return True
    try:
        days = (datetime.datetime.now() -
                datetime.datetime.strptime(list_date, '%Y%m%d')).days
        return days >= 365
    except: return True

def ma(closes, n):
    if len(closes) < n: return None
    return sum(closes[-n:]) / n

def macd(closes, f=12, s=26):
    if len(closes) < s+5: return None, None
    def ema(p, n):
        e = p[0]; k = 2/(n+1)
        for x in p[1:]: e = x*k + e*(1-k)
        return e
    ef = ema(closes, f); es = ema(closes, s)
    dif = ef-es; dea = dif*0.8
    return dif, dea

def gap(klines):
    for i in range(1, min(len(klines), 20)):
        if klines[i]['open'] > klines[i-1]['high']:
            g = (klines[i]['open']-klines[i-1]['high'])/klines[i-1]['high']*100
            if g > 3: return 100, 'up_strong'
            if g > 1.5: return 70, 'up_medium'
            if g > 0.5: return 40, 'up_weak'
    return 0, None

def vr(klines):
    if len(klines) < 5: return 1.0
    avg = sum(klines[-5:-1][j]['volume'] for j in range(4))/4
    return klines[-1]['volume']/avg if avg > 0 else 1.0

def impulse(klines):
    if len(klines) < 3: return 0
    sc = 0
    for k in klines[-5:]:
        body = abs(k['close']-k['open'])
        if body > 0:
            u = k['high']-max(k['close'],k['open'])
            if u/body > 2 and body < (k['high']-k['low'])*0.3:
                sc += 20
    return min(sc, 100)

def position(klines, price):
    if len(klines) < 60 or price <= 0: return 50
    h = max(k['high'] for k in klines[-60:])
    l = min(k['low'] for k in klines[-60:])
    if h == l: return 50
    pos = (price-l)/(h-l)*100
    return 95 if pos<20 else 80 if pos<40 else 60 if pos<60 else 40 if pos<80 else 20

def trend(klines):
    if len(klines) < 30: return 50
    cs = [k['close'] for k in klines]
    dif, dea = macd(cs)
    if dif is None: return 50
    sc = 50
    if len(klines) >= 2:
        prev_cs = [k['close'] for k in klines[:-1]]
        prev_dif, prev_dea = macd(prev_cs)
        if prev_dif is not None:
            if dif>dea and prev_dif<=dea: sc += 30
            elif dif<dea and prev_dif>=dea: sc -= 20
    if dif > 0: sc += 15
    m5,m10,m20 = ma(cs,5),ma(cs,10),ma(cs,20)
    if m5 and m10 and m20:
        if m5>m10>m20: sc += 20
        elif m5<m10<m20: sc -= 20
    return min(max(sc,0),100)

def t_score(klines):
    if not klines: return 0
    t = klines[-1]
    r = t['close']/t['open'] if t['open']>0 else 1
    return 100 if r>=1.099 else 80 if r>=1.08 else 60 if r>=1.05 else 40 if r>=1.02 else 0

def p_score(p):
    if p<=0: return 50
    return 100 if p<5 else 90 if p<8 else 80 if p<10 else 60 if p<15 else 40 if p<30 else 20

def stren(klines):
    if not klines or len(klines)<5: return 50
    sc = 50
    if len(klines)>=4:
        p3 = (klines[-1]['close']-klines[-4]['close'])/klines[-4]['close']*100
        sc += 25 if p3>20 else 15 if p3>10 else 10 if p3>5 else 0
    v = vr(klines)
    sc += 20 if v>3 else 15 if v>2 else 10 if v>1.5 else 0
    return min(sc, 100)

def hot(klines):
    if not klines or len(klines)<3: return 50
    sc = 50
    consec = 0
    for k in reversed(klines):
        if k['close']>=k['open']*1.095: consec += 1
        else: break
    if consec>=3: return 100
    elif consec==2: return 85
    elif consec==1 and klines[-1]['close']>=klines[-1]['open']*1.095: return 70
    ld = sum(1 for k in klines[-10:] if k['close']>=k['open']*1.095)
    return max(sc, 80) if ld>=2 else max(sc, 60) if ld==1 else sc

def sector(klines):
    if not klines or len(klines)<5: return 50
    p5 = 0
    if len(klines)>=6:
        p5 = (klines[-1]['close']-klines[-6]['close'])/klines[-6]['close']*100
    return 100 if p5>=20 else 85 if p5>=15 else 70 if p5>=10 else 60 if p5>=5 else 50 if p5>=0 else 30

def analyze(stock):
    if not is_old(stock['list_date']): return None
    klines = get_klines(stock['ts_code'])
    if not klines or len(klines)<30: return None
    price = klines[-1]['close']
    if price<=0: return None
    pct = klines[-1].get('pct_chg', 0)
    is_up = pct>=9.5
    cs = [k['close'] for k in klines]
    sc = {
        '时间': t_score(klines),
        '空间': position(klines, price),
        '异动': impulse(klines),
        '缺口': gap(klines)[0],
        '龙头': sector(klines),
        '转势': trend(klines),
        '股价': p_score(price),
        '强度': stren(klines),
        '热点': hot(klines),
    }
    total = sum(sc[k]*WEIGHTS[k] for k in WEIGHTS)
    signals = []
    dif, dea = macd(cs)
    if dif is not None:
        if dif>dea: signals.append("MACD金叉")
        elif dif<dea: signals.append("MACD死叉")
        if dif>0: signals.append("MACD在0轴上方")
    m5,m10,m20 = ma(cs,5),ma(cs,10),ma(cs,20)
    if m5 and m10 and m20:
        if m5>m10>m20: signals.append("均线多头排列")
        elif m5<m10<m20: signals.append("均线空头排列")
    g,gt = gap(klines)
    if gt: signals.append(f"存在{gt}缺口")
    v = vr(klines)
    if v>2: signals.append(f"量比放大({v:.1f}x)")
    risks = []
    if price>50: risks.append("股价偏高")
    if v<0.5: risks.append("成交量萎缩")
    if not is_up: risks.append("非涨停")
    ind = stock.get('industry','')
    if ind and ind!='nan': risks.append(f"行业:{ind[:6]}")
    return {
        '股票代码': stock['code'].upper(),
        '股票名称': stock['name'],
        '行业': ind if ind and ind!='nan' else '',
        '上市满一年': True,
        '总分': round(total,1),
        '时间得分': round(sc['时间'],1),
        '空间得分': round(sc['空间'],1),
        '异动得分': round(sc['异动'],1),
        '缺口得分': round(sc['缺口'],1),
        '龙头得分': round(sc['龙头'],1),
        '转势得分': round(sc['转势'],1),
        '股价得分': round(sc['股价'],1),
        '强度得分': round(sc['强度'],1),
        '热点得分': round(sc['热点'],1),
        '核心技术信号': '; '.join(signals) if signals else '无明显信号',
        '风险提示': '; '.join(risks) if risks else '无',
        '数据日期': DATA_DATE,
        '当前价': round(price,2),
        '涨跌幅': round(pct,2),
    }

def main():
    print("="*60)
    print("九龙戏珠 A股选股系统")
    print(f"运行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    stocks = get_all_stocks()
    print(f"股票总数: {len(stocks)}")
    if not stocks: return []
    random.seed(42)
    sample = random.sample(stocks, min(300, len(stocks)))
    results = []
    dim_sum = {k: 0.0 for k in WEIGHTS}
    cnt = 0
    for stock in sample:
        if cnt%50==0: print(f"进度: {cnt}/{len(sample)} ...")
        r = analyze(stock)
        if r:
            results.append(r)
            for k in WEIGHTS:
                dim_sum[k] += r[f"{k}得分"]
        cnt += 1
        if cnt%10==0: time.sleep(0.2)
    qual = sorted(results, key=lambda x: x['总分'], reverse=True)
    filt = [r for r in qual if r['总分']>=55 or r['热点得分']>=65 or r['时间得分']>0 or '非涨停' not in r['风险提示']]
    out = f"{WORK_DIR}/jlzz_results_{DATA_DATE}.json"
    with open(out, 'w') as f:
        json.dump({'run_date': DATA_DATE, 'total': len(results),
                   'qualified': len(filt), 'results': filt[:200]}, f, ensure_ascii=False, indent=2)
    print(f"\n{'='*60}\n分析报告\n{'='*60}")
    print(f"分析: {len(results)} 只 | 符合条件: {len(filt)} 只")
    if filt:
        print(f"\nTOP 20:")
        for i,r in enumerate(filt[:20],1):
            zt = "🔥" if '非涨停' not in r['风险提示'] else "  "
            print(f"{i:2}. {zt} {r['股票代码']} {r['股票名称']:10} "
                  f"总分:{r['总分']:5.1f} 热点:{r['热点得分']:4.0f} "
                  f"强度:{r['强度得分']:4.0f} 转势:{r['转势得分']:4.0f} "
                  f"现价:{r['当前价']:6.2f} {r['涨跌幅']:+.1f}%")
        print(f"\n维度平均:")
        for k in WEIGHTS:
            n = sum(1 for r in results if r[f"{k}得分"]>0)
            if n>0: print(f"  {k}: {dim_sum[k]/n:.1f} ({WEIGHTS[k]*100:.0f}%)")
    print(f"\n结果: {out}")
    return filt

if __name__ == "__main__":
    main()
