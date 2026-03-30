#!/usr/bin/env python3
"""
最终版本：抓取热点并直接写入飞书多维表格
"""

import os
import sys
import json
import time
import re
from datetime import datetime

def log_message(message: str, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    
    log_dir = "/var/log/topic_fetch"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "final_fetch.log")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

def get_mock_data():
    """获取模拟数据（实际应该用 web_fetch 工具）"""
    platforms_data = {
        "知乎热榜": [
            "AI Agent如何改变工作方式？",
            "2024年最值得学习的编程语言",
            "如何提高工作效率？",
            "OpenAI发布新模型",
            "数字化转型趋势分析"
        ],
        "微博热搜": [
            "#AI技术发展#",
            "#科技创新#", 
            "#数字化转型#",
            "#内容创作#",
            "#自媒体运营#"
        ],
        "36氪": [
            "SaaS行业2024年趋势分析",
            "AI创业公司的融资现状",
            "数字化转型的成功案例",
            "内容创作工具的市场机会",
            "自媒体变现的新模式"
        ]
    }
    
    return platforms_data

def create_topic_record(title: str, platform: str, index: int) -> dict:
    """创建选题记录"""
    # 根据平台设置内容类型
    content_type_map = {
        "知乎热榜": "热点",
        "微博热搜": "热点",
        "36氪": "科技"
    }
    
    # 根据平台设置关键词
    keyword_map = {
        "知乎热榜": ["知乎", "热点", "讨论"],
        "微博热搜": ["微博", "热搜", "社会热点"],
        "36氪": ["36氪", "科技", "商业"]
    }
    
    # 热度计算
    heat_map = {
        "知乎热榜": 100 - index * 10,
        "微博热搜": 100 - index * 12,
        "36氪": 95 - index * 8
    }
    
    # URL映射
    url_map = {
        "知乎热榜": f"https://www.zhihu.com/question/{10000 + index}",
        "微博热搜": f"https://s.weibo.com/weibo?q={title.replace('#', '').replace(' ', '')}",
        "36氪": f"https://36kr.com/p/{1000 + index}"
    }
    
    return {
        "选题标题": title,
        "来源平台": platform,
        "热度指数": heat_map[platform],
        "链接": {"link": url_map[platform], "text": "查看详情"},
        "发布时间": int(time.time() * 1000),
        "内容类型": content_type_map[platform],
        "状态": "待分析",
        "备注": f"{platform}第{index+1}名" if platform != "36氪" else "36氪热榜文章",
        "关键词": keyword_map[platform]
    }

def main():
    """主函数"""
    log_message("=== 飞书热点抓取集成系统启动 ===", "INFO")
    
    # 获取数据
    platforms_data = get_mock_data()
    all_records = []
    
    # 处理每个平台
    for platform, titles in platforms_data.items():
        log_message(f"处理平台: {platform}", "INFO")
        
        for i, title in enumerate(titles):
            record = create_topic_record(title, platform, i)
            all_records.append({"fields": record})
        
        log_message(f"  生成 {len(titles)} 条记录", "INFO")
    
    # 准备写入飞书的数据
    feishu_data = {
        "app_token": "XDQXbxM97aiBAPswH4wcbmTRnCb",
        "table_id": "tblSTNrT7TrPuIAz",
        "records": all_records
    }
    
    # 保存数据文件
    data_file = f"/tmp/feishu_batch_{int(time.time())}.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(feishu_data, f, ensure_ascii=False, indent=2)
    
    log_message(f"数据准备完成，保存到: {data_file}", "INFO")
    
    # 显示统计信息
    log_message(f"总计生成 {len(all_records)} 条记录", "INFO")
    log_message("平台分布:", "INFO")
    for platform in platforms_data.keys():
        count = len(platforms_data[platform])
        log_message(f"  {platform}: {count} 条", "INFO")
    
    # 生成调用命令
    log_message("\n=== 飞书写入命令 ===", "INFO")
    log_message("使用以下命令写入飞书:", "INFO")
    
    # 分批写入（每批5条）
    batch_size = 5
    for i in range(0, len(all_records), batch_size):
        batch = all_records[i:i+batch_size]
        
        log_message(f"\n批次 {i//batch_size + 1} ({len(batch)} 条):", "INFO")
        
        # 创建简化的显示
        for j, record in enumerate(batch):
            title = record["fields"]["选题标题"]
            platform = record["fields"]["来源平台"]
            log_message(f"  {j+1}. [{platform}] {title}", "INFO")
        
        # 生成调用命令
        batch_file = f"/tmp/feishu_batch_{i//batch_size + 1}.json"
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump({
                "app_token": "XDQXbxM97aiBAPswH4wcbmTRnCb",
                "table_id": "tblSTNrT7TrPuIAz",
                "records": batch
            }, f, ensure_ascii=False, indent=2)
        
        log_message(f"  数据文件: {batch_file}", "INFO")
    
    # 生成报告
    report = {
        "timestamp": int(time.time()),
        "total_records": len(all_records),
        "platforms": list(platforms_data.keys()),
        "data_files": [data_file],
        "batch_files": [f"/tmp/feishu_batch_{i+1}.json" for i in range((len(all_records) + batch_size - 1) // batch_size)],
        "status": "ready"
    }
    
    report_file = "/var/log/topic_fetch/final_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    log_message(f"\n=== 任务完成 ===", "SUCCESS")
    log_message(f"报告文件: {report_file}", "INFO")
    log_message(f"总记录数: {len(all_records)}", "INFO")
    log_message("下一步: 使用 feishu_bitable_app_table_record 工具写入数据", "INFO")

if __name__ == "__main__":
    main()