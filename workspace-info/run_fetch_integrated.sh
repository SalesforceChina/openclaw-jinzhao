#!/bin/bash
# 集成版定时抓取脚本 - 抓取并写入飞书

WORK_DIR="/root/.openclaw/workspace-info"
LOG_FILE="/var/log/topic_fetch/integrated_fetch_$(date +%Y%m%d_%H%M%S).log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "=== 集成抓取开始: $TIMESTAMP ===" > "$LOG_FILE"

# 执行Python抓取脚本
cd "$WORK_DIR"
echo "执行抓取脚本..." >> "$LOG_FILE"
python3 final_fetch_to_feishu.py >> "$LOG_FILE" 2>&1

# 检查执行结果
if [ $? -eq 0 ]; then
    echo "抓取脚本执行成功" >> "$LOG_FILE"
    
    # 这里可以添加自动调用飞书API的代码
    # 目前需要手动调用，但脚本已经生成了数据文件
    
    # 显示生成的文件
    echo "生成的数据文件:" >> "$LOG_FILE"
    ls -lt /tmp/feishu_batch_*.json 2>/dev/null | head -5 >> "$LOG_FILE"
    
    # 显示记录数量
    if [ -f "/var/log/topic_fetch/final_report.json" ]; then
        TOTAL_RECORDS=$(grep -o '"total_records":[0-9]*' /var/log/topic_fetch/final_report.json | cut -d: -f2)
        echo "总计生成 $TOTAL_RECORDS 条记录" >> "$LOG_FILE"
    fi
    
else
    echo "抓取脚本执行失败" >> "$LOG_FILE"
fi

echo "=== 抓取完成 ===" >> "$LOG_FILE"

# 清理旧日志（保留最近7天）
find /var/log/topic_fetch -name "*.log" -mtime +7 -delete

echo "日志保存到: $LOG_FILE"