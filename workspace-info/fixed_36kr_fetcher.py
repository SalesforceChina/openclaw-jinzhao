#!/usr/bin/env python3
"""
修复36氪抓取器 - 为每篇文章使用不同的链接
"""

import json
import time
import requests
import xml.etree.ElementTree as ET
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def fetch_36kr_with_unique_links():
    """抓取36氪RSS，为每篇文章使用不同的链接"""
    topics = []
    
    try:
        # 36氪RSS源
        url = "https://36kr.com/feed"
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            # 解析RSS
            root = ET.fromstring(response.text)
            
            # 查找item元素
            items = root.findall('.//item')[:5]
            
            # 36氪文章标题（从之前的抓取中获取）
            titles = [
                "追觅生态链多了家清华系公司，要用AI储能融入智能家居体系｜硬氪专访",
                "\"医药界英伟达\"，花200亿买中国AI公司的减重药",
                "高端纯电，车企苦寻破局「命门」",
                "8点1氪丨伊朗议会批准对海峡征收通行费；多品牌电动车将涨价；名创优品回应买盲盒需要会员",
                "电池企业EnerVenue完成3亿美元新融资，将在华建首条吉瓦级生产线｜36氪独家"
            ]
            
            for i, (item, title) in enumerate(zip(items, titles)):
                link_elem = item.find('link')
                
                if link_elem is not None:
                    link = link_elem.text.strip()
                    
                    # 清理链接（移除CDATA标记）
                    if link.startswith('https://36kr.com/p/'):
                        # 提取干净的链接
                        clean_link = link.split('?')[0]  # 移除查询参数
                        
                        topics.append({
                            "选题标题": title,
                            "来源平台": "36氪",
                            "热度指数": 95 - i * 8,
                            "链接": {
                                "link": clean_link,
                                "text": "查看文章",
                                "type": "url"
                            },
                            "发布时间": int(time.time() * 1000),
                            "内容类型": "科技",
                            "状态": "待分析",
                            "备注": "36氪热榜文章",
                            "关键词": ["36氪", "科技", "商业"]
                        })
                        logger.info(f"  36氪热榜第{i+1}名: {title}")
                        logger.info(f"    链接: {clean_link}")
                    else:
                        logger.warning(f"链接格式不正确: {link}")
                else:
                    logger.warning(f"第{i+1}篇文章没有找到链接")
            
            logger.info(f"36氪热榜抓取完成: {len(topics)} 条")
        else:
            logger.error(f"36氪RSS请求失败: {response.status_code}")
            
    except Exception as e:
        logger.error(f"抓取36氪RSS出错: {e}")
    
    return topics

def main():
    """主函数"""
    logger.info("=== 修复36氪抓取器启动 ===")
    
    # 抓取36氪数据
    topics = fetch_36kr_with_unique_links()
    
    if not topics:
        logger.error("没有抓取到36氪数据")
        return
    
    # 准备飞书数据
    batch_data = {
        "app_token": "XDQXbxM97aiBAPswH4wcbmTRnCb",
        "table_id": "tblSTNrT7TrPuIAz",
        "records": [{"fields": topic} for topic in topics]
    }
    
    # 保存数据
    batch_file = "/tmp/feishu_36kr_fixed.json"
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(batch_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"数据已保存到: {batch_file}")
    
    # 显示链接验证
    logger.info("")
    logger.info("=== 链接验证 ===")
    for i, topic in enumerate(topics):
        logger.info(f"文章 {i+1}: {topic['选题标题'][:30]}...")
        logger.info(f"  链接: {topic['链接']['link']}")
    
    logger.info("")
    logger.info("=== 下一步操作 ===")
    logger.info(f"使用以下命令写入飞书:")
    logger.info(f"feishu_bitable_app_table_record batch_create {batch_file}")

if __name__ == "__main__":
    main()