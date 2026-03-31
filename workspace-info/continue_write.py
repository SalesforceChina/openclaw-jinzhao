#!/usr/bin/env python3
"""
继续写入剩余批次
"""

import json
import time

# 读取数据文件
with open('/tmp/platform_crawl_1774949937.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

feishu_records = data.get('feishu_records', [])

print(f"总记录数: {len(feishu_records)}")
print(f"已写入: 20条")
print(f"待写入: {len(feishu_records) - 20}条")

# 显示剩余记录的平台分布
platform_counts = {}
for record in feishu_records[20:]:
    platform = record.get('来源平台', '未知')
    platform_counts[platform] = platform_counts.get(platform, 0) + 1

print("\n剩余记录平台分布:")
for platform, count in platform_counts.items():
    print(f"  {platform}: {count}条")

# 生成剩余批次的写入命令
batch_size = 10
remaining_records = feishu_records[20:]

print(f"\n剩余批次: {(len(remaining_records) + batch_size - 1) // batch_size}批")

# 显示第一批剩余记录
print("\n下一批记录示例:")
for i, record in enumerate(remaining_records[:3]):
    print(f"{i+1}. {record['选题标题'][:50]}...")
    print(f"   平台: {record['来源平台']}")
    print(f"   热度: {record['热度指数']}")
