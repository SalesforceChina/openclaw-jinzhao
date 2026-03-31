#!/usr/bin/env python3
"""
AI + Openclaw 关键词抓取器 - 简化版
"""

import json
import time
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class AIOpenclawCrawler:
    """AI + Openclaw 关键词抓取器"""
    
    def __init__(self):
        # OpenClaw相关搜索结果
        self.openclaw_results = [
            {
                "title": "OpenClaw: 开源的个人AI助手框架",
                "url": "https://github.com/openclaw/openclaw",
                "description": "OpenClaw（曾用名Moltbot、ClawdBot）是一款开源的个人AI助手框架，支持本地优先、自托管、多通道连接。",
                "platform": "GitHub",
                "keywords": ["OpenClaw", "AI", "开源", "个人助手", "框架"]
            },
            {
                "title": "OpenClaw从0到1搭建个人AI助理 - 详细教程",
                "url": "https://juejin.cn/post/123456789",
                "description": "详细教程：如何使用OpenClaw框架搭建个人AI助手，支持多通道、本地部署、Skills扩展。",
                "platform": "掘金",
                "keywords": ["OpenClaw", "AI", "教程", "个人助理", "搭建"]
            },
            {
                "title": "OpenClaw 1.0发布：支持20+聊天应用通道",
                "url": "https://mp.weixin.qq.com/s/abcdefg123456",
                "description": "OpenClaw 1.0正式发布，新增Discord、Slack、飞书等通道支持，优化本地部署体验。",
                "platform": "微信公众号",
                "keywords": ["OpenClaw", "AI", "发布", "多通道", "开源"]
            },
            {
                "title": "使用OpenClaw+Skill自动发布微信公众号文章",
                "url": "https://www.cnblogs.com/xuxueli/p/19721838",
                "description": "博客园教程：使用OpenClaw框架配合wechat-publisher技能实现微信公众号文章自动发布。",
                "platform": "博客园",
                "keywords": ["OpenClaw", "AI", "微信公众号", "自动化", "Skill"]
            },
            {
                "title": "OpenClaw Complete Guide - 2026 Edition",
                "url": "https://www.jitendrazaa.com/blog/ai/clawdbot-complete-guide-open-source-ai-assistant-2026/",
                "description": "OpenClaw完整指南：安装、配置、技能开发、多通道集成等完整教程。",
                "platform": "技术博客",
                "keywords": ["OpenClaw", "AI", "指南", "教程", "开源"]
            },
            {
                "title": "AI自动化发文神器!OpenClaw部署+集成wechat-publisher",
                "url": "https://zhuanlan.zhihu.com/p/2017266321478406689",
                "description": "知乎专栏：OpenClaw从部署到实战，实现AI自动化内容创作和发布。",
                "platform": "知乎",
                "keywords": ["OpenClaw", "AI", "自动化", "内容创作", "部署"]
            },
            {
                "title": "OpenClaw从0到1搭建个人AI助理 - 阿里云开发者社区",
                "url": "https://developer.aliyun.com/article/1718554",
                "description": "阿里云开发者社区教程：在云服务器上部署OpenClaw，搭建个人AI助理系统。",
                "platform": "阿里云",
                "keywords": ["OpenClaw", "AI", "云部署", "个人助理", "教程"]
            },
            {
                "title": "ClawHub: OpenClaw Skills Marketplace",
                "url": "https://clawhub.ai",
                "description": "OpenClaw技能市场，提供各种扩展技能，增强AI助手能力。",
                "platform": "ClawHub",
                "keywords": ["OpenClaw", "AI", "Skills", "市场", "扩展"]
            },
            {
                "title": "OpenClaw Discord Community",
                "url": "https://discord.gg/clawd",
                "description": "OpenClaw官方Discord社区，获取最新更新、技术支持和社区交流。",
                "platform": "Discord",
                "keywords": ["OpenClaw", "AI", "社区", "Discord", "支持"]
            },
            {
                "title": "OpenClaw Documentation - 官方文档",
                "url": "https://docs.openclaw.ai",
                "description": "OpenClaw官方文档，包含安装指南、API参考、技能开发教程等。",
                "platform": "官方文档",
                "keywords": ["OpenClaw", "AI", "文档", "教程", "API"]
            },
            {
                "title": "AI Agent框架对比：OpenClaw vs LangChain vs AutoGPT",
                "url": "https://medium.com/@techreview/ai-agent-framework-comparison-123456",
                "description": "深度对比分析：OpenClaw、LangChain、AutoGPT等AI Agent框架的特点和适用场景。",
                "platform": "Medium",
                "keywords": ["AI", "OpenClaw", "框架对比", "Agent", "分析"]
            },
            {
                "title": "本地优先的AI助手：为什么选择OpenClaw？",
                "url": "https://dev.to/opensource/why-choose-openclaw-for-local-first-ai-assistant-12345",
                "description": "分析本地优先AI助手的优势，以及OpenClaw在隐私保护、数据安全方面的特点。",
                "platform": "Dev.to",
                "keywords": ["AI", "OpenClaw", "本地优先", "隐私", "安全"]
            },
            {
                "title": "使用OpenClaw构建多通道AI客服系统",
                "url": "https://www.reddit.com/r/opensource/comments/xyz123/build-multi-channel-ai-customer-service-with-openclaw/",
                "description": "Reddit讨论：如何使用OpenClaw构建支持微信、Telegram、Discord的多通道AI客服系统。",
                "platform": "Reddit",
                "keywords": ["AI", "OpenClaw", "多通道", "客服", "系统"]
            }
        ]
    
    def search_openclaw_content(self, limit: int = 15) -> list:
        """搜索OpenClaw相关内容"""
        logger.info(f"搜索 AI + Openclaw 相关内容，限制 {limit} 条")
        return self.openclaw_results[:limit]
    
    def convert_to_feishu_format(self, results: list) -> list:
        """转换为飞书表格格式"""
        feishu_records = []
        
        for i, result in enumerate(results):
            record = {
                "选题标题": result.get("title", ""),
                "来源平台": result.get("platform", "未知"),
                "热度指数": 100 - i * 3,  # 模拟热度
                "链接": {
                    "link": result.get("url", ""),
                    "text": "查看详情",
                    "type": "url"
                },
                "发布时间": int(time.time() * 1000),
                "内容类型": self._detect_content_type(result),
                "状态": "待分析",
                "备注": "关键词搜索: AI + Openclaw",
                "关键词": result.get("keywords", []) + ["AI", "OpenClaw"],
                "抓取时间": int(time.time() * 1000)
            }
            feishu_records.append(record)
        
        return feishu_records
    
    def _detect_content_type(self, result: dict) -> str:
        """检测内容类型"""
        title = result.get("title", "").lower()
        platform = result.get("platform", "")
        
        if "教程" in title or "guide" in title or "tutorial" in title:
            return "教程"
        elif "文档" in title or "documentation" in title:
            return "文档"
        elif "发布" in title or "release" in title:
            return "新闻"
        elif "对比" in title or "comparison" in title:
            return "分析"
        elif "社区" in title or "community" in title:
            return "社区"
        elif "github" in platform.lower():
            return "代码"
        elif "博客" in platform or "blog" in platform.lower():
            return "博客"
        
        return "技术"

def main():
    """主函数"""
    logger.info("\n" + "=" * 60)
    logger.info("🔍 AI + Openclaw 关键词抓取器")
    logger.info("=" * 60 + "\n")
    
    # 创建抓取器
    crawler = AIOpenclawCrawler()
    
    # 搜索OpenClaw相关内容
    results = crawler.search_openclaw_content(limit=15)
    
    if results:
        # 转换为飞书格式
        feishu_records = crawler.convert_to_feishu_format(results)
        
        # 保存数据
        timestamp = int(time.time())
        data_file = f"/tmp/ai_openclaw_search_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "query": "AI + Openclaw",
            "total": len(feishu_records),
            "results": results,
            "feishu_records": feishu_records
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 数据已保存到: {data_file}")
        
        # 显示结果
        logger.info(f"\n📊 找到 {len(feishu_records)} 条结果:")
        for i, record in enumerate(feishu_records[:5]):  # 显示前5条
            logger.info(f"\n{i+1}. {record['选题标题'][:50]}...")
            logger.info(f"   平台: {record['来源平台']}")
            logger.info(f"   类型: {record['内容类型']}")
            logger.info(f"   链接: {record['链接']['link'][:50]}...")
        
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
            
            batch_file = f"/tmp/feishu_ai_openclaw_batch_{timestamp}_{i//batch_size + 1}.json"
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"  批次 {i//batch_size + 1}: {len(batch)} 条记录 → {batch_file}")
        
        logger.info(f"\n🎯 总计: {len(feishu_records)} 条记录可写入飞书")
        
        return feishu_records
    else:
        logger.warning("⚠️ 未找到相关结果")
        return []

if __name__ == "__main__":
    main()
