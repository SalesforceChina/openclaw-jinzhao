#!/usr/bin/env python3
"""
微信公众号热榜数据写入飞书
"""

import json
import sys
import os
import time

# 读取抓取的数据
data_file = "/tmp/wechat_hot_topics_1774938467.json"
with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

topics = data.get("topics", [])
print(f"准备写入 {len(topics)} 条微信公众号热榜数据")

# 准备飞书批次数据
batch_data = {
    "app_token": "XDQXbxM97aiBAPswH4wcbmTRnCb",
    "table_id": "tblSTNrT7TrPuIAz",
    "records": []
}

for i, topic in enumerate(topics):
    # 转换数据格式以匹配飞书表格
    record = {
        "fields": {
            "选题标题": topic["选题标题"],
            "来源平台": topic["来源平台"],
            "热度指数": topic["热度指数"],
            "链接": topic["链接"],
            "发布时间": topic["发布时间"],
            "内容类型": topic["内容类型"],
            "状态": topic["状态"],
            "备注": topic["备注"],
            "关键词": topic["关键词"],
            "抓取时间": int(time.time() * 1000)  # 添加抓取时间
        }
    }
    batch_data["records"].append(record)

# 保存批次文件
batch_file = "/tmp/feishu_wechat_write_batch.json"
with open(batch_file, 'w', encoding='utf-8') as f:
    json.dump(batch_data, f, ensure_ascii=False, indent=2)

print(f"批次文件已保存: {batch_file}")
print(f"第一条记录示例:")
print(json.dumps(batch_data["records"][0], ensure_ascii=False, indent=2))

# 生成写入命令
print("\n📋 写入飞书命令:")
print(f"""
# 使用 feishu_bitable_app_table_record 工具写入
# 批量创建记录（最多500条）

from openclaw import feishu_bitable_app_table_record

result = feishu_bitable_app_table_record(
    action="batch_create",
    app_token="XDQXbxM97aiBAPswH4wcbmTRnCb",
    table_id="tblSTNrT7TrPuIAz",
    records={json.dumps(batch_data["records"], ensure_ascii=False)}
)

print(f"写入结果: {{result}}")
""")