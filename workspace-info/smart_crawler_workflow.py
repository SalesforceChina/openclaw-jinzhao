#!/usr/bin/env python3
"""
智能抓取工作流 - 带确认和验证
"""

import json
import requests
import time
from typing import List, Dict, Optional

class SmartCrawlerWorkflow:
    """智能抓取工作流"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def confirm_before_crawl(self, keywords: List[str], platforms: List[str], 
                            count_per_platform: int, time_range: str) -> Dict:
        """
        抓取前确认
        
        Args:
            keywords: 关键词列表，如 ["AI", "OpenClaw"]
            platforms: 平台列表，如 ["36氪", "知乎热榜"]
            count_per_platform: 每个平台抓取数量
            time_range: 时间范围，如 "7d"（7天）
        
        Returns:
            确认信息字典
        """
        keyword_str = " + ".join(keywords)
        platform_str = "、".join(platforms)
        
        confirmation = {
            "keywords": keywords,
            "keyword_str": keyword_str,
            "platforms": platforms,
            "platform_str": platform_str,
            "count_per_platform": count_per_platform,
            "time_range": time_range,
            "estimated_total": len(platforms) * count_per_platform
        }
        
        return confirmation
    
    def format_confirmation_message(self, confirmation: Dict) -> str:
        """格式化确认消息"""
        message = f"""
🕵️ 准备抓取，请确认：

📌 关键词：{confirmation['keyword_str']}
📱 平台：{confirmation['platform_str']}
📊 数量：每个平台 {confirmation['count_per_platform']} 条
⏰ 时间范围：最近 {confirmation['time_range']}
📈 预计抓取：约 {confirmation['estimated_total']} 条

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请回复以下选项：
- "确认" - 开始抓取
- "修改" - 调整参数
- "取消" - 取消本次抓取
"""
        return message
    
    def validate_relevance(self, item: Dict, keywords: List[str]) -> Dict:
        """
        验证内容相关性
        
        Args:
            item: 单条内容记录
            keywords: 关键词列表
        
        Returns:
            验证结果 {is_relevant: bool, score: float, reasons: List[str]}
        """
        title = item.get('title', '').lower()
        content = item.get('content', '').lower()
        
        score = 0.0
        reasons = []
        
        # 检查标题中的关键词
        keyword_matches = 0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in title:
                keyword_matches += 1
                score += 30  # 标题匹配权重高
                reasons.append(f"标题包含'{keyword}'")
            elif keyword_lower in content:
                score += 10  # 内容匹配权重较低
                reasons.append(f"内容包含'{keyword}'")
        
        # 相关性评分
        if keyword_matches == len(keywords):
            score += 20  # 所有关键词都匹配
            reasons.append("完全匹配所有关键词")
        elif keyword_matches >= len(keywords) / 2:
            score += 10  # 部分关键词匹配
            reasons.append(f"匹配{keyword_matches}/{len(keywords)}个关键词")
        
        is_relevant = score >= 40  # 相关性阈值
        
        return {
            "is_relevant": is_relevant,
            "score": score,
            "reasons": reasons
        }
    
    def validate_link(self, url: str) -> Dict:
        """
        验证链接有效性
        
        Args:
            url: 链接地址
        
        Returns:
            验证结果 {is_valid: bool, status_code: int, error: str}
        """
        try:
            response = self.session.head(url, timeout=5, allow_redirects=True)
            return {
                "is_valid": response.status_code == 200,
                "status_code": response.status_code,
                "error": None
            }
        except Exception as e:
            return {
                "is_valid": False,
                "status_code": None,
                "error": str(e)
            }
    
    def validate_data_integrity(self, item: Dict) -> Dict:
        """
        验证数据完整性
        
        Args:
            item: 单条内容记录
        
        Returns:
            验证结果 {is_complete: bool, missing_fields: List[str]}
        """
        required_fields = ['title', 'link', 'platform', 'hotness']
        missing_fields = []
        
        for field in required_fields:
            if not item.get(field):
                missing_fields.append(field)
        
        # 检查关键词字段
        if not item.get('keywords') or len(item.get('keywords', [])) == 0:
            missing_fields.append('keywords')
        
        return {
            "is_complete": len(missing_fields) == 0,
            "missing_fields": missing_fields
        }
    
    def validate_batch(self, items: List[Dict], keywords: List[str]) -> Dict:
        """
        批量验证抓取结果
        
        Args:
            items: 抓取的内容列表
            keywords: 关键词列表
        
        Returns:
            验证报告
        """
        report = {
            "total": len(items),
            "relevant": 0,
            "irrelevant": 0,
            "valid_links": 0,
            "invalid_links": 0,
            "complete_data": 0,
            "incomplete_data": 0,
            "validated_items": [],
            "filtered_items": []
        }
        
        for item in items:
            # 相关性验证
            relevance = self.validate_relevance(item, keywords)
            
            # 链接验证（只验证相关内容）
            link_validation = {"is_valid": True, "status_code": 200}
            if relevance['is_relevant']:
                link_validation = self.validate_link(item.get('link', ''))
            
            # 数据完整性验证
            integrity = self.validate_data_integrity(item)
            
            # 统计
            if relevance['is_relevant']:
                report["relevant"] += 1
                if link_validation['is_valid']:
                    report["valid_links"] += 1
                else:
                    report["invalid_links"] += 1
                
                if integrity['is_complete']:
                    report["complete_data"] += 1
                else:
                    report["incomplete_data"] += 1
                
                # 添加到验证通过列表
                validated_item = item.copy()
                validated_item['validation'] = {
                    "relevance_score": relevance['score'],
                    "link_valid": link_validation['is_valid'],
                    "data_complete": integrity['is_complete']
                }
                report["validated_items"].append(validated_item)
            else:
                report["irrelevant"] += 1
                report["filtered_items"].append({
                    "title": item.get('title', ''),
                    "reason": f"相关性不足（评分: {relevance['score']}）"
                })
        
        return report
    
    def format_validation_report(self, report: Dict, keywords: List[str]) -> str:
        """格式化验证报告"""
        keyword_str = " + ".join(keywords)
        
        message = f"""
✅ 抓取完成 - 验证报告

📊 统计信息：
- 抓取总数：{report['total']} 条
- ✅ 相关内容：{report['relevant']} 条
- ❌ 无关内容：{report['irrelevant']} 条（已过滤）
- 🔗 有效链接：{report['valid_links']} 条
- ⚠️  失效链接：{report['invalid_links']} 条
- 📝 数据完整：{report['complete_data']} 条
- ⚠️  数据缺失：{report['incomplete_data']} 条

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 验证通过内容预览：
"""
        
        # 显示前5条验证通过的内容
        for i, item in enumerate(report['validated_items'][:5], 1):
            platform = item.get('platform', '')
            title = item.get('title', '')
            link = item.get('link', '')
            score = item['validation']['relevance_score']
            
            message += f"\n{i}. [{platform}] {title[:50]}... ✅\n"
            message += f"   链接：{link}\n"
            message += f"   相关性：{score}%\n"
        
        if len(report['validated_items']) > 5:
            message += f"\n... 还有 {len(report['validated_items']) - 5} 条\n"
        
        if report['filtered_items']:
            message += "\n❌ 已过滤内容：\n"
            for i, item in enumerate(report['filtered_items'][:3], 1):
                message += f"{i}. {item['title'][:50]}...\n"
                message += f"   原因：{item['reason']}\n"
        
        message += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 下一步操作：
- 回复"写入" - 将验证通过的内容写入飞书
- 回复"重试" - 重新抓取
- 回复"取消" - 放弃本次结果
"""
        
        return message


# 使用示例
if __name__ == "__main__":
    workflow = SmartCrawlerWorkflow()
    
    # 示例：抓取前确认
    keywords = ["AI", "OpenClaw"]
    platforms = ["36氪", "知乎热榜", "掘金"]
    count = 5
    time_range = "7d"
    
    confirmation = workflow.confirm_before_crawl(keywords, platforms, count, time_range)
    print(workflow.format_confirmation_message(confirmation))
    
    # 模拟抓取数据
    mock_items = [
        {
            "title": "AI驱动的OpenClaw框架发布",
            "content": "OpenClaw是一个AI驱动的开源框架",
            "link": "https://example.com/article1",
            "platform": "36氪",
            "hotness": 95,
            "keywords": ["AI", "OpenClaw", "框架"]
        },
        {
            "title": "如何使用OpenClaw进行AI开发",
            "content": "OpenClaw提供了强大的AI开发工具",
            "link": "https://example.com/article2",
            "platform": "知乎热榜",
            "hotness": 88,
            "keywords": ["OpenClaw", "AI", "开发"]
        },
        {
            "title": "今天天气真好",
            "content": "适合出去玩",
            "link": "https://example.com/article3",
            "platform": "掘金",
            "hotness": 50,
            "keywords": ["天气"]
        }
    ]
    
    # 验证抓取结果
    report = workflow.validate_batch(mock_items, keywords)
    print("\n" + workflow.format_validation_report(report, keywords))
