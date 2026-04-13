#!/usr/bin/env python3
"""
九龙戏珠 A股选股系统
基于冯矿伟《双龙战法》技术分析策略
"""

import json
import time
import math
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

def get_realtime_data(code):
    """获取实时行情"""
    try:
        if not code.startswith('sh') and not code.startswith('sz'):
            code = 'sh' + code
        url = f"https://qt.gtimg.cn/q={code}"
        resp = requests.get(url, timeout=10)
        resp.encoding = 'gbk'
        text = resp.text.strip()
        
        if not text:
            return None
        
        # 解析 v_sh600000="1~名称~代码~..."
        match = re.search(r'v_\w+="([^"]+)"', text)
        if not match:
            return None
        
        fields = match.group(1).split('~')
        if len(fields) < 40:
            return None
        
        price = float(fields[3]) if fields[3] else 0
        prev_close = float(fields[4]) if fields[4] else 0
        pct_change = float(fields[32]) if len(fields) > 32 and fields[32] else 0
        
        return {
            'code': code,
            'name': fields[1],
            'price': price,
            'prev_close': prev_close,
            'open': float(fields[5]) if fields[5] else 0,
            'volume': float(fields[6]) if fields[6] else 0,
            'pct_change': pct_change,
            'change': float(fields[31]) if len(fields) > 31 and fields[31] else 0,
            'high': float(fields[33]) if len(fields) > 33 and fields[33] else 0,
            'low': float(fields[34]) if len(fields) > 34 and fields[34] else 0,
            'limit_up_price': round(prev_close * 1.10, 2) if prev_close > 0 else 0,
            'is_limit_up': abs(pct_change - 10.0) < 0.1 if prev_close > 0 else False,
        }
    except Exception as e:
        print(f"获取实时数据失败 {code}: {e}")
        return None

def get_kline_data(code, days=60):
    """获取日K线"""
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
            # Try qfqday first (前复权日K), then day
            if 'qfqday' in stock_data:
                klines = stock_data['qfqday']
            elif 'day' in stock_data:
                klines = stock_data['day']
            elif isinstance(list(stock_data.values())[0], dict):
                inner = list(stock_data.values())[0]
                klines = inner.get('qfqday', inner.get('day', []))
            else:
                return None
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
    except Exception as e:
        return None

def calc_ma(klines, period):
    if len(klines) < period:
        return None
    return sum(k['close'] for k in klines[-period:]) / period

def calc_macd(klines, fast=12, slow=26):
    if len(klines) < slow + 5:
        return None, None
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
    for i in range(1, len(klines)):
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
    avg = sum(klines[-5:][i]['volume'] for i in range(5)) / 5
    today = klines[-1]['volume'] if klines else 1
    return today / avg if avg > 0 else 1.0

def impulse_score(klines):
    if len(klines) < 5:
        return 0
    score = 0
    for i in range(-5, 0):
        if i+1 >= len(klines):
            break
        k = klines[i]
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
            score += 30
    if dif > 0:
        score += 15
    ma5, ma10, ma20 = calc_ma(klines, 5), calc_ma(klines, 10), calc_ma(klines, 20)
    if ma5 and ma10 and ma20:
        if ma5 > ma10 > ma20:
            score += 20
        elif ma5 < ma10 < ma20:
            score -= 20
    return min(max(score, 0), 100)

def time_score(is_limit_up, klines):
    if not is_limit_up:
        return 0
    if klines:
        t = klines[-1]
        if t['open'] >= t['close'] * 0.98:
            return 100
        elif t['close'] > t['open'] * 1.05:
            return 80
        return 60
    return 50

def price_score(p):
    if p <= 0: return 50
    if p < 5: return 100
    elif p < 8: return 90
    elif p < 10: return 80
    elif p < 15: return 60
    elif p < 30: return 40
    return 20

def strength_score(klines, rt):
    if not klines or not rt:
        return 50
    score = 50
    pct = rt.get('pct_change', 0)
    if pct >= 10.0: score += 30
    elif pct >= 7.0: score += 25
    elif pct >= 5.0: score += 20
    elif pct >= 3.0: score += 10
    vr = vol_ratio(klines)
    if vr > 3: score += 15
    elif vr > 2: score += 10
    elif vr > 1.5: score += 5
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
    limit_days = sum(1 for k in klines[-5:] if k['close'] >= k['open'] * 1.095)
    if limit_days >= 2:
        score = max(score, 80)
    return min(score, 100)

def sector_score(klines, rt):
    if not rt:
        return 50
    pct = rt.get('pct_change', 0)
    if pct >= 10.0: return 100
    elif pct >= 7.0: return 85
    elif pct >= 5.0: return 70
    elif pct >= 3.0: return 60
    elif pct >= 0: return 50
    return 30

def analyze_stock(code, name=''):
    rt = get_realtime_data(code)
    klines = get_kline_data(code, 60)
    if not rt or not klines:
        return None
    
    price = rt['price']
    is_limit_up = rt.get('is_limit_up', False)
    
    scores = {
        '时间': time_score(is_limit_up, klines),
        '空间': position_score(klines, price),
        '异动': impulse_score(klines),
        '缺口': identify_gap(klines)[0],
        '龙头': sector_score(klines, rt),
        '转势': trend_score(klines),
        '股价': price_score(price),
        '强度': strength_score(klines, rt),
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
    if not is_limit_up and scores['热点'] < 50: risks.append("非热点股")
    
    return {
        '股票代码': code,
        '股票名称': rt.get('name', name),
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
        '当前价': price,
        '涨跌幅': rt.get('pct_change', 0),
    }

def write_to_bitable(results):
    """写入飞书多维表格"""
    try:
        from feishu_client import FeishuClient
        client = FeishuClient()
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
        if records:
            client.batch_create(BITABLE_APP_TOKEN, BITABLE_TABLE_ID, records)
            print(f"已写入 {len(records)} 条记录到飞书多维表格")
    except Exception as e:
        print(f"写入飞书失败: {e}")
        print("结果已保存为JSON文件")

def main():
    print("=" * 60)
    print("九龙戏珠 A股选股系统")
    print(f"运行时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 测试股票列表
    test_stocks = [
        ('sh600000', '浦发银行'), ('sh600036', '招商银行'),
        ('sh601318', '中国平安'), ('sh600519', '贵州茅台'),
        ('sh600276', '恒瑞医药'), ('sh601888', '中国中免'),
        ('sz000858', '五粮液'), ('sh600585', '海螺水泥'),
        ('sz002475', '立讯精密'), ('sh600030', '中信证券'),
        ('sz300750', '宁德时代'), ('sh601012', '隆基绿能'),
        ('sh600276', '恒瑞医药'), ('sh601166', '兴业银行'),
        ('sz002594', '比亚迪'), ('sh600309', '万华化学'),
        ('sz000333', '美的集团'), ('sh600887', '伊利股份'),
        ('sh600019', '宝钢股份'), ('sh601398', '工商银行'),
    ]
    
    results = []
    dim_avgs = {k: [] for k in WEIGHTS}
    
    print(f"\n开始分析 {len(test_stocks)} 只股票...\n")
    
    for code, name in test_stocks:
        print(f"分析中: {code} {name}...", end=' ')
        result = analyze_stock(code, name)
        if result:
            results.append(result)
            print(f"总分: {result['总分']}")
            for dim in dim_avgs:
                key = f"{dim}得分"
                if key in result:
                    dim_avgs[dim].append(result[key])
        time.sleep(0.2)
    
    qualified = [r for r in results if r['总分'] >= 60]
    qualified.sort(key=lambda x: x['总分'], reverse=True)
    
    output_file = f"{WORK_DIR}/jlzz_results_{DATA_DATE}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'run_date': DATA_DATE,
            'total_analyzed': len(results),
            'qualified_count': len(qualified),
            'results': qualified,
        }, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print("分析报告")
    print("=" * 60)
    print(f"分析股票总数: {len(results)}")
    print(f"符合条件(≥60分): {len(qualified)}")
    
    if qualified:
        print(f"\nTOP 10 股票:")
        print("-" * 60)
        for i, r in enumerate(qualified[:10], 1):
            print(f"{i:2}. {r['股票代码']} {r['股票名称']:10} 总分: {r['总分']:5.1f}  现价: {r['当前价']:6.2f}  涨幅: {r['涨跌幅']:+.2f}%")
        
        print(f"\n各维度平均得分:")
        print("-" * 40)
        for dim, scores in dim_avgs.items():
            if scores:
                avg = sum(scores) / len(scores)
                print(f"  {dim:4}: {avg:5.1f} (权重: {WEIGHTS[dim]*100:.0f}%)")
        
        print(f"\n核心技术信号:")
        print("-" * 40)
        sig_count = {}
        for r in qualified:
            for sig in r['核心技术信号'].split('; '):
                if sig and sig != '无明显信号':
                    sig_count[sig] = sig_count.get(sig, 0) + 1
        for sig, cnt in sorted(sig_count.items(), key=lambda x: -x[1])[:5]:
            print(f"  {sig}: {cnt}只")
        
        # 写入飞书
        print(f"\n准备写入飞书多维表格...")
        write_to_bitable(qualified[:50])
    else:
        print("\n没有符合条件(≥60分)的股票")
        print("\n调试信息:")
        for r in results[:3]:
            print(f"  {r['股票代码']} {r['股票名称']} 总分:{r['总分']} 热点:{r.get('热点得分',0)} 强度:{r.get('强度得分',0)}")
    
    print(f"\n结果已保存到: {output_file}")
    return qualified

if __name__ == "__main__":
    main()
