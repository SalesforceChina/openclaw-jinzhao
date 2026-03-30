#!/bin/bash
# 简单抓取脚本 - 使用 OpenClaw 工具

LOG_FILE="/tmp/topic_fetch_$(date +%Y%m%d_%H%M%S).log"
echo "=== 热点抓取开始: $(date) ===" > "$LOG_FILE"

# 使用 web_fetch 抓取知乎热榜
echo "抓取知乎热榜..." >> "$LOG_FILE"
curl -s "https://www.zhihu.com/hot" | grep -o '<div[^>]*class="HotList-itemTitle"[^>]*>[^<]*</div>' | head -10 | sed 's/<[^>]*>//g' | while read -r title; do
    echo "知乎: $title" >> "$LOG_FILE"
done

# 使用 web_fetch 抓取微博热搜
echo "抓取微博热搜..." >> "$LOG_FILE"
curl -s "https://s.weibo.com/top/summary" | grep -o '<a[^>]*href="/weibo[^"]*"[^>]*>[^<]*</a>' | head -10 | sed 's/<[^>]*>//g' | while read -r title; do
    echo "微博: $title" >> "$LOG_FILE"
done

# 使用 web_fetch 抓取36氪热榜
echo "抓取36氪热榜..." >> "$LOG_FILE"
curl -s "https://36kr.com/hot-list" | grep -o '<a[^>]*class="article-item-title"[^>]*>[^<]*</a>' | head -10 | sed 's/<[^>]*>//g' | while read -r title; do
    echo "36氪: $title" >> "$LOG_FILE"
done

echo "=== 抓取完成: $(date) ===" >> "$LOG_FILE"
echo "日志保存到: $LOG_FILE"