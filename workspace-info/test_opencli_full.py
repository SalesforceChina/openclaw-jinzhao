#!/usr/bin/env python3
"""
OpenCLI完整功能测试脚本
在安装Browser Extension后运行此脚本
"""

import json
import subprocess
import logging
from typing import List, Dict, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def test_opencli_command(command: str, description: str) -> bool:
    """测试OpenCLI命令"""
    logger.info(f"测试: {description}")
    logger.info(f"命令: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            logger.info(f"  ✅ 成功!")
            
            # 尝试解析JSON
            if result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    if isinstance(data, list):
                        logger.info(f"  返回 {len(data)} 条记录")
                        if len(data) > 0:
                            first_item = data[0]
                            title = first_item.get('title') or first_item.get('text') or first_item.get('name', '')
                            logger.info(f"  示例: {title[:50]}...")
                    else:
                        logger.info(f"  返回数据: {type(data)}")
                except json.JSONDecodeError:
                    logger.info(f"  输出: {result.stdout[:100]}...")
            return True
        else:
            logger.error(f"  ❌ 失败! 退出码: {result.returncode}")
            if result.stderr:
                logger.error(f"  错误: {result.stderr[:100]}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("  ⏰ 超时!")
        return False
    except Exception as e:
        logger.error(f"  💥 异常: {e}")
        return False

def main():
    """主函数"""
    logger.info("🔍 OpenCLI完整功能测试")
    logger.info("=" * 50)
    
    # 1. 检查Daemon状态
    logger.info("")
    logger.info("1. 检查Daemon状态...")
    test_opencli_command("opencli doctor", "Daemon诊断")
    
    # 2. 测试需要Browser Extension的命令
    logger.info("")
    logger.info("2. 测试需要Browser Extension的命令...")
    
    tests = [
        ("opencli zhihu hot --limit 2 -f json", "知乎热榜"),
        ("opencli bilibili hot --limit 2 -f json", "Bilibili热榜"),
        ("opencli xiaohongshu search --query 'AI' --limit 2 -f json", "小红书搜索"),
        ("opencli twitter trending --limit 2 -f json", "Twitter趋势"),
        ("opencli reddit hot --limit 2 -f json", "Reddit热门"),
    ]
    
    success_count = 0
    for cmd, desc in tests:
        if test_opencli_command(cmd, desc):
            success_count += 1
        logger.info("")
    
    # 3. 测试公开API命令
    logger.info("")
    logger.info("3. 测试公开API命令...")
    
    public_tests = [
        ("opencli 36kr news --limit 2 -f json", "36氪新闻"),
        ("opencli hackernews top --limit 2 -f json", "HackerNews热榜"),
    ]
    
    for cmd, desc in public_tests:
        test_opencli_command(cmd, desc)
        logger.info("")
    
    # 4. 总结
    logger.info("=" * 50)
    logger.info("📊 测试总结")
    logger.info(f"需要Browser Extension的命令: {success_count}/{len(tests)} 成功")
    
    if success_count == len(tests):
        logger.info("🎉 恭喜！所有功能测试通过！")
        logger.info("现在可以享受完整的OpenCLI功能了！")
    elif success_count > 0:
        logger.info("⚠️ 部分功能可用，请检查登录状态和网络连接")
    else:
        logger.info("❌ Browser Extension可能未正确安装或连接")
        logger.info("请检查:")
        logger.info("  1. Chrome扩展是否已安装")
        logger.info("  2. 是否开启了开发者模式")
        logger.info("  3. 是否在Chrome中登录了目标平台")
        logger.info("  4. Chrome浏览器是否在运行")
    
    # 5. 建议
    logger.info("")
    logger.info("💡 建议:")
    logger.info("  1. 保持Chrome浏览器运行")
    logger.info("  2. 在Chrome中登录所有目标平台")
    logger.info("  3. 对于需要VPN的平台，确保VPN连接正常")
    logger.info("  4. 定期运行 'opencli doctor' 检查状态")

if __name__ == "__main__":
    main()