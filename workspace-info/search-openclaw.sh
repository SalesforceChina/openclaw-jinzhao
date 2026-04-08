#!/bin/bash
# 每10分钟搜索 Google 上 Openclaw 相关资讯并推送到飞书
# 使用 OpenClaw 的 sessions_spawn 机制

# 定义搜索任务
TASK='请使用 web_search 工具搜索"Openclaw"相关的最新资讯，然后通过飞书将搜索结果发送给我。格式要求：1. 列出3-5条最相关的资讯标题和链接 2. 简短摘要每条资讯的核心内容 3. 如果有重要更新，特别标注'

# 使用 openclaw spawn 创建后台任务
# 这会在隔离的 session 中执行搜索和推送
cd /root/.openclaw/workspace-info

# 记录执行日志
echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') - OpenClaw search task triggered" >> /root/.openclaw/workspace-info/search-openclaw.log

# 注意：这个脚本由 cron 触发，实际的搜索和推送由 agent 在会话中完成
# 需要配合 HEARTBEAT.md 或直接调用 openclaw session
