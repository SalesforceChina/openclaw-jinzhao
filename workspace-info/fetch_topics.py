#!/usr/bin/env python3
"""
定时抓取热点选题脚本
每小时从配置的平台抓取热点内容，写入飞书多维表格
"""

import os
import json
import time
import requests
from datetime import datetime
import sys
from typing import List, Dict, Any

# 添加当前目录到路径，以便导入工具
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 平台配置 - 实际使用时可以从飞书表格读取
PLATFORM_CONFIGS = [
    {
        "name": "知乎热榜",
        "url": "https://www.zhihu.com/hot",
        "type": "社区论坛",
        "selector": "HotList-list"  # 示例选择器，实际需要调整
    },
    {
        "name": "微博热搜",
        "url": "https://s.weibo.com/top/summary",
        "type": "综合",
        "selector": "#pl_top_realtimehot"
    },
    {
        "name": "36氪",
        "url": "https://36kr.com/hot-list",
        "type": "科技媒体",
        "selector": ".hotlist-item"
    }
]

def fetch_web_content(url: str) -> str:
    """抓取网页内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"抓取失败 {url}: {e}")
        return ""

def parse_zhihu_hot(html: str) -> List[Dict[str, Any]]:
    """解析知乎热榜"""
    topics = []
    try:
        # 这里需要根据实际HTML结构调整
        # 示例：假设找到热榜项
        import re
        # 简化示例，实际需要更复杂的解析
        pattern = r'<div class="HotList-itemTitle">([^<]+)</div>'
        titles = re.findall(pattern, html)
        
        for i, title in enumerate(titles[:10]):  # 取前10个
            topics.append({
                "title": title.strip(),
                "platform": "知乎热榜",
                "heat_index": 100 - i * 5,  # 模拟热度
                "url": f"https://www.zhihu.com/question/{i+10000}",
                "publish_time": int(time.time() * 1000),
                "content_type": "热点",
                "keywords": ["知乎", "热点"],
                "note": f"知乎热榜第{i+1}名"
            })
    except Exception as e:
        print(f"解析知乎热榜失败: {e}")
    
    return topics

def parse_weibo_hot(html: str) -> List[Dict[str, Any]]:
    """解析微博热搜"""
    topics = []
    try:
        import re
        # 简化示例
        pattern = r'<a[^>]*?href="([^"]*weibo\.com[^"]*)"[^>]*?>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        for i, (url, title) in enumerate(matches[:10]):
            topics.append({
                "title": title.strip(),
                "platform": "微博热搜",
                "heat_index": 100 - i * 8,
                "url": url if url.startswith("http") else f"https:{url}",
                "publish_time": int(time.time() * 1000),
                "content_type": "热点",
                "keywords": ["微博", "热搜"],
                "note": f"微博热搜第{i+1}名"
            })
    except Exception as e:
        print(f"解析微博热搜失败: {e}")
    
    return topics

def parse_36kr_hot(html: str) -> List[Dict[str, Any]]:
    """解析36氪热榜"""
    topics = []
    try:
        import re
        pattern = r'<a[^>]*?class="[^"]*article-item-title[^"]*"[^>]*?>([^<]+)</a>'
        titles = re.findall(pattern, html)
        
        for i, title in enumerate(titles[:10]):
            topics.append({
                "title": title.strip(),
                "platform": "36氪",
                "heat_index": 90 - i * 7,
                "url": f"https://36kr.com/p/{i+1000}",
                "publish_time": int(time.time() * 1000),
                "content_type": "科技",
                "keywords": ["36氪", "科技"],
                "note": "36氪热榜文章"
            })
    except Exception as e:
        print(f"解析36氪热榜失败: {e}")
    
    return topics

def save_to_log(topics: List[Dict[str, Any]]):
    """保存到本地日志文件（测试用）"""
    log_file = "/tmp/topic_fetch.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n=== 抓取时间: {timestamp} ===\n")
        for topic in topics:
            f.write(f"- {topic['platform']}: {topic['title']} (热度: {topic['heat_index']})\n")
    
    print(f"已保存 {len(topics)} 条选题到 {log_file}")

def main():
    """主函数"""
    print(f"开始抓取热点选题 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_topics = []
    
    # 抓取知乎热榜
    print("抓取知乎热榜...")
    zhihu_html = fetch_web_content("https://www.zhihu.com/hot")
    if zhihu_html:
        zhihu_topics = parse_zhihu_hot(zhihu_html)
        all_topics.extend(zhihu_topics)
        print(f"  找到 {len(zhihu_topics)} 条知乎热点")
    
    # 抓取微博热搜
    print("抓取微博热搜...")
    weibo_html = fetch_web_content("https://s.weibo.com/top/summary")
    if weibo_html:
        weibo_topics = parse_weibo_hot(weibo_html)
        all_topics.extend(weibo_topics)
        print(f"  找到 {len(weibo_topics)} 条微博热搜")
    
    # 抓取36氪热榜
    print("抓取36氪热榜...")
    kr36_html = fetch_web_content("https://36kr.com/hot-list")
    if kr36_html:
        kr36_topics = parse_36kr_hot(kr36_html)
        all_topics.extend(kr36_topics)
        print(f"  找到 {len(kr36_topics)} 条36氪热点")
    
    # 保存结果
    if all_topics:
        save_to_log(all_topics)
        print(f"总计抓取 {len(all_topics)} 条热点选题")
        
        # 这里可以添加写入飞书多维表格的代码
        # 需要调用飞书API
    else:
        print("未抓取到任何热点选题")
    
    print("抓取完成")

if __name__ == "__main__":
    main()