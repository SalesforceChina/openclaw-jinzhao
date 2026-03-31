#!/usr/bin/env python3
"""
测试正则表达式
"""

import re
import requests

# 获取页面内容
url = "https://tophub.today/n/WnBe01o371"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(url, headers=headers, timeout=10)

if response.status_code == 200:
    html = response.text
    
    print("页面长度:", len(html))
    print("\n=== 测试不同正则表达式 ===\n")
    
    # 测试1: 查找所有微信公众号链接
    pattern1 = r'https://mp\.weixin\.qq\.com/[^"\s]+'
    matches1 = re.findall(pattern1, html)
    print(f"测试1 - 微信公众号链接: {len(matches1)} 个")
    for i, link in enumerate(matches1[:5]):
        print(f"  {i+1}. {link[:80]}...")
    
    print("\n" + "="*80 + "\n")
    
    # 测试2: 查找文章标题和链接
    # 查找类似: <a href="链接">标题</a> 热度
    pattern2 = r'<a[^>]*href="([^"]*)"[^>]*>([^<]+)</a>\s*([^<\s]+)'
    matches2 = re.findall(pattern2, html)
    print(f"测试2 - 标题+链接+热度: {len(matches2)} 个")
    for i, (link, title, hot) in enumerate(matches2[:10]):
        if "mp.weixin.qq.com" in link:
            print(f"  {i+1}. 标题: {title[:30]}...")
            print(f"     链接: {link[:50]}...")
            print(f"     热度: {hot}")
            print()
    
    print("\n" + "="*80 + "\n")
    
    # 测试3: 查找特定区域的内容
    # 查找包含"10.0万"等热度值的行
    pattern3 = r'>([^<]+)</a>\s*([\d\.万]+)'
    matches3 = re.findall(pattern3, html)
    print(f"测试3 - 标题+热度: {len(matches3)} 个")
    for i, (title, hot) in enumerate(matches3[:15]):
        if len(title) > 5:  # 过滤短标题
            print(f"  {i+1}. 标题: {title[:40]}...")
            print(f"     热度: {hot}")
            print()
    
    print("\n" + "="*80 + "\n")
    
    # 测试4: 查看页面结构
    # 查找包含"微信 ‧ 24h热文榜"的区域
    start_idx = html.find("微信 ‧ 24h热文榜")
    if start_idx != -1:
        sample = html[start_idx:start_idx+2000]
        print("页面结构示例:")
        print(sample[:500])
        print("...")
        print(sample[-500:])
    
else:
    print(f"请求失败: {response.status_code}")