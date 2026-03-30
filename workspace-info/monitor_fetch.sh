#!/bin/bash
# 监控抓取任务状态

LOG_DIR="/var/log/topic_fetch"
WORK_DIR="/root/.openclaw/workspace-info"

echo "=== 热点抓取任务监控 ==="
echo "检查时间: $(date)"

# 检查cron任务
echo "1. Cron任务状态:"
crontab -l | grep run_fetch.sh

# 检查最近日志
echo -e "\n2. 最近抓取日志:"
ls -lt "$LOG_DIR"/*.log 2>/dev/null | head -5

# 检查最后抓取时间
echo -e "\n3. 最后抓取状态:"
if [ -f "$LOG_DIR/latest.log" ]; then
    tail -10 "$LOG_DIR/latest.log"
else
    echo "暂无抓取记录"
fi

# 检查脚本状态
echo -e "\n4. 脚本状态:"
if [ -f "$WORK_DIR/run_fetch.sh" ]; then
    echo "抓取脚本: 存在且可执行"
else
    echo "抓取脚本: 不存在"
fi

if [ -f "$WORK_DIR/fetch_with_openclaw.py" ]; then
    echo "Python脚本: 存在"
else
    echo "Python脚本: 不存在"
fi
