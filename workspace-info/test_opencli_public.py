#!/usr/bin/env python3
"""
测试OpenCLI公开API功能
"""

import json
import subprocess
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def test_opencli_commands():
    """测试OpenCLI命令"""
    commands = [
        # 公开API命令（不需要Browser Extension）
        ("36kr news --limit 3", "36氪新闻"),
        ("hackernews top --limit 3", "HackerNews热榜"),
        ("arxiv search --query 'AI' --limit 3", "arXiv搜索"),
        ("github trending --limit 3", "GitHub趋势"),
    ]
    
    for cmd, description in commands:
        logger.info(f"测试: {description}")
        logger.info(f"命令: opencli {cmd} -f json")
        
        try:
            result = subprocess.run(
                f"opencli {cmd} -f json",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    data = json.loads(result.stdout)
                    logger.info(f"  成功! 返回 {len(data)} 条记录")
                    
                    # 显示第一条记录
                    if data and len(data) > 0:
                        first_item = data[0]
                        title = first_item.get('title') or first_item.get('text') or first_item.get('name', '')
                        logger.info(f"  示例: {title[:50]}...")
                else:
                    logger.warning("  返回空数据")
            else:
                logger.error(f"  失败! 错误码: {result.returncode}")
                logger.error(f"  错误: {result.stderr[:100]}")
                
        except subprocess.TimeoutExpired:
            logger.error("  超时!")
        except json.JSONDecodeError:
            logger.error("  JSON解析失败")
        except Exception as e:
            logger.error(f"  异常: {e}")
        
        logger.info("")

def test_browser_required_commands():
    """测试需要Browser Extension的命令"""
    commands = [
        ("zhihu hot --limit 2", "知乎热榜"),
        ("bilibili hot --limit 2", "Bilibili热榜"),
        ("xiaohongshu search --query 'AI' --limit 2", "小红书搜索"),
    ]
    
    logger.info("=== 测试需要Browser Extension的命令 ===")
    
    for cmd, description in commands:
        logger.info(f"测试: {description}")
        
        try:
            result = subprocess.run(
                f"opencli {cmd} -f json",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # 检查退出码
            if result.returncode == 69:  # EX_UNAVAILABLE
                logger.warning(f"  需要Browser Extension (退出码: 69)")
            elif result.returncode == 77:  # EX_NOPERM
                logger.warning(f"  需要登录 (退出码: 77)")
            elif result.returncode == 0:
                logger.info(f"  成功!")
            else:
                logger.error(f"  失败! 退出码: {result.returncode}")
                
        except subprocess.TimeoutExpired:
            logger.error("  超时!")
        except Exception as e:
            logger.error(f"  异常: {e}")
        
        logger.info("")

def main():
    """主函数"""
    logger.info("=== OpenCLI功能测试 ===")
    
    # 测试公开API命令
    test_opencli_commands()
    
    # 测试需要Browser Extension的命令
    test_browser_required_commands()
    
    logger.info("=== 测试完成 ===")
    
    # 建议
    logger.info("")
    logger.info("=== 建议 ===")
    logger.info("1. 安装Browser Extension以使用完整功能")
    logger.info("2. 在Chrome中登录目标平台")
    logger.info("3. 对于不需要登录的平台，使用公开API命令")
    logger.info("4. 考虑混合方案：OpenCLI + RSS + 公开API")

if __name__ == "__main__":
    main()