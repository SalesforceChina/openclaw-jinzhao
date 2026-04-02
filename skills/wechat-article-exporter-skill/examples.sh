#!/bin/bash
# WeChat Article Exporter 使用示例

API_BASE="http://localhost:3000/api/web"

# 1. 搜索公众号
echo "=== 搜索公众号 ==="
search_keyword="鲁迅"
echo "搜索关键词: $search_keyword"
curl -s -X GET "$API_BASE/search/official-account?keyword=$search_keyword" | jq '.' | head -50

# 2. 获取文章列表
echo -e "\n=== 获取文章列表 ==="
# 需要替换为实际的account_id
account_id="your_account_id"
echo "账号ID: $account_id"
# curl -s -X GET "$API_BASE/official-account/$account_id/articles" | jq '.'

# 3. 下载单篇文章
echo -e "\n=== 下载文章 ==="
article_url="https://mp.weixin.qq.com/s/..."
format="html"  # 支持: html, json, excel, txt, md, docx

echo "文章URL: $article_url"
echo "导出格式: $format"

# curl -s -X POST "$API_BASE/article/export" \
#   -H "Content-Type: application/json" \
#   -d "{
#     \"article_url\": \"$article_url\",
#     \"format\": \"$format\"
#   }" | jq '.'

echo -e "\n提示: 取消注释上面的curl命令来实际执行请求"