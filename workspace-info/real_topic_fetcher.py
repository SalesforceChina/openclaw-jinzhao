#!/usr/bin/env python3
"""
真实热点抓取器 - 从各平台获取真实的热点内容和链接
"""

import json
import time
import re
import requests
from datetime import datetime
from typing import List, Dict, Optional
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class RealTopicFetcher:
    """真实热点抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
    def fetch_zhihu_hot(self, limit: int = 5) -> List[Dict]:
        """抓取知乎热榜"""
        logger.info("开始抓取知乎热榜...")
        topics = []
        
        try:
            # 知乎热榜API
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('data', [])[:limit]
                
                for i, item in enumerate(items):
                    target = item.get('target', {})
                    title = target.get('title', '').strip()
                    question_id = target.get('id', '')
                    
                    if title and question_id:
                        topics.append({
                            "选题标题": title,
                            "来源平台": "知乎热榜",
                            "热度指数": 100 - i * 10,  # 根据排名计算热度
                            "链接": {
                                "link": f"https://www.zhihu.com/question/{question_id}",
                                "text": "查看问题",
                                "type": "url"
                            },
                            "发布时间": int(time.time() * 1000),
                            "内容类型": "热点",
                            "状态": "待分析",
                            "备注": f"知乎热榜第{i+1}名",
                            "关键词": ["知乎", "热点", "讨论"]
                        })
                        logger.info(f"  知乎热榜第{i+1}名: {title}")
                
                logger.info(f"知乎热榜抓取完成，共获取 {len(topics)} 条记录")
            else:
                logger.error(f"知乎热榜API请求失败: {response.status_code}")
                
        except Exception as e:
            logger.error(f"抓取知乎热榜时出错: {e}")
        
        return topics
    
    def fetch_36kr_hot(self, limit: int = 5) -> List[Dict]:
        """抓取36氪热榜"""
        logger.info("开始抓取36氪热榜...")
        topics = []
        
        try:
            # 36氪热榜页面
            url = "https://36kr.com/hot-list"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # 解析文章链接和标题
                # 36氪热榜的文章链接模式
                pattern = r'<a[^>]*href="(/p/\d+)"[^>]*>([^<]+)</a>'
                matches = re.findall(pattern, html)
                
                for i, (path, title) in enumerate(matches[:limit]):
                    title = title.strip()
                    if title:
                        topics.append({
                            "选题标题": title,
                            "来源平台": "36氪",
                            "热度指数": 95 - i * 8,  # 根据排名计算热度
                            "链接": {
                                "link": f"https://36kr.com{path}",
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
                
                logger.info(f"36氪热榜抓取完成，共获取 {len(topics)} 条记录")
            else:
                logger.error(f"36氪热榜请求失败: {response.status_code}")
                
        except Exception as e:
            logger.error(f"抓取36氪热榜时出错: {e}")
        
        return topics
    
    def fetch_weibo_hot(self, limit: int = 5) -> List[Dict]:
        """抓取微博热搜"""
        logger.info("开始抓取微博热搜...")
        topics = []
        
        try:
            # 微博热搜页面
            url = "https://s.weibo.com/top/summary"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # 解析热搜条目
                pattern = r'<a[^>]*href="(/weibo\?q=[^"]*)"[^>]*>([^<]+)</a>'
                matches = re.findall(pattern, html)
                
                for i, (path, title) in enumerate(matches[:limit]):
                    title = title.strip()
                    if title:
                        topics.append({
                            "选题标题": title,
                            "来源平台": "微博热搜",
                            "热度指数": 100 - i * 12,  # 根据排名计算热度
                            "链接": {
                                "link": f"https://s.weibo.com{path}",
                                "text": "查看热搜",
                                "type": "url"
                            },
                            "发布时间": int(time.time() * 1000),
                            "内容类型": "热点",
                            "状态": "待分析",
                            "备注": f"微博热搜第{i+1}名",
                            "关键词": ["微博", "热搜", "社会热点"]
                        })
                        logger.info(f"  微博热搜第{i+1}名: {title}")
                
                logger.info(f"微博热搜抓取完成，共获取 {len(topics)} 条记录")
            else:
                logger.error(f"微博热搜请求失败: {response.status_code}")
                
        except Exception as e:
            logger.error(f"抓取微博热搜时出错: {e}")
        
        return topics
    
    def fetch_all_topics(self) -> List[Dict]:
        """抓取所有平台的热点"""
        logger.info("=== 开始抓取所有平台热点 ===")
        
        all_topics = []
        
        # 抓取知乎热榜
        zhihu_topics = self.fetch_zhihu_hot(limit=5)
        all_topics.extend(zhihu_topics)
        
        # 抓取36氪热榜
        kr36_topics = self.fetch_36kr_hot(limit=5)
        all_topics.extend(kr36_topics)
        
        # 抓取微博热搜
        weibo_topics = self.fetch_weibo_hot(limit=5)
        all_topics.extend(weibo_topics)
        
        logger.info(f"=== 抓取完成，总计 {len(all_topics)} 条记录 ===")
        
        # 统计平台分布
        platform_stats = {}
        for topic in all_topics:
            platform = topic["来源平台"]
            platform_stats[platform] = platform_stats.get(platform, 0) + 1
        
        logger.info("平台分布:")
        for platform, count in platform_stats.items():
            logger.info(f"  {platform}: {count} 条")
        
        return all_topics
    
    def save_to_file(self, topics: List[Dict], filename: str = None):
        """保存数据到文件"""
        if not filename:
            timestamp = int(time.time())
            filename = f"/tmp/real_topics_{timestamp}.json"
        
        data = {
            "timestamp": int(time.time()),
            "total": len(topics),
            "topics": topics
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"数据已保存到: {filename}")
        return filename
    
    def prepare_for_feishu(self, topics: List[Dict]) -> Dict:
        """准备飞书写入数据"""
        # 将数据分组，每批最多5条
        batches = []
        batch_size = 5
        
        for i in range(0, len(topics), batch_size):
            batch = topics[i:i+batch_size]
            batch_data = {
                "app_token": "XDQXbxM97aiBAPswH4wcbmTRnCb",
                "table_id": "tblSTNrT7TrPuIAz",
                "records": [{"fields": topic} for topic in batch]
            }
            batches.append(batch_data)
        
        return batches

def main():
    """主函数"""
    logger.info("=== 真实热点抓取系统启动 ===")
    
    # 创建抓取器
    fetcher = RealTopicFetcher()
    
    # 抓取所有热点
    topics = fetcher.fetch_all_topics()
    
    if not topics:
        logger.error("没有抓取到任何热点数据")
        return
    
    # 保存原始数据
    data_file = fetcher.save_to_file(topics)
    
    # 准备飞书数据
    batches = fetcher.prepare_for_feishu(topics)
    
    # 保存批次数据
    for i, batch in enumerate(batches):
        batch_file = f"/tmp/feishu_batch_{i+1}.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)
        logger.info(f"批次 {i+1} 数据已保存到: {batch_file}")
    
    # 生成报告
    report = {
        "timestamp": int(time.time()),
        "total_topics": len(topics),
        "data_file": data_file,
        "batch_files": [f"/tmp/feishu_batch_{i+1}.json" for i in range(len(batches))],
        "platform_stats": {},
        "next_steps": [
            "1. 使用 feishu_bitable_app_table_record 工具写入数据",
            "2. 检查飞书表格中的链接是否正确",
            "3. 验证抓取的数据质量"
        ]
    }
    
    # 统计平台分布
    platform_stats = {}
    for topic in topics:
        platform = topic["来源平台"]
        platform_stats[platform] = platform_stats.get(platform, 0) + 1
    report["platform_stats"] = platform_stats
    
    # 保存报告
    report_file = f"/var/log/topic_fetch/real_fetch_report_{int(time.time())}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"=== 抓取完成 ===")
    logger.info(f"总计抓取: {len(topics)} 条记录")
    logger.info(f"平台分布: {platform_stats}")
    logger.info(f"报告文件: {report_file}")
    logger.info("")
    logger.info("=== 下一步操作 ===")
    logger.info("使用以下命令写入飞书:")
    for i in range(len(batches)):
        logger.info(f"批次 {i+1}: feishu_bitable_app_table_record batch_create /tmp/feishu_batch_{i+1}.json")

if __name__ == "__main__":
    main()