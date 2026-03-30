#!/bin/bash
# 定时抓取执行脚本

WORK_DIR="/root/.openclaw/workspace-info"
LOG_FILE="/var/log/topic_fetch/fetch_$(date +%Y%m%d_%H%M%S).log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "=== 定时抓取开始: $TIMESTAMP ===" > "$LOG_FILE"

# 执行Python抓取脚本
cd "$WORK_DIR"
python3 fetch_with_openclaw.py >> "$LOG_FILE" 2>&1

# 检查执行结果
if [ $? -eq 0 ]; then
    echo "抓取成功: $TIMESTAMP" >> "$LOG_FILE"
else
    echo "抓取失败: $TIMESTAMP" >> "$LOG_FILE"
fi

echo "=== 抓取完成 ===" >> "$LOG_FILE"

# 清理旧日志（保留最近7天）
find /var/log/topic_fetch -name "*.log" -mtime +7 -delete
