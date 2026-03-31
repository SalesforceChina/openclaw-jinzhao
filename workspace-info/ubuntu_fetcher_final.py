#!/usr/bin/env python3
"""
Ubuntu服务器专用选题库抓取器 - 最终版
使用无头浏览器和公开API，无需Chrome扩展
"""

import json
import time
import subprocess
import requests
import logging
from typing import List, Dict, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class UbuntuServerFetcher:
    """Ubuntu服务器专用抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    # ========== 使用curl/wget抓取 ==========
    
    def fetch_via_curl(self, url: str) -> Optional[str]:
        """使用curl抓取网页内容"""
        try:
            cmd = f"curl -s -L '{url}'"
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            return None
                
        except Exception as e:
            logger.debug(f"curl抓取失败: {e}")
            return None
    
    # ========== 知乎热榜（无头模式） ==========
    
    def fetch_zhihu_hot_headless(self, limit: int = 5) -> List[Dict]:
        """使用无头模式抓取知乎热榜"""
        logger.info("抓取知乎热榜（无头模式）...")
        
        topics = []
        
        try:
            # 使用curl抓取知乎热榜页面
            html = self.fetch_via_curl("https://www.zhihu.com/hot")
            
            if html:
                # 简单解析HTML
                import re
                
                # 查找热榜条目
                pattern = r'<div[^>]*class="[^"]*HotItem-title[^"]*"[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
                matches = re.findall(pattern, html, re.DOTALL)[:limit]
                
                for i, (link, title) in enumerate(matches):
                    full_link = f"https://www.zhihu.com{link}" if link.startswith("/") else link
                    
                    topics.append({
                        "选题标题": title.strip(),
                        "来源平台": "知乎热榜",
                        "热度指数": 100 - i * 10,
                        "链接": {
                            "link": full_link,
                            "text": "查看问题",
                            "type": "url"
                        },
                        "发布时间": int(time.time() * 1000),
                        "内容类型": "热点",
                        "状态": "待分析",
                        "备注": "知乎热榜（无头模式）",
                        "关键词": ["知乎", "热点", "讨论"]
                    })
        
        except Exception as e:
            logger.error(f"❌ 知乎热榜抓取失败: {e}")
        
        logger.info(f"✅ 知乎热榜: {len(topics)} 条")
        return topics
    
    # ========== Bilibili热榜（API） ==========
    
    def fetch_bilibili_hot_api(self, limit: int = 5) -> List[Dict]:
        """使用Bilibili API抓取热榜"""
        logger.info("抓取Bilibili热榜（API）...")
        
        topics = []
        
        try:
            # Bilibili热榜API
            url = "https://api.bilibili.com/x/web-interface/ranking/v2"
            params = {
                "rid": 0,  # 全站
                "type": "all"
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("data") and data["data"].get("list"):
                    for i, item in enumerate(data["data"]["list"][:limit]):
                        title = item.get("title", "")
                        bvid = item.get("bvid", "")
                        
                        if title:
                            topics.append({
                                "选题标题": title,
                                "来源平台": "Bilibili",
                                "热度指数": 95 - i * 8,
                                "链接": {
                                    "link": f"https://www.bilibili.com/video/{bvid}",
                                    "text": "观看视频",
                                    "type": "url"
                                },
                                "发布时间": int(time.time() * 1000),
                                "内容类型": "视频",
                                "状态": "待分析",
                                "备注": "Bilibili热榜（API）",
                                "关键词": ["Bilibili", "视频", "娱乐"]
                            })
        
        except Exception as e:
            logger.error(f"❌ Bilibili热榜抓取失败: {e}")
        
        logger.info(f"✅ Bilibili热榜: {len(topics)} 条")
        return topics
    
    # ========== 微博热搜（无头模式） ==========
    
    def fetch_weibo_hot_headless(self, limit: int = 5) -> List[Dict]:
        """使用无头模式抓取微博热搜"""
        logger.info("抓取微博热搜（无头模式）...")
        
        topics = []
        
        try:
            # 使用curl抓取微博热搜页面
            html = self.fetch_via_curl("https://s.weibo.com/top/summary")
            
            if html:
                # 解析热搜
                import re
                
                # 查找热搜条目
                pattern = r'<a[^>]*href="([^"]*weibo[^"]*)"[^>]*>([^<]*)</a>'
                matches = re.findall(pattern, html)[:limit]
                
                for i, (link, title) in enumerate(matches):
                    full_link = f"https://s.weibo.com{link}" if link.startswith("/") else link
                    
                    topics.append({
                        "选题标题": title.strip(),
                        "来源平台": "微博热搜",
                        "热度指数": 100 - i * 10,
                        "链接": {
                            "link": full_link,
                            "text": "查看热搜",
                            "type": "url"
                        },
                        "发布时间": int(time.time() * 1000),
                        "内容类型": "热点",
                        "状态": "待分析",
                        "备注": "微博热搜（无头模式）",
                        "关键词": ["微博", "热搜", "热点"]
                    })
        
        except Exception as e:
            logger.error(f"❌ 微博热搜抓取失败: {e}")
        
        logger.info(f"✅ 微博热搜: {len(topics)} 条")
        return topics
    
    # ========== 36氪热榜（API） ==========
    
    def fetch_36kr_hot_api(self, limit: int = 5) -> List[Dict]:
        """使用36氪API抓取热榜"""
        logger.info("抓取36氪热榜（API）...")
        
        topics = []
        
        try:
            # 36氪热榜API
            url = "https://36kr.com/pp/api/aggregation-entity/hot-list"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("data") and data["data"].get("hotListData"):
                    for i, item in enumerate(data["data"]["hotListData"][:limit]):
                        title = item.get("title", "")
                        item_id = item.get("itemId", "")
                        
                        if title:
                            topics.append({
                                "选题标题": title,
                                "来源平台": "36氪",
                                "热度指数": 95 - i * 8,
                                "链接": {
                                    "link": f"https://36kr.com/p/{item_id}",
                                    "text": "查看文章",
                                    "type": "url"
                                },
                                "发布时间": int(time.time() * 1000),
                                "内容类型": "科技",
                                "状态": "待分析",
                                "备注": "36氪热榜（API）",
                                "关键词": ["36氪", "科技", "商业"]
                            })
        
        except Exception as e:
            logger.error(f"❌ 36氪热榜抓取失败: {e}")
        
        logger.info(f"✅ 36氪热榜: {len(topics)} 条")
        return topics
    
    # ========== 掘金热榜（API） ==========
    
    def fetch_juejin_hot_api(self, limit: int = 5) -> List[Dict]:
        """使用掘金API抓取热榜"""
        logger.info("抓取掘金热榜（API）...")
        
        topics = []
        
        try:
            # 掘金热门文章API
            url = "https://api.juejin.cn/content_api/v1/content/article_rank"
            params = {
                "category_id": "1",  # 综合
                "type": "hot",
                "count": limit
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("data"):
                    for i, item in enumerate(data["data"][:limit]):
                        article = item.get("content", {})
                        title = article.get("title", "")
                        article_id = article.get("content_id", "")
                        
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
                                "备注": "掘金热榜（API）",
                                "关键词": ["掘金", "技术", "开发"]
                            })
        
        except Exception as e:
            logger.error(f"❌ 掘金热榜抓取失败: {e}")
        
        logger.info(f"✅ 掘金热榜: {len(topics)} 条")
        return topics
    
    # ========== 主抓取方法 ==========
    
    def fetch_all_topics(self):
        """抓取所有平台热点"""
        logger.info("=" * 60)
        logger.info("🚀 Ubuntu服务器专用选题库抓取系统启动")
        logger.info("=" * 60)
        
        all_topics = []
        
        # 1. 知乎热榜（无头模式）
        logger.info("\n【阶段1】知乎热榜...")
        zhihu_topics = self.fetch_zhihu_hot_headless(limit=3)
        all_topics.extend(zhihu_topics)
        
        # 2. Bilibili热榜（API）
        logger.info("\n【阶段2】Bilibili热榜...")
        bilibili_topics = self.fetch_bilibili_hot_api(limit=3)
        all_topics.extend(bilibili_topics)
        
        # 3. 微博热搜（无头模式）
        logger.info("\n【阶段3】微博热搜...")
        weibo_topics = self.fetch_weibo_hot_headless(limit=3)
        all_topics.extend(weibo_topics)
        
        # 4. 36氪热榜（API）
        logger.info("\n【阶段4】36氪热榜...")
        kr36_topics = self.fetch_36kr_hot_api(limit=3)
        all_topics.extend(kr36_topics)
        
        # 5. 掘金热榜（API）
        logger.info("\n【阶段5】掘金热榜...")
        juejin_topics = self.fetch_juejin_hot_api(limit=3)
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
        
        return all_topics, platform_stats

def main():
    """主函数"""
    logger.info("\n" + "=" * 60)
    logger.info("🔥 Ubuntu服务器专用选题库抓取器")
    logger.info("使用无头浏览器和公开API，无需Chrome扩展")
    logger.info("=" * 60 + "\n")
    
    # 创建抓取器
    fetcher = UbuntuServerFetcher()
    
    # 抓取热点
    topics, platform_stats = fetcher.fetch_all_topics()
    
    if not topics:
        logger.error("❌ 没有抓取到任何数据")
        return
    
    # 保存数据
    timestamp = int(time.time())
    data_file = f"/tmp/ubuntu_topics_{timestamp}.json"
    
    data = {
        "timestamp": timestamp,
        "total": len(topics),
        "source": "Ubuntu服务器专用抓取器（无头模式 + API）",
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
        
        batch_file = f"/tmp/feishu_ubuntu_batch_{i//batch_size + 1}.json"
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
        "platform_stats": platform_stats,
        "method": "Ubuntu服务器版（无头模式 + API）",
        "note": "适合Ubuntu服务器环境，无需Chrome扩展",
        "advantages": [
            "无需浏览器环境",
            "使用公开API",
            "真实数据源",
            "适合定时任务"
        ]
    }
    
    report_file = f"/var/log/topic_fetch/ubuntu_fetch_report_{timestamp}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n📄 报告文件: {report_file}")
    logger.info("\n" + "=" * 60)
    logger.info("✅ 抓取完成！")
    logger.info("=" * 60)
    
    # 显示示例数据
    if topics:
        logger.info("\n📝 示例数据:")
        for i, topic in enumerate(topics[:2]):
            logger.info(f"  {i+1}. {topic['选题标题'][:50]}...")
            logger.info(f"     来源: {topic['来源平台']}, 热度: {topic['热度指数']}")
            logger.info(f"     链接: {topic['链接']['link'][:50]}...")

if __name__ == "__main__":
    main()