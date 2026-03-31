#!/usr/bin/env python3
"""
为飞书记录批量添加内容亮点
"""

import json

# 读取内容亮点数据
with open('/tmp/feishu_records_with_highlights.json', 'r', encoding='utf-8') as f:
    records_with_highlights = json.load(f)

# 创建标题到亮点的映射
title_to_highlight = {}
for record in records_with_highlights:
    title = record.get('选题标题', '')
    highlight = record.get('内容亮点', '')
    title_to_highlight[title] = highlight

# 读取飞书记录ID映射（需要从飞书API获取）
# 这里我们先准备数据，然后分批更新

print(f"✅ 已准备 {len(title_to_highlight)} 条记录的内容亮点映射")
print(f"📋 准备更新飞书记录...")

# 显示示例
print("\n📝 内容亮点示例:")
for i, (title, highlight) in enumerate(list(title_to_highlight.items())[:3]):
    print(f"\n{i+1}. {title[:50]}...")
    print(f"   {highlight.split(chr(10))[0]}")
    print(f"   {highlight.split(chr(10))[1]}")

# 保存映射文件供后续使用
mapping_file = '/tmp/title_highlight_mapping.json'
with open(mapping_file, 'w', encoding='utf-8') as f:
    json.dump(title_to_highlight, f, ensure_ascii=False, indent=2)

print(f"\n💾 映射文件已保存: {mapping_file}")
