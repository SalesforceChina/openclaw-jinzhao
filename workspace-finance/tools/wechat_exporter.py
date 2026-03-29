#!/usr/bin/env python3
"""
微信文章抓取工具
使用多种方法尝试获取微信公众号文章内容
"""

import sys
import re
import json
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError


def extract_wechat_content(url):
    """
    尝试从微信文章URL提取内容
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')

        # 尝试提取文章内容
        # 微信文章通常在特定的div中
        patterns = [
            r'<div class="rich_media_content"[^>]*>(.*?)</div>',
            r'<div id="js_content"[^>]*>(.*?)</div>',
            r'<div class="article-content"[^>]*>(.*?)</div>',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, html, re.DOTALL)
            if matches:
                content = matches[0]
                # 清理HTML标签
                content = re.sub(r'<[^>]+>', '\n', content)
                content = re.sub(r'\n+', '\n\n', content)
                content = content.strip()
                return content

        # 如果没有找到内容，尝试提取纯文本
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        return text[:3000]  # 返回前3000字符

    except (URLError, HTTPError) as e:
        return f"访问错误: {e}"
    except Exception as e:
        return f"发生错误: {e}"


def try_jina_reader(url):
    """
    尝试使用 Jina Reader 获取内容
    """
    jina_url = f"https://r.jina.ai/{url}"
    try:
        req = urllib.request.Request(jina_url, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return None


def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 wechat_exporter.py <微信文章URL>")
        print("示例: python3 wechat_exporter.py https://mp.weixin.qq.com/s/xxxxx")
        sys.exit(1)

    url = sys.argv[1]

    print(f"正在抓取微信文章...")
    print(f"URL: {url}")
    print("=" * 60)

    # 方法1: 尝试直接抓取
    content = extract_wechat_content(url)

    # 方法2: 尝试 Jina Reader
    if len(content) < 500 or "访问错误" in content:
        print("直接抓取失败，尝试使用 Jina Reader...")
        content = try_jina_reader(url)

    if content and len(content) > 200:
        print(content)
    else:
        print("无法获取文章内容。")
        print("\n建议：")
        print("1. 在浏览器中打开文章")
        print("2. 手动复制内容并粘贴")
        print("3. 或者截图后使用 OCR 提取文字")


if __name__ == "__main__":
    main()
