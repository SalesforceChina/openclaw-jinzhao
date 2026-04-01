#!/bin/bash
# 发送天气提醒到飞书
openclaw exec -- "
source /root/.openclaw/workspace-person/scripts/weather-reminder.sh
" 2>/dev/null || bash /root/.openclaw/workspace-person/scripts/weather-reminder.sh
