#!/usr/bin/env python3
"""
微信文章抓取工具 V2
使用多种方法尝试获取微信公众号文章内容
"""

import sys
import re
import subprocess
import json


def try_jina_reader(url):
    """使用 Jina Reader API"""
    jina_url = f"https://r.jina.ai/{url}"
    try:
        result = subprocess.run([
            'curl', '-sL', '-m', '15',
            '-A', 'Mozilla/5.0',
            jina_url
        ], capture_output=True, text=True, timeout=20)

        if result.returncode == 0 and result.stdout:
            content = result.stdout
            # 过滤掉 JS 代码
            if 'try{var ua=navigator' not in content[:100]:
                return content
        return None
    except Exception as e:
        return None


def extract_text_from_html(html):
    """从 HTML 中提取文本"""
    # 移除 script 和 style
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)

    # 提取主要内容区域
    patterns = [
        r'<div class="rich_media_content"[^>]*>(.*?)</div>',
        r'<div id="js_content"[^>]*>(.*?)</div>',
        r'<article[^>]*>(.*?)</article>',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
        if matches:
            content = matches[0]
            # 清理 HTML 标签
            content = re.sub(r'<[^>]+>', '\n', content)
            content = re.sub(r'&nbsp;', ' ', content)
            content = re.sub(r'&quot;', '"', content)
            content = re.sub(r'&lt;', '<', content)
            content = re.sub(r'&gt;', '>', content)
            content = re.sub(r'&amp;', '&', content)
            content = re.sub(r'\n\s*\n', '\n\n', content)
            return content.strip()

    return None


def try_direct_fetch(url):
    """直接抓取"""
    try:
        result = subprocess.run([
            'curl', '-sL', '-m', '15',
            '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            url
        ], capture_output=True, text=True, timeout=20)

        if result.returncode == 0 and result.stdout:
            return extract_text_from_html(result.stdout)
        return None
    except Exception as e:
        return None


def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 wechat_export_v2.py <微信文章URL>")
        sys.exit(1)

    url = sys.argv[1]

    print(f"正在抓取微信文章...")
    print(f"URL: {url}")
    print("=" * 70)

    # 方法1: Jina Reader
    print("方法1: 使用 Jina Reader...")
    content = try_jina_reader(url)

    # 方法2: 直接抓取
    if not content or len(content) < 200:
        print("方法2: 直接抓取...")
        content = try_direct_fetch(url)

    if content and len(content) > 200:
        print("\n" + "=" * 70)
        print("【文章内容】")
        print("=" * 70)
        print(content)
        print("\n" + "=" * 70)
        print(f"【字数统计】约 {len(content)} 字")
    else:
        print("\n❌ 无法获取文章内容")
        print("\n可能的原因：")
        print("1. 微信文章需要 JavaScript 渲染")
        print("2. 文章有访问限制或已删除")
        print("3. 网络连接问题")
        print("\n建议：")
        print("• 在浏览器中打开文章，手动复制内容")
        print("• 或者截图后使用 OCR 工具提取文字")


if __name__ == "__main__":
    main()
