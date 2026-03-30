#!/bin/bash
# 定时任务设置脚本

echo "=== 设置热点抓取定时任务 ==="

# 1. 创建工作目录
WORK_DIR="/root/.openclaw/workspace-info"
LOG_DIR="/var/log/topic_fetch"
mkdir -p "$LOG_DIR"

# 2. 创建定时任务脚本
cat > "$WORK_DIR/run_fetch.sh" << 'EOF'
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
EOF

chmod +x "$WORK_DIR/run_fetch.sh"

# 3. 添加cron定时任务
CRON_JOB="0 * * * * $WORK_DIR/run_fetch.sh"
(crontab -l 2>/dev/null | grep -v "run_fetch.sh"; echo "$CRON_JOB") | crontab -

# 4. 创建监控脚本
cat > "$WORK_DIR/monitor_fetch.sh" << 'EOF'
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
EOF

chmod +x "$WORK_DIR/monitor_fetch.sh"

# 5. 创建状态报告
cat > "$WORK_DIR/fetch_status.json" << EOF
{
    "setup_time": "$(date)",
    "cron_schedule": "每小时执行一次",
    "script_location": "$WORK_DIR/run_fetch.sh",
    "log_location": "$LOG_DIR",
    "platforms": ["知乎热榜", "微博热搜", "36氪"],
    "status": "active"
}
EOF

echo "=== 定时任务设置完成 ==="
echo "1. 抓取脚本: $WORK_DIR/run_fetch.sh"
echo "2. 监控脚本: $WORK_DIR/monitor_fetch.sh"
echo "3. 日志目录: $LOG_DIR"
echo "4. Cron任务: 每小时执行一次"
echo ""
echo "立即测试: bash $WORK_DIR/run_fetch.sh"
echo "查看状态: bash $WORK_DIR/monitor_fetch.sh"
echo "查看cron: crontab -l"