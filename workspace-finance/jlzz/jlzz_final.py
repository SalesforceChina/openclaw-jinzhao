#!/usr/bin/env python3
"""
九龙戏珠 A股选股系统
数据源: 腾讯财经(实时+K线) + BaoStock(补充历史数据)
"""

import json
import time
import datetime
import requests
import re
import baostock as bs

WORK_DIR = "/root/.openclaw/workspace-finance/jlzz"
DATA_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
BITABLE_APP_TOKEN = "H4PKb6gJRa1ZccsPY3Yc42eGnTd"
BITABLE_TABLE_ID = "tblLo5ZXoU7DpkSk"

WEIGHTS = {
    '时间': 0.15, '空间': 0.12, '异动': 0.10, '缺口': 0.12,
    '龙头': 0.10, '转势': 0.13, '股价': 0.08, '强度': 0.10, '热点': 0.10,
}

# 沪深300成分股(示例列表，实际应用中应从新浪/东方财富获取完整列表)
HS300_CODES = [
    ('sh600000', '浦发银行'), ('sh600016', '民生银行'), ('sh600019', '宝钢股份'),
    ('sh600028', '中国石化'), ('sh600030', '中信证券'), ('sh600031', '三一重工'),
    ('sh600036', '招商银行'), ('sh600048', '保利发展'), ('sh600050', '中国联通'),
    ('sh600104', '上汽集团'), ('sh600109', '国投资本'), ('sh600111', '北方稀土'),
    ('sh600150', '中国船舶'), ('sh600176', '中国化学'), ('sh600183', '生亚硅业'),
    ('sh600196', '复星医药'), ('sh600276', '恒瑞医药'), ('sh600297', '万华化学'),
    ('sh600309', '宝丰能源'), ('sh600406', '国电南瑞'), ('sh600436', '片仔癀'),
    ('sh600438', '通威股份'), ('sh600519', '贵州茅台'), ('sh600547', '山东黄金'),
    ('sh600570', '恒生电子'), ('sh600585', '海螺水泥'), ('sh600588', '用友网络'),
    ('sh600690', '海尔智家'), ('sh600703', '三安光电'), ('sh600745', '闻泰科技'),
    ('sh600760', '中航沈飞'), ('sh600809', '山西汾酒'), ('sh600837', '海通证券'),
    ('sh600887', '伊利股份'), ('sh600893', '航发动力'), ('sh600900', '长江电力'),
    ('sh600905', '三峡能源'), ('sh600918', '中金公司'), ('sh600926', '杭州银行'),
    ('sh600989', '宝武钢铁'), ('sh601006', '大秦铁路'), ('sh601012', '隆基绿能'),
    ('sh601066', '中信建投'), ('sh601088', '中国神华'), ('sh601118', '海南橡胶'),
    ('sh601138', '工业富联'), ('sh601166', '兴业银行'), ('sh601169', '北京银行'),
    ('sh601186', '中国铁建'), ('sh601211', '国泰君安'), ('sh601225', '陕西煤业'),
    ('sh601288', '农业银行'), ('sh601318', '中国平安'), ('sh601319', '中国人保'),
    ('sh601328', '交通银行'), ('sh601336', '新华保险'), ('sh601390', '中国中铁'),
    ('sh601398', '工商银行'), ('sh601601', '中国太保'), ('sh601628', '中国人寿'),
    ('sh601658', '邮储银行'), ('sh601668', '中国建筑'), ('sh601688', '华泰证券'),
    ('sh601728', '中国电信'), ('sh601818', '光大银行'), ('sh601857', '中国石油'),
    ('sh601888', '中国中免'), ('sh601899', '紫金矿业'), ('sh601919', '中远海控'),
    ('sh601939', '建设银行'), ('sh601985', '中国核电'), ('sh601988', '中国银行'),
    ('sh601989', '中国重工'), ('sh601995', '中金公司'), ('sh603259', '药明康德'),
    ('sh603288', '海天味业'), ('sh603501', '韦尔股份'), ('sh603799', '华友钴业'),
    ('sh603986', '兆易创新'), ('sh688041', '寒武纪'), ('sh688111', '金山办公'),
    ('sh688981', '中芯国际'), ('sz000001', '平安银行'), ('sz000002', '万科A'),
    ('sz000063', '中兴通讯'), ('sz000066', '中国长城'), ('sz000100', 'TCL科技'),
    ('sz000333', '美的集团'), ('sz000338', '潍柴动力'), ('sz000425', '徐工机械'),
    ('sz000538', '云南白药'), ('sz000568', '泸州老窖'), ('sz000596', '古井贡酒'),
    ('sz000651', '格力电器'), ('sz000661', '长春高新'), ('sz000708', '中信特钢'),
    ('sz000725', '京东方A'), ('sz000768', '中航西飞'), ('sz000858', '五粮液'),
    ('sz000876', '新希望'), ('sz000895', '双汇发展'), ('sz000938', '紫光股份'),
    ('sz000961', '中南建设'), ('sz000983', '山西焦煤'), ('sz001896', '豫能控股'),
    ('sz002001', '新和成'), ('sz002027', '分众传媒'), ('sz002042', '华孚时尚'),
    ('sz002050', '三花智控'), ('sz002142', '宁波银行'), ('sz002236', '大华股份'),
    ('sz002252', '上海莱士'), ('sz002304', '洋河股份'), ('sz002311', '海大集团'),
    ('sz002352', '顺丰控股'), ('sz002371', '北方华创'), ('sz002415', '海康威视'),
    ('sz002460', '赣锋锂业'), ('sz002475', '立讯精密'), ('sz002493', '荣盛石化'),
    ('sz002594', '比亚迪'), ('sz002601', '龙佰集团'), ('sz002714', '牧原股份'),
    ('sz002736', '国信证券'), ('sz002812', '中伟股份'), ('sz002841', '视源股份'),
    ('sz300015', '爱尔眼科'), ('sz300059', '东方财富'), ('sz300122', '智飞生物'),
    ('sz300124', '汇川技术'), ('sz300142', '沃森生物'), ('sz300274', '阳光电源'),
    ('sz300347', '泰格医药'), ('sz300408', '三环集团'), ('sz300450', '先导智能'),
    ('sz300496', '中科创达'), ('sz300498', '温氏股份'), ('sz300750', '宁德时代'),
    ('sz300751', '迈为股份'), ('sz300760', '迈瑞医疗'), ('sz300782', '卓胜微'),
    ('sz300896', '爱美客'), ('sz300998', '宁波方正'),
]

def get_realtime_data(code):
    """获取实时行情"""
    try:
        url = f"https://qt.gtimg.cn/q={code}"
        resp = requests.get(url, timeout=10)
        resp.encoding = 'gbk'
        text = resp.text.strip()
        match = re.search(r'v_\w+="([^"]+)"', text)
        if not match:
            return None
        fields = match.group(1).split('~')
        if len(fields) < 40:
            return None
        price = float(fields[3]) if fields[3] else 0
        prev_close = float(fields[4]) if fields[4] else 0
        pct = float(fields[32]) if len(fields) > 32 and fields[32] else 0
        return {
            'code': code, 'name': fields[1], 'price': price,
            'prev_close': prev_close, 'pct': pct,
            'open': float(fields[5]) if fields[5] else 0,
            'high': float(fields[33]) if len(fields) > 33 and fields[33] else 0,
            'low': float(fields[34]) if len(fields) > 34 and fields[34] else 0,
            'volume': float(fields[6]) if fields[6] else 0,
            'is_limit_up': abs(pct - 10.0) < 0.2 if prev_close > 0 else False,
        }
    except:
        return None

def get_kline_data(code, days=120):
    """获取日K线(腾讯财经)"""
    try:
        if code.startswith('sh') or code.startswith('sz'):
            market = code[:2]
            stock_code = code[2:]
        else:
            market = 'sh'
            stock_code = code
        url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={market}{stock_code},day,,,{days},qfq"
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if 'data' not in data:
            return None
        stock_data = data['data']
        if isinstance(stock_data, dict):
            klines = stock_data.get('qfqday', stock_data.get('day', []))
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

def get_baostock_kline(code, days=60):
    """从BaoStock获取补充历史数据"""
    bs_code = code.replace('sh', 'sh.').replace('sz', 'sz.')
    rs = bs.query_history_k_data_plus(
        bs_code,
        'date,open,high,low,close,volume',
        start_date='2025-01-01',
        end_date='2025-12-31',
        frequency='d', adjustflag='2'
    )
    klines = []
    while rs.error_code == '0' and rs.next():
        row = rs.get_row_data()
        try:
            klines.append({
                'date': row[0], 'open': float(row[1]),
                'close': float(row[4]), 'high': float(row[2]),
                'low': float(row[3]), 'volume': float(row[5]),
            })
        except:
            continue
    return klines

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
    if len(klines) < 5:
        return 1.0
    avg = sum(klines[-5:-1][i]['volume'] for i in range(4)) / 4
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
    high_ratio = today['high'] / today['close'] if today['close'] > 0 else 1
    # 涨停或接近涨停
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

def analyze_stock(code, name):
    """分析单只股票"""
    rt = get_realtime_data(code)
    klines = get_kline_data(code, 120)
    
    if not klines or len(klines) < 30:
        # 尝试从BaoStock补充
        bs_klines = get_baostock_kline(code, 60)
        if bs_klines:
            klines = bs_klines
    
    if not klines or len(klines) < 30:
        return None
    
    price = rt['price'] if rt else klines[-1]['close']
    if price <= 0:
        return None
    
    is_limit_up = rt.get('is_limit_up', False) if rt else False
    
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
    if not is_limit_up: risks.append("非涨停股")
    
    pct_change = 0
    if rt:
        pct_change = rt.get('pct', 0)
    elif len(klines) >= 2:
        pct_change = (klines[-1]['close'] - klines[-2]['close']) / klines[-2]['close'] * 100
    
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
        '涨跌幅': round(pct_change, 2),
    }

def feishu_batch_create(app_token, table_id, records):
    """写入飞书多维表格"""
    import subprocess
    import json as json_lib
    
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create',
        '-H', 'Content-Type: application/json',
        '-d', json_lib.dumps({'records': records})
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json_lib.loads(result.stdout)

def main():
    print("=" * 60)
    print("九龙戏珠 A股选股系统")
    print(f"运行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    bs.login()
    
    results = []
    dim_avgs = {k: [] for k in WEIGHTS}
    
    print(f"\n开始分析 {len(HS300_CODES)} 只股票...\n")
    
    for i, (code, name) in enumerate(HS300_CODES):
        if i % 30 == 0:
            print(f"进度: {i}/{len(HS300_CODES)} ... 当前: {code} {name}")
        
        result = analyze_stock(code, name)
        if result:
            results.append(result)
            for dim in dim_avgs:
                key = f"{dim}得分"
                if key in result:
                    dim_avgs[dim].append(result[key])
        
        if i % 10 == 0:
            time.sleep(0.3)
    
    bs.logout()
    
    # 排序
    qualified = sorted(results, key=lambda x: x['总分'], reverse=True)
    
    # 筛选：总分>=50 或 热点得分>=60 或 有涨停信号
    filtered = [r for r in qualified if r['总分'] >= 50 or r['热点得分'] >= 60 or r['时间得分'] > 0]
    
    # 保存
    output_file = f"{WORK_DIR}/jlzz_results_{DATA_DATE}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'run_date': DATA_DATE,
            'total_analyzed': len(results),
            'qualified_count': len(filtered),
            'results': filtered[:100],
        }, f, ensure_ascii=False, indent=2)
    
    # 报告
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
        
        print(f"\n各维度平均得分:")
        for dim, scores in dim_avgs.items():
            if scores:
                avg = sum(scores) / len(scores)
                print(f"  {dim:4}: {avg:5.1f} (权重: {WEIGHTS[dim]*100:.0f}%)")
        
        # 写入飞书
        print(f"\n写入飞书多维表格...")
        records = [{'fields': {k: v for k, v in r.items() if k != '当前价' and k != '涨跌幅'}} for r in filtered[:50]]
        try:
            resp = feishu_batch_create(BITABLE_APP_TOKEN, BITABLE_TABLE_ID, records)
            if resp.get('data'):
                print(f"成功写入 {len(resp['data'].get('records', []))} 条")
            else:
                print(f"写入响应: {resp}")
        except Exception as e:
            print(f"写入失败: {e}")
    else:
        print("\n没有符合条件股票")
        top10 = qualified[:10]
        for i, r in enumerate(top10, 1):
            print(f"{i:2}. {r['股票代码']} {r['股票名称']:10} 总分:{r['总分']:5.1f}")
    
    print(f"\n结果已保存到: {output_file}")
    return filtered

if __name__ == "__main__":
    main()
