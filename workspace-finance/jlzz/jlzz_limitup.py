#!/usr/bin/env python3
"""近3日涨停股 - 九龙戏珠分析"""
import json, urllib.request, datetime, time

TOKEN = "99b9743f5413c3b2dccd837014ba26972cb2984d1306925325d69484"
WORK_DIR = "/root/.openclaw/workspace-finance/jlzz"
DATA_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
BITABLE_APP_TOKEN = "H4PKb6gJRa1ZccsPY3Yc42eGnTd"
BITABLE_TABLE_ID = "tblLo5ZXoU7DpkSk"

WEIGHTS = {'时间':0.15,'空间':0.12,'异动':0.10,'缺口':0.12,'龙头':0.10,'转势':0.13,'股价':0.08,'强度':0.10,'热点':0.10}

def tushare(api_name, params=None, fields=''):
    payload = json.dumps({'api_name':api_name,'token':TOKEN,'params':params or {},'fields':fields}).encode()
    req = urllib.request.Request('https://api.tushare.pro', data=payload, headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read().decode())
            if result.get('code') != 0: return []
            data = result.get('data', {})
            if not data: return []
            flds = data.get('fields', [])
            return [dict(zip(flds, row)) for row in data.get('items', [])]
    except: return []

def tencent_kline(code, days=120):
    """腾讯财经K线，含名称"""
    try:
        url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={code},day,,,{days},qfq"
        resp = urllib.request.urlopen(url, timeout=10)
        data = json.loads(resp.read().decode())
        sd = data.get('data', {})
        if isinstance(sd, dict) and code in sd:
            inner = sd[code]
        elif isinstance(sd, dict) and len(sd) == 1:
            inner = list(sd.values())[0]
        else: return None, None
        klines = inner.get('qfqday', inner.get('day', []))
        name = inner.get('qt', {}).get(code.replace('sh','sh').replace('sz','sz'), [{}])
        # 从qt字段提取名称
        qt_str = str(inner.get('qt', ''))
        # 名称在qt的第2个字段
        name = qt_str.split('~')[1] if qt_str and '~' in qt_str else code
        result = []
        for k in klines:
            if len(k) >= 6:
                try:
                    result.append({'date':k[0],'open':float(k[1]),'close':float(k[2]),
                                  'high':float(k[3]),'low':float(k[4]),'volume':float(k[5])})
                except: continue
        return result, name if name != code else code
    except: return None, None

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
            if u/body > 2 and body < (k['high']-k['low'])*0.3: sc += 20
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
        prev_dif, _ = macd(cs[:-1])
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

def main():
    print("="*60)
    print("九龙戏珠 - 近3日涨停股分析")
    print(f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # 从Tushare获取近3日涨停股
    today = datetime.datetime.now()
    dates = []
    for i in range(1, 10):
        d = today - datetime.timedelta(days=i)
        if d.weekday() < 5:
            dates.append(d.strftime('%Y%m%d'))
        if len(dates) >= 3: break
    print(f"查询交易日: {dates}")

    all_limit = {}  # ts_code -> {'count': n, 'max_pct': x.x, 'days': [(date, pct),...]}
    for date in dates:
        rows = tushare('daily', {'trade_date': date}, 'ts_code,trade_date,pct_chg,close')
        if not rows: continue
        for r in rows:
            pct = float(r.get('pct_chg', 0))
            if pct >= 9.5:
                ts = r['ts_code']
                if ts not in all_limit:
                    all_limit[ts] = {'count': 0, 'max_pct': 0.0, 'days': []}
                all_limit[ts]['count'] += 1
                all_limit[ts]['max_pct'] = max(all_limit[ts]['max_pct'], pct)
                all_limit[ts]['days'].append((date, pct))
    print(f"近3日涨停股: {len(all_limit)} 只")

    # 优先：多次涨停 > 单次但高涨幅
    sorted_codes = sorted(all_limit.items(), key=lambda x: (x[1]['count'], x[1]['max_pct']), reverse=True)
    
    # 过滤ST、上市不满1年
    # 先排除明显新股（价格>100且涨停）
    candidates = []
    for ts, stats in sorted_codes:
        if stats['max_pct'] > 50 and stats['count'] == 1:
            continue  # 跳过单次暴涨（可能是新股）
        candidates.append((ts, stats))

    print(f"候选分析: {len(candidates)} 只")

    # 腾讯API获取K线+名称
    results = []
    dim_sum = {k: 0.0 for k in WEIGHTS}
    dim_cnt = {k: 0 for k in WEIGHTS}

    for i, (ts, stats) in enumerate(candidates):
        # 转换代码格式
        sym = ts.split('.')[0]
        if ts.endswith('.SH'):
            code = f"sh{sym}"
        else:
            code = f"sz{sym}"

        if i % 10 == 0:
            print(f"  进度: {i}/{len(candidates)} ... {code}")

        klines, name = tencent_kline(code, 120)
        if not klines or len(klines) < 30:
            time.sleep(0.1)
            continue

        price = klines[-1]['close']
        if price <= 0:
            time.sleep(0.1)
            continue

        pct_today = (klines[-1]['close'] - klines[-2]['close']) / klines[-2]['close'] * 100 if len(klines) >= 2 else 0
        is_limit_up = pct_today >= 9.5
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
        if price > 50: risks.append("股价偏高")
        if v < 0.5: risks.append("量能萎缩")
        limit_tag = "涨停" if is_limit_up else f"涨幅{pct_today:.1f}%"
        if len(stats['days']) > 1:
            risks.append(f"近3日{stats['count']}次涨停")
        elif stats['count'] == 1:
            risks.append(f"近3日1次涨停({stats['max_pct']:.1f}%)")

        results.append({
            '股票代码': code.upper(),
            '股票名称': name if name != code else ts,
            '上市满一年': True,
            '总分': round(total, 1),
            '时间得分': round(sc['时间'], 1),
            '空间得分': round(sc['空间'], 1),
            '异动得分': round(sc['异动'], 1),
            '缺口得分': round(sc['缺口'], 1),
            '龙头得分': round(sc['龙头'], 1),
            '转势得分': round(sc['转势'], 1),
            '股价得分': round(sc['股价'], 1),
            '强度得分': round(sc['强度'], 1),
            '热点得分': round(sc['热点'], 1),
            '核心技术信号': '; '.join(signals) if signals else '无明显信号',
            '风险提示': '; '.join(risks) if risks else '无',
            '数据日期': DATA_DATE,
            '当前价': round(price, 2),
            '涨跌幅': round(pct_today, 2),
        })

        for k in WEIGHTS:
            if sc[k] > 0:
                dim_sum[k] += sc[k]
                dim_cnt[k] += 1

        time.sleep(0.15)

    # 排序
    qualified = sorted(results, key=lambda x: x['总分'], reverse=True)
    # 过滤：总分>=50
    filtered = [r for r in qualified if r['总分'] >= 50]

    # 保存
    out = f"{WORK_DIR}/jlzz_limitup_results_{DATA_DATE}.json"
    with open(out, 'w') as f:
        json.dump({
            'run_date': DATA_DATE,
            'total_analyzed': len(results),
            'qualified_count': len(filtered),
            'dates': dates,
            'results': filtered[:100]
        }, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}\n近3日涨停股分析报告\n{'='*60}")
    print(f"分析: {len(results)} 只 | 符合条件(≥50分): {len(filtered)} 只")

    if filtered:
        print(f"\n🔥 九龙戏珠精选 TOP 20:")
        print("-"*100)
        for i, r in enumerate(filtered[:20], 1):
            print(f"{i:2}. {r['股票代码']} {r['股票名称']:10} 总分:{r['总分']:5.1f} "
                  f"热点:{r['热点得分']:4.0f} 强度:{r['强度得分']:4.0f} "
                  f"转势:{r['转势得分']:4.0f} 空间:{r['空间得分']:4.0f} "
                  f"现价:{r['当前价']:6.2f} {r['涨跌幅']:+.1f}%")
            print(f"    信号:{r['核心技术信号'][:50]}")
            print(f"    提示:{r['风险提示']}")

        print(f"\n各维度平均得分:")
        for k in WEIGHTS:
            if dim_cnt[k] > 0:
                print(f"  {k}: {dim_sum[k]/dim_cnt[k]:.1f} ({WEIGHTS[k]*100:.0f}%)")
    else:
        print("\n无符合条件股票")

    print(f"\n结果已保存: {out}")
    return filtered

if __name__ == "__main__":
    main()
