#!/usr/bin/env python3
"""
微信公众号热榜抓取器 - 基于今日热榜公开接口
"""

import json
import time
import re
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

class WechatHotFetcher:
    """微信公众号热榜抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def fetch_wechat_hot(self, limit: int = 10) -> List[Dict]:
        """抓取微信公众号热榜"""
        logger.info("抓取微信公众号热榜...")
        
        topics = []
        
        try:
            # 今日热榜微信公众号页面
            url = "https://tophub.today/n/WnBe01o371"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # 解析HTML获取文章数据
                # 今日热榜页面结构：<a href="链接">标题</a> 热度
                pattern = r'<a[^>]*href="(https://mp\.weixin\.qq\.com/[^"]*)"[^>]*>([^<]+)</a>\s*([\d\.万]+)'
                matches = re.findall(pattern, html)
                
                for i, (link, title, hotness_str) in enumerate(matches[:limit]):
                    # 清理数据
                    title = title.strip()
                    hotness = self._parse_hotness(hotness_str)
                    
                    topics.append({
                        "选题标题": title,
                        "来源平台": "微信公众号",
                        "热度指数": hotness,
                        "链接": {
                            "link": link,
                            "text": "查看文章",
                            "type": "url"
                        },
                        "发布时间": int(time.time() * 1000),
                        "内容类型": self._detect_category(title),
                        "状态": "待分析",
                        "备注": "微信公众号热榜（今日热榜）",
                        "关键词": self._extract_keywords(title)
                    })
        
        except Exception as e:
            logger.error(f"❌ 微信公众号热榜抓取失败: {e}")
        
        logger.info(f"✅ 微信公众号热榜: {len(topics)} 条")
        return topics
    
    def fetch_wechat_category_hot(self, category: str = "科技", limit: int = 5) -> List[Dict]:
        """抓取微信公众号分类热榜"""
        logger.info(f"抓取微信公众号{category}热榜...")
        
        # 分类对应的hashid
        category_map = {
            "科技": "5PdMaaadmg",      # 微信科技24h热文榜
            "财经": "Ywv4BJRePa",      # 微信财经24h热文榜
            "生活": "nBe0xxje37",      # 微信生活24h热文榜
            "娱乐": "6YoVqqGeZa",      # 微信娱乐24h热文榜
            "健康": "Q0orrr0o8B",      # 微信健康24h热文榜
            "教育": "MZd7BVYvrO",      # 微信教育24h热文榜
            "职场": "DOvn33ydEB",      # 微信职场24h热文榜
            "美食": "m4ejxxyvxE",      # 微信美食24h热文榜
            "旅行": "qndgqqLoLl",      # 微信旅行24h热文榜
            "时尚": "b0vmYYWvB1",      # 微信时尚24h热文榜
        }
        
        hashid = category_map.get(category, "WnBe01o371")  # 默认综合热榜
        
        topics = []
        
        try:
            url = f"https://tophub.today/n/{hashid}"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # 解析HTML
                pattern = r'<a[^>]*href="(https://mp\.weixin\.qq\.com/[^"]*)"[^>]*>([^<]+)</a>\s*([\d\.万]+)'
                matches = re.findall(pattern, html)
                
                for i, (link, title, hotness_str) in enumerate(matches[:limit]):
                    title = title.strip()
                    hotness = self._parse_hotness(hotness_str)
                    
                    topics.append({
                        "选题标题": title,
                        "来源平台": f"微信公众号({category})",
                        "热度指数": hotness,
                        "链接": {
                            "link": link,
                            "text": "查看文章",
                            "type": "url"
                        },
                        "发布时间": int(time.time() * 1000),
                        "内容类型": category,
                        "状态": "待分析",
                        "备注": f"微信公众号{category}热榜",
                        "关键词": [category, "微信公众号", "热榜"]
                    })
        
        except Exception as e:
            logger.error(f"❌ 微信公众号{category}热榜抓取失败: {e}")
        
        logger.info(f"✅ 微信公众号{category}热榜: {len(topics)} 条")
        return topics
    
    def _parse_hotness(self, hotness_str: str) -> int:
        """解析热度值"""
        try:
            hotness_str = str(hotness_str).strip()
            
            if "万" in hotness_str:
                # 示例: "10.0万" -> 100000
                num_str = hotness_str.replace("万", "").strip()
                num = float(num_str)
                return int(num * 10000)
            elif "." in hotness_str:
                # 示例: "5.3" -> 5
                return int(float(hotness_str))
            else:
                # 示例: "1000" -> 1000
                return int(hotness_str)
        except:
            # 默认热度值
            return 10000
    
    def _detect_category(self, title: str) -> str:
        """检测内容类型"""
        category_keywords = {
            "科技": ["科技", "AI", "人工智能", "互联网", "数码", "手机", "电脑", "软件", "硬件"],
            "财经": ["财经", "经济", "股票", "投资", "金融", "货币", "汇率", "银行", "证券"],
            "生活": ["生活", "健康", "养生", "习惯", "日常", "睡眠", "饮食", "家居", "家庭"],
            "娱乐": ["娱乐", "明星", "影视", "音乐", "综艺", "演唱会", "电影", "电视剧", "歌手"],
            "时事": ["新闻", "政策", "通知", "公告", "政府", "国家", "国际", "政治", "外交"],
            "教育": ["教育", "学习", "学校", "考试", "培训", "学生", "老师", "课程", "教材"],
            "健康": ["健康", "医疗", "医生", "医院", "疾病", "疫苗", "养生", "保健", "体检"],
            "汽车": ["汽车", "车型", "驾驶", "新能源", "电动车", "特斯拉", "宝马", "奔驰", "奥迪"],
            "房产": ["房产", "房价", "楼市", "房地产", "买房", "租房", "房贷", "装修", "物业"],
            "旅游": ["旅游", "旅行", "景点", "酒店", "机票", "度假", "景区", "民宿", "攻略"]
        }
        
        title_lower = title.lower()
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword.lower() in title_lower:
                    return category
        
        return "综合"
    
    def _extract_keywords(self, title: str) -> List[str]:
        """提取关键词"""
        keywords = ["微信公众号", "热榜"]
        
        # 简单分词（按空格和标点）
        import re
        words = re.findall(r'[\u4e00-\u9fff\w]{2,}', title)
        
        for word in words[:5]:  # 取前5个词作为关键词
            if word not in keywords:
                keywords.append(word)
        
        return keywords[:7]  # 最多7个关键词

def main():
    """主函数"""
    logger.info("\n" + "=" * 60)
    logger.info("🚀 微信公众号热榜抓取器")
    logger.info("基于今日热榜公开接口，无需API密钥")
    logger.info("=" * 60 + "\n")
    
    # 创建抓取器
    fetcher = WechatHotFetcher()
    
    # 抓取综合热榜
    logger.info("【阶段1】抓取微信公众号综合热榜...")
    general_topics = fetcher.fetch_wechat_hot(limit=5)
    
    # 抓取分类热榜
    logger.info("\n【阶段2】抓取微信公众号分类热榜...")
    category_topics = []
    
    categories = ["科技", "财经", "生活", "娱乐", "健康"]
    for category in categories:
        topics = fetcher.fetch_wechat_category_hot(category, limit=2)
        category_topics.extend(topics)
    
    # 合并所有数据
    all_topics = general_topics + category_topics
    
    # 统计
    logger.info("\n" + "=" * 60)
    logger.info(f"🎉 抓取完成！总计: {len(all_topics)} 条记录")
    logger.info("=" * 60)
    
    # 按平台统计
    platform_stats = {}
    for topic in all_topics:
        platform = topic["来源平台"]
        platform_stats[platform] = platform_stats.get(platform, 0) + 1
    
    logger.info("\n📊 平台分布:")
    for platform, count in platform_stats.items():
        logger.info(f"  • {platform}: {count} 条")
    
    # 保存数据
    if all_topics:
        timestamp = int(time.time())
        data_file = f"/tmp/wechat_hot_topics_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "total": len(all_topics),
            "source": "微信公众号热榜抓取器（今日热榜）",
            "topics": all_topics
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n💾 数据已保存到: {data_file}")
        
        # 准备飞书批次
        batches = []
        batch_size = 5
        
        for i in range(0, len(all_topics), batch_size):
            batch = all_topics[i:i+batch_size]
            batch_data = {
                "app_token": "XDQXbxM97aiBAPswH4wcbmTRnCb",
                "table_id": "tblSTNrT7TrPuIAz",
                "records": [{"fields": topic} for topic in batch]
            }
            
            batch_file = f"/tmp/feishu_wechat_batch_{i//batch_size + 1}.json"
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=2)
            
            batches.append(batch_file)
        
        logger.info(f"\n📦 已准备 {len(batches)} 个批次写入飞书")
        for i, batch_file in enumerate(batches):
            logger.info(f"  批次 {i+1}: {batch_file}")
        
        # 生成报告
        report = {
            "timestamp": timestamp,
            "total_topics": len(all_topics),
            "data_file": data_file,
            "batch_files": batches,
            "platform_stats": platform_stats,
            "method": "今日热榜公开接口",
            "note": "无需API密钥，适合个人使用",
            "advantages": [
                "无需注册",
                "无需API密钥",
                "实时数据",
                "多分类支持"
            ]
        }
        
        report_file = f"/var/log/topic_fetch/wechat_fetch_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n📄 报告文件: {report_file}")
        
        # 显示示例数据
        logger.info("\n📝 示例数据:")
        for i, topic in enumerate(all_topics[:3]):
            logger.info(f"  {i+1}. {topic['选题标题'][:40]}...")
            logger.info(f"     来源: {topic['来源平台']}, 热度: {topic['热度指数']}")
            logger.info(f"     类型: {topic['内容类型']}")
            logger.info(f"     链接: {topic['链接']['link'][:50]}...")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 抓取完成！")
    logger.info("=" * 60)
    
    # 建议
    logger.info("\n🎯 建议:")
    logger.info("1. 可以注册今日热榜获取API密钥，获得更稳定、更完整的数据")
    logger.info("2. 将微信公众号热榜集成到现有抓取系统")
    logger.info("3. 注意抓取频率，避免对目标网站造成压力")
    logger.info("4. 定期检查数据质量，优化解析规则")

if __name__ == "__main__":
    main()