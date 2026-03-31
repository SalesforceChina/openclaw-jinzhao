#!/usr/bin/env python3
"""
使用Jina Reader抓取热点内容 - 绕过反爬虫限制
"""

import json
import time
import re
import requests
import logging
from typing import List, Dict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class JinaFetcher:
    """使用Jina Reader抓取热点"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
    
    def fetch_with_jina(self, url: str) -> str:
        """使用Jina Reader获取页面内容"""
        jina_url = f"https://r.jina.ai/{url}"
        try:
            response = self.session.get(jina_url, timeout=15)
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"Jina请求失败: {response.status_code}")
                return ""
        except Exception as e:
            logger.error(f"Jina请求出错: {e}")
            return ""
    
    def parse_zhihu_hot(self, html: str, limit: int = 5) -> List[Dict]:
        """解析知乎热榜页面"""
        topics = []
        
        try:
            # 知乎热榜的简化解析
            # 查找问题和链接
            pattern = r'https://www\.zhihu\.com/question/(\d+)[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html)
            
            for i, (qid, title) in enumerate(matches[:limit]):
                title = title.strip()
                if title and qid:
                    topics.append({
                        "选题标题": title,
                        "来源平台": "知乎热榜",
                        "热度指数": 100 - i * 10,
                        "链接": {
                            "link": f"https://www.zhihu.com/question/{qid}",
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
            
        except Exception as e:
            logger.error(f"解析知乎热榜出错: {e}")
        
        return topics
    
    def parse_36kr_hot(self, html: str, limit: int = 5) -> List[Dict]:
        """解析36氪热榜页面"""
        topics = []
        
        try:
            # 36氪热榜解析
            # 查找文章链接
            pattern = r'https://36kr\.com/p/(\d+)[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html)
            
            for i, (pid, title) in enumerate(matches[:limit]):
                title = title.strip()
                if title and pid:
                    topics.append({
                        "选题标题": title,
                        "来源平台": "36氪",
                        "热度指数": 95 - i * 8,
                        "链接": {
                            "link": f"https://36kr.com/p/{pid}",
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
            
        except Exception as e:
            logger.error(f"解析36氪热榜出错: {e}")
        
        return topics
    
    def parse_weibo_hot(self, html: str, limit: int = 5) -> List[Dict]:
        """解析微博热搜页面"""
        topics = []
        
        try:
            # 微博热搜解析
            # 查找热搜词条
            pattern = r'https://s\.weibo\.com/weibo\?q=([^&"]+)[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html)
            
            for i, (query, title) in enumerate(matches[:limit]):
                title = title.strip()
                if title:
                    # URL编码查询参数
                    import urllib.parse
                    encoded_query = urllib.parse.quote(query)
                    
                    topics.append({
                        "选题标题": title,
                        "来源平台": "微博热搜",
                        "热度指数": 100 - i * 12,
                        "链接": {
                            "link": f"https://s.weibo.com/weibo?q={encoded_query}",
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
            
        except Exception as e:
            logger.error(f"解析微博热搜出错: {e}")
        
        return topics
    
    def fetch_all_topics(self) -> List[Dict]:
        """抓取所有平台热点"""
        logger.info("=== 使用Jina Reader抓取热点 ===")
        
        all_topics = []
        
        # 知乎热榜
        logger.info("抓取知乎热榜...")
        zhihu_html = self.fetch_with_jina("https://www.zhihu.com/hot")
        if zhihu_html:
            zhihu_topics = self.parse_zhihu_hot(zhihu_html, limit=5)
            all_topics.extend(zhihu_topics)
            logger.info(f"知乎热榜抓取完成: {len(zhihu_topics)} 条")
        else:
            logger.error("知乎热榜抓取失败")
        
        # 36氪热榜
        logger.info("抓取36氪热榜...")
        kr36_html = self.fetch_with_jina("https://36kr.com/hot-list")
        if kr36_html:
            kr36_topics = self.parse_36kr_hot(kr36_html, limit=5)
            all_topics.extend(kr36_topics)
            logger.info(f"36氪热榜抓取完成: {len(kr36_topics)} 条")
        else:
            logger.error("36氪热榜抓取失败")
        
        # 微博热搜
        logger.info("抓取微博热搜...")
        weibo_html = self.fetch_with_jina("https://s.weibo.com/top/summary")
        if weibo_html:
            weibo_topics = self.parse_weibo_hot(weibo_html, limit=5)
            all_topics.extend(weibo_topics)
            logger.info(f"微博热搜抓取完成: {len(weibo_topics)} 条")
        else:
            logger.error("微博热搜抓取失败")
        
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
    logger.info("=== Jina Reader热点抓取系统启动 ===")
    
    # 创建抓取器
    fetcher = JinaFetcher()
    
    # 抓取热点
    topics = fetcher.fetch_all_topics()
    
    if not topics:
        logger.error("没有抓取到任何热点数据")
        return
    
    # 保存数据
    timestamp = int(time.time())
    data_file = f"/tmp/jina_topics_{timestamp}.json"
    
    data = {
        "timestamp": timestamp,
        "total": len(topics),
        "topics": topics
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
        
        batch_file = f"/tmp/feishu_jina_batch_{i//batch_size + 1}.json"
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
    report_file = f"/var/log/topic_fetch/jina_fetch_report_{timestamp}.json"
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