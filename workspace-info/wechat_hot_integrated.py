#!/usr/bin/env python3
"""
微信公众号热榜抓取器 - 集成版本
可以直接集成到现有选题库抓取系统
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

class WechatHotFetcherIntegrated:
    """微信公众号热榜抓取器（集成版）"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def fetch_wechat_hot(self, limit: int = 10) -> List[Dict]:
        """抓取微信公众号热榜（集成到现有系统）"""
        logger.info("抓取微信公众号热榜...")
        
        topics = []
        
        try:
            # 今日热榜微信公众号页面
            url = "https://tophub.today/n/WnBe01o371"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # 使用行模式匹配
                row_pattern = r'<td><a[^>]*href="(https://mp\.weixin\.qq\.com/[^"]*)"[^>]*>([^<]+)</a></td>\s*<td[^>]*>([\d\.万]+)</td>'
                row_matches = re.findall(row_pattern, html)
                
                logger.info(f"找到 {len(row_matches)} 条微信公众号热榜记录")
                
                for i, (link, title, hotness_str) in enumerate(row_matches[:limit]):
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
                        "关键词": self._extract_keywords(title),
                        "抓取时间": int(time.time() * 1000)
                    })
        
        except Exception as e:
            logger.error(f"❌ 微信公众号热榜抓取失败: {e}")
        
        logger.info(f"✅ 微信公众号热榜: {len(topics)} 条")
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

def write_to_feishu(topics: List[Dict], app_token: str, table_id: str, batch_size: int = 5):
    """将数据写入飞书多维表格"""
    if not topics:
        logger.warning("⚠️ 没有数据可写入飞书")
        return
    
    logger.info(f"准备写入 {len(topics)} 条数据到飞书")
    
    # 分批写入
    for i in range(0, len(topics), batch_size):
        batch = topics[i:i+batch_size]
        records = [{"fields": topic} for topic in batch]
        
        try:
            # 这里需要调用飞书API
            # 实际使用时需要替换为实际的API调用
            logger.info(f"📦 批次 {i//batch_size + 1}: {len(batch)} 条记录")
            
            # 示例：生成飞书批次文件
            batch_data = {
                "app_token": app_token,
                "table_id": table_id,
                "records": records
            }
            
            batch_file = f"/tmp/feishu_wechat_batch_{int(time.time())}_{i//batch_size + 1}.json"
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 批次文件: {batch_file}")
            
        except Exception as e:
            logger.error(f"❌ 写入飞书失败（批次 {i//batch_size + 1}）: {e}")

def main():
    """主函数"""
    logger.info("\n" + "=" * 60)
    logger.info("🚀 微信公众号热榜抓取器（集成版）")
    logger.info("=" * 60 + "\n")
    
    # 创建抓取器
    fetcher = WechatHotFetcherIntegrated()
    
    # 抓取数据
    topics = fetcher.fetch_wechat_hot(limit=10)
    
    if topics:
        # 保存数据
        timestamp = int(time.time())
        data_file = f"/tmp/wechat_hot_integrated_{timestamp}.json"
        
        data = {
            "timestamp": timestamp,
            "total": len(topics),
            "source": "微信公众号热榜抓取器（集成版）",
            "topics": topics
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 数据已保存到: {data_file}")
        
        # 显示示例
        logger.info("\n📝 示例数据:")
        for i, topic in enumerate(topics[:3]):
            logger.info(f"  {i+1}. {topic['选题标题'][:40]}...")
            logger.info(f"     来源: {topic['来源平台']}, 热度: {topic['热度指数']}")
            logger.info(f"     类型: {topic['内容类型']}")
            logger.info(f"     链接: {topic['链接']['link'][:50]}...")
        
        # 写入飞书（示例配置）
        # write_to_feishu(topics, "XDQXbxM97aiBAPswH4wcbmTRnCb", "tblSTNrT7TrPuIAz")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 抓取完成！")
    logger.info("=" * 60)
    
    # 集成建议
    logger.info("\n🎯 集成到现有系统的建议:")
    logger.info("1. 将此类添加到现有抓取器类中")
    logger.info("2. 在 `fetch_all_topics()` 方法中调用 `fetch_wechat_hot()`")
    logger.info("3. 配置飞书写入参数（app_token, table_id）")
    logger.info("4. 添加到定时任务（如每小时抓取一次）")

if __name__ == "__main__":
    main()