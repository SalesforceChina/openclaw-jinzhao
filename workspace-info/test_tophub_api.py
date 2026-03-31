#!/usr/bin/env python3
"""
测试今日热榜API - 微信公众号热榜
使用公开接口，无需API密钥
"""

import requests
import json
import time
import logging
from typing import List, Dict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class TophubPublicFetcher:
    """今日热榜公开接口抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def fetch_wechat_hot_public(self, limit: int = 10) -> List[Dict]:
        """使用公开接口抓取微信公众号热榜"""
        logger.info("抓取微信公众号热榜（公开接口）...")
        
        topics = []
        
        try:
            # 今日热榜公开接口（无需API密钥）
            # 微信公众号热榜页面
            url = "https://tophub.today/n/WnBe01o371"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # 解析HTML获取数据
                # 注意：这里使用简单的正则解析，实际生产环境应该用BeautifulSoup
                import re
                
                # 查找文章条目
                # 模式：<a href="链接">标题</a> 热度
                pattern = r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>\s*([\d\.万]+)'
                matches = re.findall(pattern, html)
                
                for i, (link, title, hotness_str) in enumerate(matches[:limit]):
                    # 清理标题
                    title = title.strip()
                    
                    # 解析热度
                    hotness = self._parse_hotness(hotness_str)
                    
                    # 确保链接完整
                    if link and not link.startswith("http"):
                        link = f"https:{link}" if link.startswith("//") else link
                    
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
                        "备注": "微信公众号热榜（今日热榜公开接口）",
                        "关键词": self._extract_keywords(title)
                    })
        
        except Exception as e:
            logger.error(f"❌ 微信公众号热榜抓取失败: {e}")
        
        logger.info(f"✅ 微信公众号热榜: {len(topics)} 条")
        return topics
    
    def fetch_wechat_hot_via_api(self, limit: int = 10) -> List[Dict]:
        """尝试使用API接口（需要API密钥）"""
        logger.info("尝试使用API接口抓取微信公众号热榜...")
        
        topics = []
        
        try:
            # 这里可以替换为实际的API密钥
            # API_KEY = "YOUR_API_KEY_HERE"
            
            # 如果没有API密钥，返回空列表
            logger.warning("⚠️ 未配置API密钥，跳过API接口")
            return topics
            
            # 如果有API密钥，使用以下代码
            """
            headers = {"Authorization": API_KEY}
            response = self.session.get(
                "https://api.tophubdata.com/nodes/WnBe01o371",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get("error"):
                    items = data["data"].get("items", [])
                    
                    for i, item in enumerate(items[:limit]):
                        title = item.get("title", "")
                        url = item.get("url", "")
                        extra = item.get("extra", "0")
                        
                        hotness = self._parse_hotness(extra)
                        
                        topics.append({
                            "选题标题": title,
                            "来源平台": "微信公众号",
                            "热度指数": hotness,
                            "链接": {
                                "link": url,
                                "text": "查看文章",
                                "type": "url"
                            },
                            "发布时间": int(time.time() * 1000),
                            "内容类型": self._detect_category(title),
                            "状态": "待分析",
                            "备注": "微信公众号热榜（今日热榜API）",
                            "关键词": self._extract_keywords(title)
                        })
            """
        
        except Exception as e:
            logger.error(f"❌ API接口抓取失败: {e}")
        
        return topics
    
    def _parse_hotness(self, hotness_str: str) -> int:
        """解析热度值"""
        try:
            # 示例: "10.0万" -> 100000, "5.3万" -> 53000
            hotness_str = str(hotness_str).strip()
            
            if "万" in hotness_str:
                num_str = hotness_str.replace("万", "").strip()
                num = float(num_str)
                return int(num * 10000)
            elif "." in hotness_str:
                return int(float(hotness_str))
            else:
                return int(hotness_str)
        except:
            return 10000  # 默认值
    
    def _detect_category(self, title: str) -> str:
        """检测内容类型"""
        categories = {
            "科技": ["科技", "AI", "人工智能", "互联网", "数码", "手机", "电脑"],
            "财经": ["财经", "经济", "股票", "投资", "金融", "货币", "汇率"],
            "生活": ["生活", "健康", "养生", "习惯", "日常", "睡眠", "饮食"],
            "娱乐": ["娱乐", "明星", "影视", "音乐", "综艺", "演唱会", "电影"],
            "时事": ["新闻", "政策", "通知", "公告", "政府", "国家", "国际"],
            "教育": ["教育", "学习", "学校", "考试", "培训", "学生", "老师"],
            "健康": ["健康", "医疗", "医生", "医院", "疾病", "疫苗", "养生"],
            "汽车": ["汽车", "车型", "驾驶", "新能源", "电动车", "特斯拉"],
            "房产": ["房产", "房价", "楼市", "房地产", "买房", "租房"],
            "旅游": ["旅游", "旅行", "景点", "酒店", "机票", "度假"]
        }
        
        title_lower = title.lower()
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in title_lower:
                    return category
        
        return "综合"
    
    def _extract_keywords(self, title: str) -> List[str]:
        """提取关键词"""
        keywords = ["微信公众号", "热榜"]
        
        # 添加标题中的关键词
        import jieba
        try:
            words = jieba.lcut(title)
            for word in words:
                if len(word) > 1 and word not in keywords:
                    keywords.append(word)
                    if len(keywords) >= 7:  # 最多7个关键词
                        break
        except:
            # 如果jieba不可用，使用简单分词
            words = title.split()
            for word in words[:5]:
                if len(word) > 1:
                    keywords.append(word)
        
        return keywords[:7]

def main():
    """主函数"""
    logger.info("\n" + "=" * 60)
    logger.info("🔍 测试今日热榜API - 微信公众号热榜")
    logger.info("=" * 60 + "\n")
    
    # 创建抓取器
    fetcher = TophubPublicFetcher()
    
    # 方法1: 使用公开接口
    logger.info("【方法1】使用公开接口抓取...")
    topics_public = fetcher.fetch_wechat_hot_public(limit=5)
    
    # 方法2: 使用API接口（需要API密钥）
    logger.info("\n【方法2】使用API接口抓取...")
    topics_api = fetcher.fetch_wechat_hot_via_api(limit=5)
    
    # 合并结果
    all_topics = topics_public + topics_api
    
    # 显示结果
    logger.info("\n" + "=" * 60)
    logger.info(f"📊 抓取结果: {len(all_topics)} 条记录")
    logger.info("=" * 60)
    
    if all_topics:
        for i, topic in enumerate(all_topics):
            logger.info(f"\n{i+1}. {topic['选题标题'][:40]}...")
            logger.info(f"   平台: {topic['来源平台']}")
            logger.info(f"   热度: {topic['热度指数']}")
            logger.info(f"   类型: {topic['内容类型']}")
            logger.info(f"   链接: {topic['链接']['link'][:50]}...")
            logger.info(f"   关键词: {', '.join(topic['关键词'][:3])}")
    else:
        logger.warning("⚠️ 未抓取到任何数据")
    
    # 保存数据
    if all_topics:
        timestamp = int(time.time())
        data_file = f"/tmp/wechat_topics_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "total": len(all_topics),
            "source": "今日热榜（公开接口）",
            "topics": all_topics
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n💾 数据已保存到: {data_file}")
        
        # 准备飞书批次
        batch_data = {
            "app_token": "XDQXbxM97aiBAPswH4wcbmTRnCb",
            "table_id": "tblSTNrT7TrPuIAz",
            "records": [{"fields": topic} for topic in all_topics]
        }
        
        batch_file = f"/tmp/feishu_wechat_batch_{timestamp}.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📦 飞书批次文件: {batch_file}")
    
    # 建议
    logger.info("\n" + "=" * 60)
    logger.info("🎯 建议:")
    logger.info("1. 注册今日热榜获取API密钥: https://www.tophubdata.com/register")
    logger.info("2. 使用API接口获取更稳定、更完整的数据")
    logger.info("3. 将微信公众号热榜集成到现有抓取系统")
    logger.info("4. 注意API调用频率限制")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()