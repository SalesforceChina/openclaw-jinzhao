#!/usr/bin/env python3
"""
综合测试脚本 - 评估所有抓取器的效果
"""

import json
import os
import glob
import logging
from datetime import datetime
from typing import Dict, List

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def analyze_data_file(filepath: str) -> Dict:
    """分析数据文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        filename = os.path.basename(filepath)
        
        # 提取基本信息
        result = {
            "file": filename,
            "size_kb": os.path.getsize(filepath) / 1024,
            "timestamp": data.get("timestamp", 0),
            "total": data.get("total", 0),
            "source": data.get("source", "未知"),
            "platforms": {},
            "link_quality": 0,
            "sample_titles": []
        }
        
        # 分析平台分布
        topics = data.get("topics", [])
        for topic in topics[:10]:  # 只分析前10条
            platform = topic.get("来源平台", "未知")
            result["platforms"][platform] = result["platforms"].get(platform, 0) + 1
            
            # 检查链接质量
            link = topic.get("链接", {})
            if isinstance(link, dict):
                link_url = link.get("link", "")
                if link_url and ("http://" in link_url or "https://" in link_url):
                    result["link_quality"] += 1
            
            # 收集示例标题
            title = topic.get("选题标题", "")
            if title and len(result["sample_titles"]) < 3:
                result["sample_titles"].append(title[:50] + "..." if len(title) > 50 else title)
        
        # 计算链接质量百分比
        if topics:
            result["link_quality_pct"] = round(result["link_quality"] / len(topics) * 100, 1)
        else:
            result["link_quality_pct"] = 0
        
        return result
        
    except Exception as e:
        logger.error(f"分析文件 {filepath} 失败: {e}")
        return None

def analyze_batch_file(filepath: str) -> Dict:
    """分析批次文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        filename = os.path.basename(filepath)
        
        # 提取基本信息
        result = {
            "file": filename,
            "size_kb": os.path.getsize(filepath) / 1024,
            "app_token": data.get("app_token", "未知")[:10] + "...",
            "table_id": data.get("table_id", "未知")[:10] + "...",
            "record_count": len(data.get("records", [])),
            "sample_fields": []
        }
        
        # 收集示例字段
        records = data.get("records", [])
        for record in records[:2]:  # 只分析前2条
            fields = record.get("fields", {})
            if fields:
                # 提取关键字段
                sample = {
                    "title": fields.get("选题标题", "")[:30],
                    "platform": fields.get("来源平台", ""),
                    "link": fields.get("链接", {}).get("link", "")[:30] if isinstance(fields.get("链接"), dict) else ""
                }
                result["sample_fields"].append(sample)
        
        return result
        
    except Exception as e:
        logger.error(f"分析批次文件 {filepath} 失败: {e}")
        return None

def main():
    """主函数"""
    logger.info("\n" + "=" * 80)
    logger.info("🔍 选题库抓取系统综合测试")
    logger.info("=" * 80 + "\n")
    
    # 查找所有数据文件
    data_files = glob.glob("/tmp/*topics*.json")
    batch_files = glob.glob("/tmp/feishu_*batch*.json")
    
    logger.info(f"📁 找到 {len(data_files)} 个数据文件")
    logger.info(f"📦 找到 {len(batch_files)} 个批次文件")
    
    # 分析数据文件
    logger.info("\n" + "=" * 80)
    logger.info("📊 数据文件分析")
    logger.info("=" * 80)
    
    data_results = []
    for filepath in sorted(data_files, reverse=True)[:5]:  # 只分析最新的5个
        result = analyze_data_file(filepath)
        if result:
            data_results.append(result)
    
    # 显示数据文件分析结果
    for result in data_results:
        logger.info(f"\n📄 文件: {result['file']}")
        logger.info(f"   大小: {result['size_kb']:.1f} KB")
        logger.info(f"   来源: {result['source']}")
        logger.info(f"   记录数: {result['total']}")
        logger.info(f"   链接质量: {result['link_quality_pct']}%")
        
        # 平台分布
        if result["platforms"]:
            platforms_str = ", ".join([f"{k}({v})" for k, v in result["platforms"].items()])
            logger.info(f"   平台分布: {platforms_str}")
        
        # 示例标题
        if result["sample_titles"]:
            logger.info(f"   示例标题:")
            for i, title in enumerate(result["sample_titles"], 1):
                logger.info(f"     {i}. {title}")
    
    # 分析批次文件
    logger.info("\n" + "=" * 80)
    logger.info("📦 批次文件分析")
    logger.info("=" * 80)
    
    batch_results = []
    for filepath in sorted(batch_files, reverse=True)[:10]:  # 只分析最新的10个
        result = analyze_batch_file(filepath)
        if result:
            batch_results.append(result)
    
    # 按类型分组批次文件
    batch_types = {}
    for result in batch_results:
        filename = result["file"]
        if "ubuntu" in filename:
            batch_types.setdefault("ubuntu", []).append(result)
        elif "server" in filename:
            batch_types.setdefault("server", []).append(result)
        elif "hybrid" in filename:
            batch_types.setdefault("hybrid", []).append(result)
        elif "opencli" in filename:
            batch_types.setdefault("opencli", []).append(result)
        elif "api" in filename:
            batch_types.setdefault("api", []).append(result)
        else:
            batch_types.setdefault("other", []).append(result)
    
    # 显示批次文件分析结果
    for batch_type, results in batch_types.items():
        logger.info(f"\n🔧 {batch_type.upper()} 批次:")
        total_records = sum(r["record_count"] for r in results)
        logger.info(f"   文件数: {len(results)}, 总记录数: {total_records}")
        
        for result in results[:2]:  # 只显示前2个
            logger.info(f"   • {result['file']}: {result['record_count']} 条记录")
            if result["sample_fields"]:
                for sample in result["sample_fields"]:
                    logger.info(f"     标题: {sample['title']}...")
                    logger.info(f"     平台: {sample['platform']}")
                    if sample["link"]:
                        logger.info(f"     链接: {sample['link']}...")
    
    # 运行当前抓取器测试
    logger.info("\n" + "=" * 80)
    logger.info("🚀 运行当前抓取器测试")
    logger.info("=" * 80)
    
    # 测试Ubuntu专用抓取器
    logger.info("\n1. 测试Ubuntu专用抓取器...")
    try:
        import subprocess
        result = subprocess.run(
            ["python3", "/root/.openclaw/workspace-info/ubuntu_fetcher_final.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            logger.info("   ✅ Ubuntu抓取器运行成功")
            # 提取关键信息
            lines = result.stdout.split('\n')
            for line in lines:
                if "总计:" in line:
                    logger.info(f"   {line.strip()}")
                elif "平台分布:" in line:
                    logger.info(f"   {line.strip()}")
        else:
            logger.error(f"   ❌ Ubuntu抓取器运行失败: {result.stderr[:100]}")
            
    except Exception as e:
        logger.error(f"   ❌ Ubuntu抓取器测试异常: {e}")
    
    # 测试服务器版抓取器
    logger.info("\n2. 测试服务器版抓取器...")
    try:
        import subprocess
        result = subprocess.run(
            ["python3", "/root/.openclaw/workspace-info/server_fetcher.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            logger.info("   ✅ 服务器抓取器运行成功")
            # 提取关键信息
            lines = result.stdout.split('\n')
            for line in lines:
                if "总计:" in line:
                    logger.info(f"   {line.strip()}")
                elif "平台分布:" in line:
                    logger.info(f"   {line.strip()}")
        else:
            logger.error(f"   ❌ 服务器抓取器运行失败: {result.stderr[:100]}")
            
    except Exception as e:
        logger.error(f"   ❌ 服务器抓取器测试异常: {e}")
    
    # 检查定时任务
    logger.info("\n" + "=" * 80)
    logger.info("⏰ 定时任务检查")
    logger.info("=" * 80)
    
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            cron_lines = result.stdout.strip().split('\n')
            topic_cron = [line for line in cron_lines if "topic_fetch" in line or "fetch" in line]
            
            if topic_cron:
                logger.info("✅ 找到定时任务:")
                for line in topic_cron:
                    logger.info(f"   {line}")
            else:
                logger.info("⚠️ 未找到选题库相关的定时任务")
        else:
            logger.info("⚠️ 无法读取crontab")
            
    except Exception as e:
        logger.error(f"❌ 检查定时任务失败: {e}")
    
    # 检查日志目录
    logger.info("\n" + "=" * 80)
    logger.info("📋 日志文件检查")
    logger.info("=" * 80)
    
    log_dir = "/var/log/topic_fetch"
    if os.path.exists(log_dir):
        log_files = glob.glob(f"{log_dir}/*.json") + glob.glob(f"{log_dir}/*.log")
        logger.info(f"✅ 日志目录存在: {log_dir}")
        logger.info(f"   日志文件数: {len(log_files)}")
        
        # 显示最新的日志文件
        if log_files:
            latest_log = max(log_files, key=os.path.getmtime)
            logger.info(f"   最新日志: {os.path.basename(latest_log)}")
            logger.info(f"   大小: {os.path.getsize(latest_log) / 1024:.1f} KB")
    else:
        logger.info(f"⚠️ 日志目录不存在: {log_dir}")
    
    # 总结
    logger.info("\n" + "=" * 80)
    logger.info("📈 系统状态总结")
    logger.info("=" * 80)
    
    total_data_files = len(data_files)
    total_batch_files = len(batch_files)
    total_records = sum(r["total"] for r in data_results if r["total"])
    
    logger.info(f"📊 数据统计:")
    logger.info(f"   • 数据文件: {total_data_files} 个")
    logger.info(f"   • 批次文件: {total_batch_files} 个")
    logger.info(f"   • 总记录数: {total_records} 条")
    
    # 计算平均链接质量
    if data_results:
        avg_link_quality = sum(r["link_quality_pct"] for r in data_results) / len(data_results)
        logger.info(f"   • 平均链接质量: {avg_link_quality:.1f}%")
    
    # 平台覆盖统计
    all_platforms = {}
    for result in data_results:
        for platform, count in result["platforms"].items():
            all_platforms[platform] = all_platforms.get(platform, 0) + count
    
    if all_platforms:
        logger.info(f"   • 平台覆盖: {len(all_platforms)} 个平台")
        top_platforms = sorted(all_platforms.items(), key=lambda x: x[1], reverse=True)[:5]
        platforms_str = ", ".join([f"{k}({v})" for k, v in top_platforms])
        logger.info(f"   • 热门平台: {platforms_str}")
    
    logger.info("\n🎯 建议:")
    logger.info("   1. 配置定时任务，每小时自动抓取")
    logger.info("   2. 优化知乎、微博等平台的抓取成功率")
    logger.info("   3. 添加更多平台（虎嗅、人人都是产品经理等）")
    logger.info("   4. 定期清理临时文件")
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ 综合测试完成")
    logger.info("=" * 80)

if __name__ == "__main__":
    main()