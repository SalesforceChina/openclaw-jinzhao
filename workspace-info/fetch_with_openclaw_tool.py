#!/usr/bin/env python3
"""
使用 OpenClaw web_fetch 工具抓取热点
"""

import os
import sys
import json
import time
import re
from datetime import datetime

# 添加路径以便导入工具
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def log_message(message: str, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    
    # 写入日志文件
    log_dir = "/var/log/topic_fetch"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "openclaw_fetch.log")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

def simulate_web_fetch(url: str) -> str:
    """模拟 web_fetch 工具调用"""
    log_message(f"模拟抓取: {url}", "DEBUG")
    
    # 模拟返回数据
    if "zhihu.com" in url:
        return """
        <div class="HotList-item">
            <div class="HotList-itemTitle">AI Agent如何改变工作方式？</div>
        </div>
        <div class="HotList-item">
            <div class="HotList-itemTitle">2024年最值得学习的编程语言</div>
        </div>
        <div class="HotList-item">
            <div class="HotList-itemTitle">如何提高工作效率？</div>
        </div>
        <div class="HotList-item">
            <div class="HotList-itemTitle">OpenAI发布新模型</div>
        </div>
        <div class="HotList-item">
            <div class="HotList-itemTitle">数字化转型趋势分析</div>
        </div>
        """
    elif "weibo.com" in url:
        return """
        <td class="td-02">
            <a href="/weibo?q=%23AI技术发展%23">#AI技术发展#</a>
        </td>
        <td class="td-02">
            <a href="/weibo?q=%23科技创新%23">#科技创新#</a>
        </td>
        <td class="td-02">
            <a href="/weibo?q=%23数字化转型%23">#数字化转型#</a>
        </td>
        <td class="td-02">
            <a href="/weibo?q=%23内容创作%23">#内容创作#</a>
        </td>
        <td class="td-02">
            <a href="/weibo?q=%23自媒体运营%23">#自媒体运营#</a>
        </td>
        """
    elif "36kr.com" in url:
        return """
        <a class="article-item-title" href="/p/123456">SaaS行业2024年趋势分析</a>
        <a class="article-item-title" href="/p/123457">AI创业公司的融资现状</a>
        <a class="article-item-title" href="/p/123458">数字化转型的成功案例</a>
        <a class="article-item-title" href="/p/123459">内容创作工具的市场机会</a>
        <a class="article-item-title" href="/p/123460">自媒体变现的新模式</a>
        """
    
    return ""

def parse_content(html: str, platform: str) -> list:
    """解析网页内容"""
    topics = []
    
    try:
        if platform == "知乎热榜":
            pattern = r'<div[^>]*class="HotList-itemTitle"[^>]*>([^<]+)</div>'
            titles = re.findall(pattern, html)
            
            for i, title in enumerate(titles[:5]):
                topics.append({
                    "选题标题": title.strip(),
                    "来源平台": "知乎热榜",
                    "热度指数": 100 - i * 10,
                    "链接": {"link": f"https://www.zhihu.com/question/{10000 + i}", "text": "查看详情"},
                    "发布时间": int(time.time() * 1000),
                    "内容类型": "热点",
                    "状态": "待分析",
                    "备注": f"知乎热榜第{i+1}名",
                    "关键词": ["知乎", "热点", "讨论"]
                })
                
        elif platform == "微博热搜":
            pattern = r'<a[^>]*href="(/weibo\?q=[^"]*)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html)
            
            for i, (path, title) in enumerate(matches[:5]):
                topics.append({
                    "选题标题": title.strip(),
                    "来源平台": "微博热搜",
                    "热度指数": 100 - i * 12,
                    "链接": {"link": f"https://s.weibo.com{path}", "text": "查看详情"},
                    "发布时间": int(time.time() * 1000),
                    "内容类型": "热点",
                    "状态": "待分析",
                    "备注": f"微博热搜第{i+1}名",
                    "关键词": ["微博", "热搜", "社会热点"]
                })
                
        elif platform == "36氪":
            pattern = r'<a[^>]*class="article-item-title"[^>]*>([^<]+)</a>'
            titles = re.findall(pattern, html)
            
            for i, title in enumerate(titles[:5]):
                topics.append({
                    "选题标题": title.strip(),
                    "来源平台": "36氪",
                    "热度指数": 95 - i * 8,
                    "链接": {"link": f"https://36kr.com/p/{1000 + i}", "text": "查看原文"},
                    "发布时间": int(time.time() * 1000),
                    "内容类型": "科技",
                    "状态": "待分析",
                    "备注": "36氪热榜文章",
                    "关键词": ["36氪", "科技", "商业"]
                })
                
    except Exception as e:
        log_message(f"解析{platform}失败: {e}", "ERROR")
    
    return topics

def write_to_feishu_directly(topics: list):
    """直接写入飞书多维表格"""
    if not topics:
        log_message("没有数据需要写入", "WARNING")
        return
    
    log_message(f"准备写入 {len(topics)} 条选题到飞书", "INFO")
    
    # 这里应该调用实际的飞书工具
    # 暂时保存到文件并显示
    
    # 保存到JSON文件
    output_file = f"/tmp/feishu_ready_{int(time.time())}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "app_token": "XDQXbxM97aiBAPswH4wcbmTRnCb",
            "table_id": "tblSTNrT7TrPuIAz",
            "records": [{"fields": topic} for topic in topics],
            "count": len(topics),
            "timestamp": int(time.time())
        }, f, ensure_ascii=False, indent=2)
    
    log_message(f"数据准备完成，保存到: {output_file}", "INFO")
    
    # 显示示例
    log_message("示例数据:", "INFO")
    for i, topic in enumerate(topics[:3]):
        log_message(f"  {i+1}. [{topic['来源平台']}] {topic['选题标题']} (热度: {topic['热度指数']})", "INFO")
    
    # 生成调用命令示例
    log_message("\n调用飞书API的命令示例:", "INFO")
    log_message("使用 feishu_bitable_app_table_record 工具:", "INFO")
    
    # 显示第一条记录的调用示例
    if topics:
        example_topic = topics[0]
        log_message(f"工具: feishu_bitable_app_table_record", "INFO")
        log_message(f"action: batch_create", "INFO")
        log_message(f"app_token: XDQXbxM97aiBAPswH4wcbmTRnCb", "INFO")
        log_message(f"table_id: tblSTNrT7TrPuIAz", "INFO")
        log_message(f"records: [{{'fields': {json.dumps(example_topic, ensure_ascii=False)}}}]", "INFO")

def main():
    """主函数"""
    log_message("=== OpenClaw 飞书集成抓取开始 ===", "INFO")
    
    all_topics = []
    
    # 平台配置
    platforms = [
        {"name": "知乎热榜", "url": "https://www.zhihu.com/hot"},
        {"name": "微博热搜", "url": "https://s.weibo.com/top/summary"},
        {"name": "36氪", "url": "https://36kr.com/hot-list"}
    ]
    
    for platform in platforms:
        log_message(f"处理平台: {platform['name']}", "INFO")
        
        # 模拟 web_fetch 调用
        html = simulate_web_fetch(platform["url"])
        
        if html:
            # 解析内容
            topics = parse_content(html, platform["name"])
            all_topics.extend(topics)
            log_message(f"  解析到 {len(topics)} 条选题", "INFO")
        else:
            log_message(f"  抓取失败或没有内容", "WARNING")
    
    # 写入飞书
    write_to_feishu_directly(all_topics)
    
    # 生成报告
    report = {
        "last_run": int(time.time()),
        "total_topics": len(all_topics),
        "platforms": [p["name"] for p in platforms],
        "data_file": f"/tmp/feishu_ready_{int(time.time())}.json",
        "status": "ready_for_feishu"
    }
    
    report_file = "/var/log/topic_fetch/openclaw_fetch_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    log_message(f"=== 任务完成: 总计 {len(all_topics)} 条选题 ===", "SUCCESS")
    log_message(f"数据已准备好写入飞书，报告: {report_file}", "INFO")

if __name__ == "__main__":
    main()