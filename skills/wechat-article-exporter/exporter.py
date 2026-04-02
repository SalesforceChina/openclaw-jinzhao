#!/usr/bin/env python3
"""
WeChat Article Exporter - Python API Client
微信公众号文章导出工具 - Python API客户端
"""

import requests
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

class WechatArticleExporter:
    """微信公众号文章导出客户端"""
    
    def __init__(self, base_url: str = "http://localhost:3000"):
        """
        初始化客户端
        
        Args:
            base_url: API服务地址，默认为本地3000端口
        """
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api/web"
        self.session = requests.Session()
    
    def search_official_account(self, keyword: str, limit: int = 10) -> Dict[str, Any]:
        """
        搜索公众号
        
        Args:
            keyword: 搜索关键词
            limit: 返回结果数量限制
            
        Returns:
            搜索结果
        """
        url = f"{self.api_base}/search/official-account"
        params = {
            'keyword': keyword,
            'limit': limit
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ 搜索失败: {e}")
            return {}
    
    def get_articles(self, account_id: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """
        获取公众号文章列表
        
        Args:
            account_id: 公众号ID
            page: 页码
            limit: 每页数量
            
        Returns:
            文章列表
        """
        url = f"{self.api_base}/official-account/{account_id}/articles"
        params = {
            'page': page,
            'limit': limit
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取文章列表失败: {e}")
            return {}
    
    def export_article(self, article_url: str, format: str = 'html', 
                      output_path: Optional[str] = None) -> bool:
        """
        导出文章
        
        Args:
            article_url: 文章URL
            format: 导出格式 (html/json/excel/txt/md/docx)
            output_path: 输出文件路径，如果为None则返回内容
            
        Returns:
            是否导出成功
        """
        url = f"{self.api_base}/article/export"
        payload = {
            'article_url': article_url,
            'format': format
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            if output_path:
                # 保存到文件
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                if format in ['html', 'md', 'txt', 'json']:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                else:
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                
                print(f"✅ 文章已导出到: {output_file}")
                return True
            else:
                print(f"✅ 导出成功")
                return True
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 导出失败: {e}")
            return False
    
    def batch_export(self, article_urls: list, format: str = 'html', 
                    output_dir: str = './articles') -> int:
        """
        批量导出文章
        
        Args:
            article_urls: 文章URL列表
            format: 导出格式
            output_dir: 输出目录
            
        Returns:
            成功导出的文章数
        """
        success_count = 0
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for i, url in enumerate(article_urls, 1):
            print(f"\n[{i}/{len(article_urls)}] 正在导出: {url}")
            
            # 生成文件名
            filename = f"article_{i}.{format}"
            file_path = output_path / filename
            
            if self.export_article(url, format, str(file_path)):
                success_count += 1
        
        print(f"\n✅ 批量导出完成: {success_count}/{len(article_urls)} 成功")
        return success_count


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='微信公众号文章导出工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 搜索公众号
  python3 exporter.py search "鲁迅"
  
  # 导出单篇文章
  python3 exporter.py export "https://mp.weixin.qq.com/s/..." --format html --output article.html
  
  # 批量导出
  python3 exporter.py batch urls.txt --format html --output ./articles
        '''
    )
    
    parser.add_argument('--base-url', default='http://localhost:3000',
                       help='API服务地址 (默认: http://localhost:3000)')
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 搜索命令
    search_parser = subparsers.add_parser('search', help='搜索公众号')
    search_parser.add_argument('keyword', help='搜索关键词')
    search_parser.add_argument('--limit', type=int, default=10, help='结果数量限制')
    
    # 导出命令
    export_parser = subparsers.add_parser('export', help='导出文章')
    export_parser.add_argument('url', help='文章URL')
    export_parser.add_argument('--format', default='html', 
                              choices=['html', 'json', 'excel', 'txt', 'md', 'docx'],
                              help='导出格式')
    export_parser.add_argument('--output', help='输出文件路径')
    
    # 批量导出命令
    batch_parser = subparsers.add_parser('batch', help='批量导出')
    batch_parser.add_argument('file', help='包含URL的文件（每行一个URL）')
    batch_parser.add_argument('--format', default='html',
                             choices=['html', 'json', 'excel', 'txt', 'md', 'docx'],
                             help='导出格式')
    batch_parser.add_argument('--output', default='./articles', help='输出目录')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 创建客户端
    exporter = WechatArticleExporter(args.base_url)
    
    # 执行命令
    if args.command == 'search':
        print(f"🔍 搜索公众号: {args.keyword}")
        result = exporter.search_official_account(args.keyword, args.limit)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == 'export':
        print(f"📥 导出文章: {args.url}")
        exporter.export_article(args.url, args.format, args.output)
    
    elif args.command == 'batch':
        print(f"📥 批量导出: {args.file}")
        with open(args.file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        exporter.batch_export(urls, args.format, args.output)


if __name__ == '__main__':
    main()
