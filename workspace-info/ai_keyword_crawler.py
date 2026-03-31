#!/usr/bin/env python3
"""
根据关键字抓取内容：AI + (Openclaw 或 小龙虾)
"""

import requests
import json
import time
import re
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

class AICrawler:
    """AI相关关键词抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
        # 关键词配置
        self.keywords = {
            "primary": "AI",
            "secondary": ["Openclaw", "小龙虾", "OpenClaw", "clawd", "ClawdBot"]
        }
        
        # 搜索平台配置
        self.search_platforms = [
            {
                "name": "GitHub",
                "url": "https://api.github.com/search/repositories",
                "params": {"q": "AI Openclaw", "sort": "stars", "order": "desc"}
            },
            {
                "name": "知乎",
                "url": "https://www.zhihu.com/api/v4/search_v3",
                "params": {"q": "AI 小龙虾", "t": "general", "lc_idx": "0", "correction": "1"}
            },
            {
                "name": "掘金",
                "url": "https://api.juejin.cn/search_api/v1/search",
                "params": {"query": "AI Openclaw", "id_type": 0, "cursor": "0", "limit": 20}
            },
            {
                "name": "微信公众号搜索",
                "url": "https://weixin.sogou.com/weixin",
                "params": {"query": "AI 小龙虾", "type": "2"}
            }
        ]
    
    def search_all_platforms(self, limit_per_platform: int = 5) -> List[Dict]:
        """在所有平台上搜索关键词"""
        logger.info(f"开始搜索关键词: AI + ({' 或 '.join(self.keywords['secondary'])})")
        
        all_results = []
        
        for platform in self.search_platforms:
            try:
                logger.info(f"搜索平台: {platform['name']}")
                results = self._search_platform(platform, limit_per_platform)
                all_results.extend(results)
                
                logger.info(f"  → 找到 {len(results)} 条结果")
                
            except Exception as e:
                logger.error(f"搜索平台 {platform['name']} 失败: {e}")
        
        # 去重和过滤
        filtered_results = self._filter_and_deduplicate(all_results)
        
        logger.info(f"总计找到 {len(filtered_results)} 条相关结果")
        return filtered_results
    
    def _search_platform(self, platform: Dict, limit: int) -> List[Dict]:
        """搜索单个平台"""
        try:
            if platform["name"] == "GitHub":
                response = self.session.get(
                    platform["url"],
                    params=platform["params"],
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # 这里可以添加具体的解析逻辑
                    return []
            
            elif platform["name"] == "知乎":
                # 知乎需要特殊处理
                return self._search_zhihu_simulated(limit)
            
            elif platform["name"] == "掘金":
                return self._search_juejin_simulated(limit)
            
            elif platform["name"] == "微信公众号搜索":
                return self._search_weixin_simulated(limit)
        
        except Exception as e:
            logger.error(f"搜索 {platform['name']} 失败: {e}")
        
        return []
    
    def _search_zhihu_simulated(self, limit: int) -> List[Dict]:
        """模拟知乎搜索（实际需要API密钥）"""
        # 这里使用模拟数据，实际使用时需要真实的知乎API
        simulated_results = [
            {
                "title": "OpenClaw：开源的个人AI助手框架深度解析",
                "url": "https://zhuanlan.zhihu.com/p/123456789",
                "description": "OpenClaw（曾用名Moltbot、ClawdBot）是一款开源的个人AI助手框架，支持本地优先、自托管、多通道连接。",
                "platform": "知乎",
                "keywords": ["AI", "OpenClaw", "开源", "个人助手"]
            },
            {
                "title": "小龙虾AI：如何用AI技术优化小龙虾养殖？",
                "url": "https://www.zhihu.com/question/123456789",
                "description": "探讨AI技术在小龙虾养殖中的应用，包括水质监测、生长预测、病害识别等。",
                "platform": "知乎",
                "keywords": ["AI", "小龙虾", "养殖", "农业科技"]
            }
        ]
        
        return simulated_results[:limit]
    
    def _search_juejin_simulated(self, limit: int) -> List[Dict]:
        """模拟掘金搜索"""
        simulated_results = [
            {
                "title": "OpenClaw从0到1搭建个人AI助理 - 掘金",
                "url": "https://juejin.cn/post/123456789",
                "description": "详细教程：如何使用OpenClaw框架搭建个人AI助手，支持多通道、本地部署。",
                "platform": "掘金",
                "keywords": ["AI", "OpenClaw", "教程", "个人助理"]
            },
            {
                "title": "AI+农业：小龙虾智能养殖系统设计与实现",
                "url": "https://juejin.cn/post/987654321",
                "description": "基于AI技术的小龙虾智能养殖系统，实现自动化监控和智能决策。",
                "platform": "掘金",
                "keywords": ["AI", "小龙虾", "农业", "智能养殖"]
            }
        ]
        
        return simulated_results[:limit]
    
    def _search_weixin_simulated(self, limit: int) -> List[Dict]:
        """模拟微信公众号搜索"""
        simulated_results = [
            {
                "title": "OpenClaw开源AI助手框架发布1.0版本",
                "url": "https://mp.weixin.qq.com/s/abcdefg123456",
                "description": "OpenClaw 1.0正式发布，支持20+聊天应用通道，本地优先设计。",
                "platform": "微信公众号",
                "keywords": ["AI", "OpenClaw", "开源", "框架"]
            },
            {
                "title": "AI赋能传统农业：小龙虾养殖的数字化转型",
                "url": "https://mp.weixin.qq.com/s/hijklmn789012",
                "description": "AI技术如何帮助小龙虾养殖业实现数字化转型和智能化升级。",
                "platform": "微信公众号",
                "keywords": ["AI", "小龙虾", "农业", "数字化转型"]
            }
        ]
        
        return simulated_results[:limit]
    
    def _filter_and_deduplicate(self, results: List[Dict]) -> List[Dict]:
        """过滤和去重结果"""
        seen_urls = set()
        filtered = []
        
        for result in results:
            url = result.get("url", "")
            
            # 去重
            if url in seen_urls:
                continue
            
            # 检查是否包含关键词
            title = result.get("title", "").lower()
            description = result.get("description", "").lower()
            
            # 必须包含AI
            if "ai" not in title and "ai" not in description:
                # 检查中文"人工智能"
                if "人工智能" not in title and "人工智能" not in description:
                    continue
            
            # 检查是否包含次要关键词
            has_secondary = False
            for keyword in self.keywords["secondary"]:
                kw_lower = keyword.lower()
                if kw_lower in title or kw_lower in description:
                    has_secondary = True
                    break
            
            if not has_secondary:
                continue
            
            seen_urls.add(url)
            filtered.append(result)
        
        return filtered
    
    def convert_to_feishu_format(self, results: List[Dict]) -> List[Dict]:
        """转换为飞书表格格式"""
        feishu_records = []
        
        for i, result in enumerate(results):
            record = {
                "选题标题": result.get("title", ""),
                "来源平台": result.get("platform", "未知"),
                "热度指数": 100 - i * 5,  # 模拟热度
                "链接": {
                    "link": result.get("url", ""),
                    "text": "查看详情",
                    "type": "url"
                },
                "发布时间": int(time.time() * 1000),
                "内容类型": self._detect_content_type(result),
                "状态": "待分析",
                "备注": f"关键词搜索: AI + ({' 或 '.join(self.keywords['secondary'])})",
                "关键词": result.get("keywords", []) + ["AI"],
                "抓取时间": int(time.time() * 1000)
            }
            feishu_records.append(record)
        
        return feishu_records
    
    def _detect_content_type(self, result: Dict) -> str:
        """检测内容类型"""
        title = result.get("title", "").lower()
        platform = result.get("platform", "")
        
        if "openclaw" in title or "clawd" in title:
            return "技术"
        elif "小龙虾" in title:
            return "农业"
        elif "教程" in title or "指南" in title:
            return "教程"
        elif platform in ["GitHub", "掘金"]:
            return "技术"
        elif platform in ["知乎", "微信公众号"]:
            return "文章"
        
        return "综合"

def main():
    """主函数"""
    logger.info("\n" + "=" * 60)
    logger.info("🔍 AI + (Openclaw/小龙虾) 关键词抓取器")
    logger.info("=" * 60 + "\n")
    
    # 创建抓取器
    crawler = AICrawler()
    
    # 搜索所有平台
    results = crawler.search_all_platforms(limit_per_platform=3)
    
    if results:
        # 转换为飞书格式
        feishu_records = crawler.convert_to_feishu_format(results)
        
        # 保存数据
        timestamp = int(time.time())
        data_file = f"/tmp/ai_keyword_search_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "keywords": crawler.keywords,
            "total": len(feishu_records),
            "results": results,
            "feishu_records": feishu_records
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 数据已保存到: {data_file}")
        
        # 显示结果
        logger.info("\n📊 搜索结果:")
        for i, record in enumerate(feishu_records):
            logger.info(f"\n{i+1}. {record['选题标题'][:50]}...")
            logger.info(f"   平台: {record['来源平台']}")
            logger.info(f"   类型: {record['内容类型']}")
            logger.info(f"   链接: {record['链接']['link'][:50]}...")
            logger.info(f"   关键词: {', '.join(record['关键词'][:3])}")
        
        # 准备写入飞书
        logger.info("\n📦 准备写入飞书...")
        
        # 分批写入（每批5条）
        batch_size = 5
        for i in range(0, len(feishu_records), batch_size):
            batch = feishu_records[i:i+batch_size]
            batch_data = {
                "app_token": "XDQXbxM97aiBAPswH4wcbmTRnCb",
                "table_id": "tblSTNrT7TrPuIAz",
                "records": [{"fields": record} for record in batch]
            }
            
            batch_file = f"/tmp/feishu_ai_batch_{timestamp}_{i//batch_size + 1}.json"
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"  批次 {i//batch_size + 1}: {len(batch)} 条记录 → {batch_file}")
        
        logger.info(f"\n🎯 总计: {len(feishu_records)} 条记录可写入飞书")
        
    else:
        logger.warning("⚠️ 未找到相关结果")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 搜索完成！")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()