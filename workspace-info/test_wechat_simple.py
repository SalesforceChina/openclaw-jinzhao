#!/usr/bin/env python3
"""
简单测试微信公众号热榜 - 直接解析页面
"""

import requests
import json
import time
import re
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def fetch_wechat_hot_simple():
    """简单抓取微信公众号热榜"""
    logger.info("简单抓取微信公众号热榜...")
    
    try:
        # 今日热榜微信公众号页面
        url = "https://tophub.today/n/WnBe01o371"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            html = response.text
            
            # 查看HTML结构
            print("HTML长度:", len(html))
            print("前1000字符:", html[:1000])
            
            # 尝试不同的解析方法
            topics = []
            
            # 方法1: 查找文章链接
            link_pattern = r'<a[^>]*href="(https://mp\.weixin\.qq\.com/[^"]*)"[^>]*>([^<]+)</a>'
            link_matches = re.findall(link_pattern, html)
            
            print(f"找到 {len(link_matches)} 个微信公众号链接")
            
            for i, (link, title) in enumerate(link_matches[:10]):
                print(f"{i+1}. {title[:50]}...")
                print(f"   链接: {link[:50]}...")
                
                topics.append({
                    "选题标题": title.strip(),
                    "来源平台": "微信公众号",
                    "热度指数": 10000 - i * 500,  # 模拟热度
                    "链接": {
                        "link": link,
                        "text": "查看文章",
                        "type": "url"
                    },
                    "发布时间": int(time.time() * 1000),
                    "内容类型": "热点",
                    "状态": "待分析",
                    "备注": "微信公众号热榜（简单抓取）",
                    "关键词": ["微信公众号", "热榜"]
                })
            
            return topics
        
    except Exception as e:
        logger.error(f"抓取失败: {e}")
    
    return []

def main():
    """主函数"""
    logger.info("\n" + "=" * 60)
    logger.info("🔍 简单测试微信公众号热榜")
    logger.info("=" * 60)
    
    # 抓取数据
    topics = fetch_wechat_hot_simple()
    
    logger.info(f"\n📊 抓取结果: {len(topics)} 条记录")
    
    if topics:
        # 保存数据
        timestamp = int(time.time())
        data_file = f"/tmp/wechat_simple_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "total": len(topics),
            "source": "微信公众号热榜（简单抓取）",
            "topics": topics
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 数据已保存到: {data_file}")
        
        # 显示示例
        logger.info("\n📝 示例数据:")
        for i, topic in enumerate(topics[:3]):
            logger.info(f"{i+1}. {topic['选题标题'][:40]}...")
            logger.info(f"   链接: {topic['链接']['link'][:50]}...")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 测试完成")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()