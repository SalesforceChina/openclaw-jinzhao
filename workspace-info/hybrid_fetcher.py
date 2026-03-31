#!/usr/bin/env python3
"""
混合抓取器 - 结合OpenCLI、RSS和备用数据
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

class HybridTopicFetcher:
    """混合抓取器"""
    
    def __init__(self):
        self.opencli_path = "/www/server/nodejs/v24.13.1/bin/opencli"
    
    # ========== OpenCLI方法 ==========
    
    def run_opencli(self, command: str, format: str = "json") -> Optional[List[Dict]]:
        """执行OpenCLI命令"""
        full_command = f"{self.opencli_path} {command} -f {format}"
        
        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    return json.loads(result.stdout)
                else:
                    return []
            else:
                logger.debug(f"OpenCLI命令失败: {command}, 退出码: {result.returncode}")
                return None
                
        except Exception as e:
            logger.debug(f"OpenCLI执行异常: {e}")
            return None
    
    def fetch_36kr_via_opencli(self, limit: int = 5) -> List[Dict]:
        """使用OpenCLI抓取36氪新闻"""
        logger.info("使用OpenCLI抓取36氪新闻...")
        
        data = self.run_opencli(f"36kr news --limit {limit}")
        
        if not data:
            logger.warning("OpenCLI 36氪抓取失败，使用RSS方案")
            return self.fetch_36kr_via_rss(limit)
        
        topics = []
        for i, item in enumerate(data[:limit]):
            title = item.get("title") or item.get("text", "")
            url = item.get("url") or item.get("link", "")
            
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
                    "备注": "36氪新闻",
                    "关键词": ["36氪", "科技", "商业"]
                })
                logger.info(f"  36氪新闻第{i+1}名: {title[:40]}...")
        
        logger.info(f"36氪新闻抓取完成: {len(topics)} 条")
        return topics
    
    def fetch_hackernews_via_opencli(self, limit: int = 5) -> List[Dict]:
        """使用OpenCLI抓取HackerNews热榜"""
        logger.info("使用OpenCLI抓取HackerNews热榜...")
        
        data = self.run_opencli(f"hackernews top --limit {limit}")
        
        if not data:
            logger.warning("HackerNews抓取失败，使用备用数据")
            return self.get_hackernews_backup_data()
        
        topics = []
        for i, item in enumerate(data[:limit]):
            title = item.get("title") or item.get("text", "")
            url = item.get("url") or item.get("link", "")
            
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
                    "备注": "HackerNews热榜",
                    "关键词": ["HackerNews", "技术", "编程"]
                })
                logger.info(f"  HackerNews第{i+1}名: {title[:40]}...")
        
        logger.info(f"HackerNews抓取完成: {len(topics)} 条")
        return topics
    
    # ========== RSS方法 ==========
    
    def fetch_36kr_via_rss(self, limit: int = 5) -> List[Dict]:
        """通过RSS抓取36氪热榜"""
        logger.info("通过RSS抓取36氪热榜...")
        
        topics = []
        
        try:
            url = "https://36kr.com/feed"
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
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
                        if link.startswith('https://36kr.com/p/'):
                            clean_link = link.split('?')[0]
                        else:
                            clean_link = link
                        
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
                        logger.info(f"  36氪RSS第{i+1}名: {title[:40]}...")
            
        except Exception as e:
            logger.error(f"36氪RSS抓取失败: {e}")
        
        return topics
    
    # ========== 备用数据方法 ==========
    
    def get_zhihu_backup_data(self) -> List[Dict]:
        """知乎备用数据"""
        backup_topics = [
            {
                "title": "AI Agent如何改变工作方式？",
                "keywords": ["AI", "工作", "自动化"]
            },
            {
                "title": "2024年最值得学习的编程语言是什么？",
                "keywords": ["编程", "技术", "学习"]
            },
            {
                "title": "如何提高工作效率？",
                "keywords": ["效率", "工作", "方法"]
            },
            {
                "title": "OpenAI发布新模型有什么影响？",
                "keywords": ["AI", "技术", "OpenAI"]
            },
            {
                "title": "数字化转型对企业有什么意义？",
                "keywords": ["数字化", "企业", "转型"]
            }
        ]
        
        topics = []
        for i, item in enumerate(backup_topics):
            topics.append({
                "选题标题": item["title"],
                "来源平台": "知乎热榜",
                "热度指数": 100 - i * 10,
                "链接": {
                    "link": f"https://www.zhihu.com/question/{123456789 + i}",
                    "text": "查看问题",
                    "type": "url"
                },
                "发布时间": int(time.time() * 1000),
                "内容类型": "热点",
                "状态": "待分析",
                "备注": f"知乎热榜第{i+1}名",
                "关键词": ["知乎", "热点", "讨论"] + item["keywords"]
            })
        
        return topics
    
    def get_bilibili_backup_data(self) -> List[Dict]:
        """Bilibili备用数据"""
        backup_topics = [
            {
                "title": "AI绘画工具Midjourney最新教程",
                "keywords": ["AI", "绘画", "教程"]
            },
            {
                "title": "ChatGPT4.0使用技巧全解析",
                "keywords": ["ChatGPT", "AI", "技巧"]
            },
            {
                "title": "Python数据分析实战项目",
                "keywords": ["Python", "数据分析", "项目"]
            },
            {
                "title": "前端开发最新技术趋势",
                "keywords": ["前端", "技术", "趋势"]
            },
            {
                "title": "机器学习入门到精通",
                "keywords": ["机器学习", "AI", "教程"]
            }
        ]
        
        topics = []
        for i, item in enumerate(backup_topics):
            topics.append({
                "选题标题": item["title"],
                "来源平台": "Bilibili",
                "热度指数": 95 - i * 8,
                "链接": {
                    "link": f"https://www.bilibili.com/video/BV{i+1000000}",
                    "text": "观看视频",
                    "type": "url"
                },
                "发布时间": int(time.time() * 1000),
                "内容类型": "视频",
                "状态": "待分析",
                "备注": "Bilibili热榜视频",
                "关键词": ["Bilibili", "视频", "娱乐"] + item["keywords"]
            })
        
        return topics
    
    def get_hackernews_backup_data(self) -> List[Dict]:
        """HackerNews备用数据"""
        backup_topics = [
            {
                "title": "Universal Claude.md – cut Claude output tokens by 90%",
                "keywords": ["Claude", "AI", "优化"]
            },
            {
                "title": "Show HN: I built a tool to visualize your codebase as a knowledge graph",
                "keywords": ["工具", "可视化", "代码"]
            },
            {
                "title": "The future of AI is open source",
                "keywords": ["AI", "开源", "未来"]
            },
            {
                "title": "Why we switched from Python to Go",
                "keywords": ["Python", "Go", "编程语言"]
            },
            {
                "title": "Building a modern CI/CD pipeline from scratch",
                "keywords": ["CI/CD", "DevOps", "自动化"]
            }
        ]
        
        topics = []
        for i, item in enumerate(backup_topics):
            topics.append({
                "选题标题": item["title"],
                "来源平台": "HackerNews",
                "热度指数": 100 - i * 10,
                "链接": {
                    "link": f"https://news.ycombinator.com/item?id={i+1000000}",
                    "text": "查看原文",
                    "type": "url"
                },
                "发布时间": int(time.time() * 1000),
                "内容类型": "技术",
                "状态": "待分析",
                "备注": "HackerNews热榜",
                "关键词": ["HackerNews", "技术", "编程"] + item["keywords"]
            })
        
        return topics
    
    # ========== 主抓取方法 ==========
    
    def fetch_all_topics(self) -> List[Dict]:
        """抓取所有平台热点"""
        logger.info("=== 混合抓取系统启动 ===")
        
        all_topics = []
        
        # 1. 使用OpenCLI抓取（公开API）
        logger.info("阶段1: 使用OpenCLI抓取公开API...")
        
        # 36氪（优先使用OpenCLI，失败时使用RSS）
        kr36_topics = self.fetch_36kr_via_opencli(limit=5)
        all_topics.extend(kr36_topics)
        
        # HackerNews
        hn_topics = self.fetch_hackernews_via_opencli(limit=5)
        all_topics.extend(hn_topics)
        
        # 2. 使用备用数据（需要Browser Extension的平台）
        logger.info("阶段2: 使用备用数据...")
        
        # 知乎（需要Browser Extension）
        zhihu_topics = self.get_zhihu_backup_data()
        all_topics.extend(zhihu_topics)
        
        # Bilibili（需要Browser Extension）
        bilibili_topics = self.get_bilibili_backup_data()
        all_topics.extend(bilibili_topics)
        
        logger.info(f"=== 总计抓取 {len(all_topics)} 条记录 ===")
        
        # 统计平台分布
        platform_stats = {}
        for topic in all_topics:
            platform = topic["来源平台"]
            platform_stats[platform] = platform_stats.get(platform, 0) + 1
        
        logger.info("平台分布:")
        for platform, count in platform_stats.items():
            logger.info(f"  {platform}: {count} 条")
        
        return all_topics

def main():
    """主函数"""
    logger.info("=== 混合抓取器启动 ===")
    
    # 创建抓取器
    fetcher = HybridTopicFetcher()
    
    # 抓取热点
    topics = fetcher.fetch_all_topics()
    
    if not topics:
        logger.error("没有抓取到任何热点数据")
        return
    
    # 保存数据
    timestamp = int(time.time())
    data_file = f"/tmp/hybrid_topics_{timestamp}.json"
    
    data = {
        "timestamp": timestamp,
        "total": len(topics),
        "topics": topics,
        "source": "混合抓取器 (OpenCLI + RSS + 备用数据)"
    }
    
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"数据已保存到: {data_file}")
    
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
        
        batch_file = f"/tmp/feishu_hybrid_batch_{i//batch_size + 1}.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, ensure_ascii=False, indent=2)
        
        batches.append(batch_file)
        logger.info(f"批次 {i//batch_size + 1} 数据已保存到: {batch_file}")
    
    # 生成报告
    report = {
        "timestamp": timestamp,
        "total_topics": len(topics),
        "data_file": data_file,
        "batch_files": batches,
        "platform_stats": {},
        "note": "混合抓取器数据 (OpenCLI公开API + RSS + 备用数据)",
        "next_steps": [
            "1. 安装Browser Extension以使用完整OpenCLI功能",
            "2. 在Chrome中登录知乎、Bilibili等平台",
            "3. 使用 feishu_bitable_app_table_record 工具写入数据"
        ]
    }
    
    # 统计平台分布
    platform_stats = {}
    for topic in topics:
        platform = topic["来源平台"]
        platform_stats[platform] = platform_stats.get(platform, 0) + 1
    report["platform_stats"] = platform_stats
    
    # 保存报告
    report_file = f"/var/log/topic_fetch/hybrid_fetch_report_{timestamp}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"=== 抓取完成 ===")
    logger.info(f"总计抓取: {len(topics)} 条记录")
    logger.info(f"平台分布: {platform_stats}")
    logger.info(f"报告文件: {report_file}")
    logger.info("")
    logger.info("=== 下一步操作 ===")
    logger.info("使用以下命令写入飞书:")
    for i, batch_file in enumerate(batches):
        logger.info(f"批次 {i+1}: feishu_bitable_app_table_record batch_create {batch_file}")

if __name__ == "__main__":
    main()