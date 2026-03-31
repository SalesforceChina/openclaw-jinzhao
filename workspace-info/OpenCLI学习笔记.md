# OpenCLI 学习笔记与集成方案

## 🎯 OpenCLI 核心特性

### 1. **零LLM成本**
- 不消耗Token运行
- 确定性输出，每次运行结果相同
- 可管道化、脚本化、CI友好

### 2. **支持的平台（66+适配器）**

#### 我们需要的平台
- ✅ **Bilibili**: `hot`, `search`, `feed`, `ranking`, `comments`, `download`
- ✅ **Zhihu**: `search`, `feed`, `download` (文章导出Markdown)
- ✅ **Xiaohongshu**: `search`, `note`, `comments`, `feed`, `download`
- ✅ **Twitter/X**: `trending`, `search`, `post`, `download`
- ✅ **Reddit**: `hot`, `search`, `subreddit`, `user-posts`
- ✅ **YouTube**: 通过插件支持

### 3. **工作原理**
1. **Browser Bridge Extension** - 重用Chrome登录状态
2. **Micro-daemon** - 零配置自动启动
3. **AI Agent Ready** - 通过 `opencli list` 自动发现所有工具

### 4. **输出格式**
- `-f json` - JSON格式（适合LLM处理）
- `-f csv` - CSV格式（适合导入表格）
- `-f md` - Markdown格式
- `-f yaml` - YAML格式
- 默认：table格式

## 🚀 快速开始

### 安装
```bash
# 全局安装
npm install -g @jackwener/opencli

# 检查连接状态
opencli doctor

# 查看所有可用命令
opencli list
```

### 使用示例
```bash
# Bilibili热榜
opencli bilibili hot --limit 10 -f json

# 知乎热榜
opencli zhihu search --query "AI" --limit 10 -f json

# 小红书热门笔记
opencli xiaohongshu search --query "AI工具" --limit 10 -f json

# Twitter趋势
opencli twitter trending --limit 10 -f json

# Reddit热榜
opencli reddit hot --limit 10 -f json
```

## 📊 集成到选题库系统

### 方案1：直接替换现有抓取器

```python
#!/usr/bin/env python3
"""
使用OpenCLI的抓取器 - 替代之前的方案
"""

import json
import subprocess
from typing import List, Dict

class OpenCLIFetcher:
    """使用OpenCLI抓取热点"""

    def run_opencli(self, command: str) -> List[Dict]:
        """执行OpenCLI命令"""
        full_command = f"opencli {command} -f json"
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"Error: {result.stderr}")
            return []

    def fetch_bilibili_hot(self, limit: int = 10) -> List[Dict]:
        """抓取Bilibili热榜"""
        data = self.run_opencli(f"bilibili hot --limit {limit}")
        return self.convert_to_feishu_format(data, "Bilibili")

    def fetch_zhihu_hot(self, limit: int = 10) -> List[Dict]:
        """抓取知乎热榜"""
        data = self.run_opencli(f"zhihu search --query '热榜' --limit {limit}")
        return self.convert_to_feishu_format(data, "知乎")

    def fetch_xiaohongshu_hot(self, limit: int = 10) -> List[Dict]:
        """抓取小红书热门笔记"""
        data = self.run_opencli(f"xiaohongshu search --query '热门' --limit {limit}")
        return self.convert_to_feishu_format(data, "小红书")

    def fetch_twitter_trending(self, limit: int = 10) -> List[Dict]:
        """抓取Twitter趋势"""
        data = self.run_opencli(f"twitter trending --limit {limit}")
        return self.convert_to_feishu_format(data, "Twitter")

    def fetch_reddit_hot(self, limit: int = 10) -> List[Dict]:
        """抓取Reddit热榜"""
        data = self.run_opencli(f"reddit hot --limit {limit}")
        return self.convert_to_feishu_format(data, "Reddit")

    def convert_to_feishu_format(self, data: List[Dict], platform: str) -> List[Dict]:
        """转换为飞书表格格式"""
        topics = []

        for i, item in enumerate(data):
            # 根据平台数据结构调整字段映射
            topic = {
                "选题标题": item.get("title") or item.get("text", ""),
                "来源平台": platform,
                "热度指数": 100 - i * 10,
                "链接": {
                    "link": item.get("url") or item.get("link", ""),
                    "text": "查看原文",
                    "type": "url"
                },
                "发布时间": int(time.time() * 1000),
                "内容类型": self.get_content_type(platform),
                "状态": "待分析",
                "备注": f"{platform}热榜第{i+1}名",
                "关键词": self.extract_keywords(item)
            }
            topics.append(topic)

        return topics
```

### 方案2：混合方案（保留现有+OpenCLI扩展）

```python
class HybridTopicFetcher:
    """混合抓取器 - 结合RSS和OpenCLI"""

    def __init__(self):
        self.use_opencli = True  # 优先使用OpenCLI

    def fetch_all_topics(self) -> List[Dict]:
        """抓取所有平台热点"""
        all_topics = []

        # 使用OpenCLI抓取的平台
        if self.use_opencli:
            try:
                # Bilibili
                bilibili_topics = self.fetch_with_opencli("bilibili hot --limit 5")
                all_topics.extend(bilibili_topics)

                # 知乎
                zhihu_topics = self.fetch_with_opencli("zhihu search --query 'AI' --limit 5")
                all_topics.extend(zhihu_topics)

                # 小红书
                xhs_topics = self.fetch_with_opencli("xiaohongshu search --query 'AI工具' --limit 5")
                all_topics.extend(xhs_topics)

            except Exception as e:
                print(f"OpenCLI抓取失败，降级到RSS方案: {e}")
                # 降级到之前的RSS方案
                all_topics.extend(self.fetch_with_rss())

        return all_topics
```

## 🔧 部署步骤

### 1. 安装OpenCLI
```bash
# 在服务器上安装
npm install -g @jackwener/opencli

# 验证安装
opencli doctor
opencli list
```

### 2. 安装Browser Extension
1. 访问 https://github.com/jackwener/opencli/releases
2. 下载 `opencli-extension.zip`
3. 解压
4. 打开 `chrome://extensions`
5. 启用开发者模式
6. 加载已解压的扩展程序

### 3. 登录目标平台
在Chrome中登录：
- Bilibili
- Zhihu
- Xiaohongshu
- Twitter/X（需要VPN）
- Reddit（需要VPN）

### 4. 测试抓取
```bash
# 测试Bilibili
opencli bilibili hot --limit 5

# 测试知乎
opencli zhihu search --query "AI" --limit 5

# 测试小红书
opencli xiaohongshu search --query "热门" --limit 5
```

## 📋 平台映射表

| 平台 | OpenCLI命令 | 字段映射 | 状态 |
|------|-------------|----------|------|
| Bilibili | `bilibili hot` | title, url, author | ✅ 可用 |
| Zhihu | `zhihu search` | title, url, author | ✅ 可用 |
| Xiaohongshu | `xiaohongshu search` | title, url, author | ✅ 可用 |
| Twitter | `twitter trending` | text, url | ⚠️ 需VPN |
| Reddit | `reddit hot` | title, url | ⚠️ 需VPN |
| 36氪 | RSS | title, link | ✅ 已实现 |
| 微博 | RSS | title, link | ⚠️ 限制多 |

## 🎯 优势对比

### OpenCLI vs 原方案

| 特性 | OpenCLI | 原RSS方案 | 优势 |
|------|---------|-----------|------|
| 安装难度 | 简单（npm） | 简单 | 平手 |
| 数据质量 | 真实、完整 | 真实、有限 | OpenCLI胜 |
| 平台覆盖 | 66+ | 2-3个 | OpenCLI胜 |
| 反爬虫 | 无（重用登录） | 经常遇到 | OpenCLI胜 |
| 成本 | 零LLM成本 | 零成本 | 平手 |
| 维护成本 | 低 | 中 | OpenCLI胜 |
| 速度 | 快 | 快 | 平手 |

## 🚀 下一步行动

### 立即执行
1. ✅ 学习OpenCLI文档
2. ⏳ 安装OpenCLI到服务器
3. ⏳ 测试各平台抓取
4. ⏳ 创建集成脚本

### 集成到定时任务
```bash
# 更新定时任务脚本
# 0 * * * * /root/.openclaw/workspace-info/run_fetch_with_opencli.sh
```

### 扩展平台支持
- 第一批：Bilibili, Zhihu, Xiaohongshu
- 第二批：Twitter, Reddit（需解决VPN问题）
- 第三批：YouTube, Instagram等

## 📝 注意事项

### 1. Chrome登录状态
- 必须在Chrome中登录目标平台
- 登录过期会导致抓取失败
- 需要定期检查登录状态

### 2. Browser Extension
- 必须安装并启用扩展
- 扩展必须保持运行
- 可以通过 `opencli doctor` 检查状态

### 3. 错误处理
```bash
# 退出码
77 = 需要登录
69 = 浏览器未运行
66 = 空结果
```

### 4. 性能优化
- 可以并发抓取多个平台
- 使用 `-f json` 直接输出结构化数据
- 避免重复抓取相同内容

---

**学习时间**: 2026-03-31 02:23 UTC
**学习者**: 夏洛克·福尔摩斯 🕵️
**下一步**: 安装并测试OpenCLI