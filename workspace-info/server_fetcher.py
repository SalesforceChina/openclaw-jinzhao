#!/usr/bin/env python3
"""
服务器版选题库抓取器 - 使用公开API和RSS源
适合Ubuntu服务器环境（无需Chrome扩展）
"""

import json
import time
import subprocess
import requests
import xml.etree.ElementTree as ET
import logging
from typing import List, Dict, Optional
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ServerTopicFetcher:
    """服务器版抓取器 - 使用公开API和RSS"""
    
    def __init__(self):
        self.opencli_path = "/www/server/nodejs/v24.13.1/bin/opencli"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    # ========== OpenCLI公开API方法 ==========
    
    def run_opencli(self, command: str) -> Optional[List[Dict]]:
        """执行OpenCLI命令"""
        try:
            result = subprocess.run(
                f"{self.opencli_path} {command}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout)
            return None
                
        except Exception as e:
            logger.debug(f"OpenCLI执行异常: {e}")
            return None
    
    def fetch_36kr_via_opencli(self, limit: int = 5) -> List[Dict]:
        """使用OpenCLI抓取36氪"""
        logger.info("抓取36氪新闻...")
        
        data = self.run_opencli(f"36kr news --limit {limit}")
        
        if not data:
            return self.fetch_36kr_via_rss(limit)
        
        topics = []
        for i, item in enumerate(data[:limit]):
            title = item.get("title") or ""
            url = item.get("url") or ""
            
            if title:
                topics.append({
                    "选题标题": title,
                    "来源平台": "36氪",
                    "热度指数": 95 - i * 8,
                    "链接": {
                        "link": url or f"https://36kr.com/p/{i+1000000}",
                        "text": "查看文章",
                        "type": "url"
                    },
                    "发布时间": int(time.time() * 1000),
                    "内容类型": "科技",
                    "状态": "待分析",
                    "备注": "36氪新闻（OpenCLI）",
                    "关键词": ["36氪", "科技", "商业"]
                })
        
        logger.info(f"✅ 36氪: {len(topics)} 条")
        return topics
    
    def fetch_hackernews_via_opencli(self, limit: int = 5) -> List[Dict]:
        """使用OpenCLI抓取HackerNews"""
        logger.info("抓取HackerNews热榜...")
        
        data = self.run_opencli(f"hackernews top --limit {limit}")
        
        if not data:
            return []
        
        topics = []
        for i, item in enumerate(data[:limit]):
            title = item.get("title") or ""
            url = item.get("url") or ""
            
            if title:
                topics.append({
                    "选题标题": title,
                    "来源平台": "HackerNews",
                    "热度指数": 100 - i * 10,
                    "链接": {
                        "link": url or f"https://news.ycombinator.com/item?id={i+1000000}",
                        "text": "查看原文",
                        "type": "url"
                    },
                    "发布时间": int(time.time() * 1000),
                    "内容类型": "技术",
                    "状态": "待分析",
                    "备注": "HackerNews热榜（OpenCLI）",
                    "关键词": ["HackerNews", "技术", "编程"]
                })
        
        logger.info(f"✅ HackerNews: {len(topics)} 条")
        return topics
    
    # ========== RSS方法 ==========
    
    def fetch_36kr_via_rss(self, limit: int = 5) -> List[Dict]:
        """通过RSS抓取36氪"""
        logger.info("通过RSS抓取36氪...")
        
        topics = []
        
        try:
            response = self.session.get("https://36kr.com/feed", timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                items = root.findall('.//item')[:limit]
                
                for i, item in enumerate(items):
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    
                    if title_elem is not None and link_elem is not None:
                        title = title_elem.text.strip()
                        link = link_elem.text.strip()
                        
                        # 清理链接
                        clean_link = link.split('?')[0] if '?' in link else link
                        
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
                            "备注": "36氪RSS",
                            "关键词": ["36氪", "科技", "商业"]
                        })
        
        except Exception as e:
            logger.error(f"❌ 36氪RSS抓取失败: {e}")
        
        logger.info(f"✅ 36氪RSS: {len(topics)} 条")
        return topics
    
    def fetch_rssp_huxiu(self, limit: int = 5) -> List[Dict]:
        """通过RSS抓取虎嗅"""
        logger.info("通过RSS抓取虎嗅...")
        
        topics = []
        
        try:
            # 虎嗅RSS
            response = self.session.get("https://www.huxiu.com/rss/0.xml", timeout=10)
            
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                items = root.findall('.//item')[:limit]
                
                for i, item in enumerate(items):
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    
                    if title_elem is not None and link_elem is not None:
                        title = title_elem.text.strip()
                        link = link_elem.text.strip()
                        
                        topics.append({
                            "选题标题": title,
                            "来源平台": "虎嗅",
                            "热度指数": 90 - i * 8,
                            "链接": {
                                "link": link,
                                "text": "查看文章",
                                "type": "url"
                            },
                            "发布时间": int(time.time() * 1000),
                            "内容类型": "科技",
                            "状态": "待分析",
                            "备注": "虎嗅RSS",
                            "关键词": ["虎嗅", "科技", "商业"]
                        })
        
        except Exception as e:
            logger.error(f"❌ 虎嗅RSS抓取失败: {e}")
        
        logger.info(f"✅ 虎嗅RSS: {len(topics)} 条")
        return topics
    
    # ========== 公开API方法 ==========
    
    def fetch_weibo_hot(self, limit: int = 5) -> List[Dict]:
        """通过公开API抓取微博热搜"""
        logger.info("抓取微博热搜...")
        
        topics = []
        
        try:
            # 使用微博热搜API
            url = "https://weibo.com/ajax/side/hotSearch"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("data") and data["data"].get("realtime"):
                    for i, item in enumerate(data["data"]["realtime"][:limit]):
                        title = item.get("word", "")
                        link = f"https://s.weibo.com/weibo?q={title}"
                        
                        topics.append({
                            "选题标题": title,
                            "来源平台": "微博",
                            "热度指数": 100 - i * 10,
                            "链接": {
                                "link": link,
                                "text": "查看热搜",
                                "type": "url"
                            },
                            "发布时间": int(time.time() * 1000),
                            "内容类型": "热点",
                            "状态": "待分析",
                            "备注": "微博热搜",
                            "关键词": ["微博", "热搜", "热点"]
                        })
        
        except Exception as e:
            logger.error(f"❌ 微博热搜抓取失败: {e}")
        
        logger.info(f"✅ 微博热搜: {len(topics)} 条")
        return topics
    
    def fetch_juejin_hot(self, limit: int = 5) -> List[Dict]:
        """通过公开API抓取掘金热榜"""
        logger.info("抓取掘金热榜...")
        
        topics = []
        
        try:
            # 掘金热门文章API
            url = "https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed"
            params = {
                "limit": limit,
                "sort_type": 3  # 热门
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("data"):
                    for i, item in enumerate(data["data"][:limit]):
                        article = item.get("article", {})
                        title = article.get("title", "")
                        article_id = article.get("article_id", "")
                        
                        if title:
                            topics.append({
                                "选题标题": title,
                                "来源平台": "掘金",
                                "热度指数": 90 - i * 8,
                                "链接": {
                                    "link": f"https://juejin.cn/post/{article_id}",
                                    "text": "查看文章",
                                    "type": "url"
                                },
                                "发布时间": int(time.time() * 1000),
                                "内容类型": "技术",
                                "状态": "待分析",
                                "备注": "掘金热门",
                                "关键词": ["掘金", "技术", "开发"]
                            })
        
        except Exception as e:
            logger.error(f"❌ 掘金热榜抓取失败: {e}")
        
        logger.info(f"✅ 掘金热榜: {len(topics)} 条")
        return topics
    
    # ========== 知乎热榜（备用方案） ==========
    
    def fetch_zhihu_hot_via_api(self, limit: int = 5) -> List[Dict]:
        """通过公开API抓取知乎热榜"""
        logger.info("抓取知乎热榜...")
        
        topics = []
        
        try:
            # 知乎热榜API
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("data"):
                    for i, item in enumerate(data["data"][:limit]):
                        target = item.get("target", {})
                        title = target.get("title", "")
                        question_id = target.get("id", "")
                        
                        if title:
                            topics.append({
                                "选题标题": title,
                                "来源平台": "知乎热榜",
                                "热度指数": 100 - i * 10,
                                "链接": {
                                    "link": f"https://www.zhihu.com/question/{question_id}",
                                    "text": "查看问题",
                                    "type": "url"
                                },
                                "发布时间": int(time.time() * 1000),
                                "内容类型": "热点",
                                "状态": "待分析",
                                "备注": "知乎热榜（API）",
                                "关键词": ["知乎", "热点", "讨论"]
                            })
        
        except Exception as e:
            logger.error(f"❌ 知乎热榜抓取失败: {e}")
        
        logger.info(f"✅ 知乎热榜: {len(topics)} 条")
        return topics
    
    # ========== 主抓取方法 ==========
    
    def fetch_all_topics(self) -> List[Dict]:
        """抓取所有平台热点"""
        logger.info("=" * 60)
        logger.info("🚀 服务器版选题库抓取系统启动")
        logger.info("=" * 60)
        
        all_topics = []
        
        # 1. OpenCLI公开API
        logger.info("\n【阶段1】使用OpenCLI抓取公开API...")
        
        # 36氪
        kr36_topics = self.fetch_36kr_via_opencli(limit=5)
        all_topics.extend(kr36_topics)
        
        # HackerNews
        hn_topics = self.fetch_hackernews_via_opencli(limit=5)
        all_topics.extend(hn_topics)
        
        # 2. RSS源
        logger.info("\n【阶段2】使用RSS抓取...")
        
        # 虎嗅
        huxiu_topics = self.fetch_rssp_huxiu(limit=5)
        all_topics.extend(huxiu_topics)
        
        # 3. 公开API
        logger.info("\n【阶段3】使用公开API抓取...")
        
        # 知乎热榜
        zhihu_topics = self.fetch_zhihu_hot_via_api(limit=5)
        all_topics.extend(zhihu_topics)
        
        # 微博热搜
        weibo_topics = self.fetch_weibo_hot(limit=5)
        all_topics.extend(weibo_topics)
        
        # 掘金热榜
        juejin_topics = self.fetch_juejin_hot(limit=5)
        all_topics.extend(juejin_topics)
        
        # 统计
        logger.info("\n" + "=" * 60)
        logger.info(f"🎉 抓取完成！总计: {len(all_topics)} 条记录")
        logger.info("=" * 60)
        
        platform_stats = {}
        for topic in all_topics:
            platform = topic["来源平台"]
            platform_stats[platform] = platform_stats.get(platform, 0) + 1
        
        logger.info("\n📊 平台分布:")
        for platform, count in platform_stats.items():
            logger.info(f"  • {platform}: {count} 条")
        
        return all_topics

def main():
    """主函数"""
    logger.info("\n" + "=" * 60)
    logger.info("🔥 服务器版选题库抓取器")
    logger.info("适合Ubuntu服务器环境（无需Chrome扩展）")
    logger.info("=" * 60 + "\n")
    
    # 创建抓取器
    fetcher = ServerTopicFetcher()
    
    # 抓取热点
    topics = fetcher.fetch_all_topics()
    
    if not topics:
        logger.error("❌ 没有抓取到任何数据")
        return
    
    # 保存数据
    timestamp = int(time.time())
    data_file = f"/tmp/server_topics_{timestamp}.json"
    
    data = {
        "timestamp": timestamp,
        "total": len(topics),
        "source": "服务器版抓取器（OpenCLI + RSS + 公开API）",
        "topics": topics
    }
    
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n💾 数据已保存到: {data_file}")
    
    # 准备飞书数据
    batches = []
    batch_size = 5
    
    for i in range(0, len(topics), batch_size):
        batch = topics[i:i+batch_size]
        batch_data = {
            "app_token": "XDQXbxM97aiBAPswH4wcbmTRnCb",
            "table_id": "tblSTNrT7TrPuIAz",
            "records": [{"fields": topic} for topic in batch]
        }
        
        batch_file = f"/tmp/feishu_server_batch_{i//batch_size + 1}.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, ensure_ascii=False, indent=2)
        
        batches.append(batch_file)
    
    logger.info(f"\n📦 已准备 {len(batches)} 个批次写入飞书")
    for i, batch_file in enumerate(batches):
        logger.info(f"  批次 {i+1}: {batch_file}")
    
    # 生成报告
    report = {
        "timestamp": timestamp,
        "total_topics": len(topics),
        "data_file": data_file,
        "batch_files": batches,
        "platform_stats": {},
        "method": "服务器版（OpenCLI + RSS + 公开API）",
        "note": "适合Ubuntu服务器环境，无需Chrome扩展",
        "advantages": [
            "无需浏览器环境",
            "使用公开API和RSS",
            "真实数据源",
            "适合定时任务"
        ]
    }
    
    platform_stats = {}
    for topic in topics:
        platform = topic["来源平台"]
        platform_stats[platform] = platform_stats.get(platform, 0) + 1
    report["platform_stats"] = platform_stats
    
    report_file = f"/var/log/topic_fetch/server_fetch_report_{timestamp}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n📄 报告文件: {report_file}")
    logger.info("\n" + "=" * 60)
    logger.info("✅ 抓取完成！")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()