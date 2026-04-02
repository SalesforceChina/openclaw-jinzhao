# WeChat Article Exporter Skill

微信公众号文章批量下载工具 - OpenClaw Skill

## 概述

这是一个基于 `wechat-article-exporter` 项目的OpenClaw Skill，用于下载和导出微信公众号文章。

支持多种导出格式：HTML、JSON、Excel、TXT、Markdown、DOCX

## 安装

### 前置要求

- Docker（已安装）
- Python 3.7+
- requests库

### 安装步骤

1. **启动Docker容器**

```bash
docker run -d \
  -p 3000:3000 \
  -v wechat-data:/app/.data \
  --name wechat-exporter \
  wechat-article-exporter:latest
```

2. **验证服务**

```bash
curl http://localhost:3000
```

## 使用方法

### 方法1：Web界面（推荐）

访问 `http://localhost:3000`，通过图形界面下载文章

### 方法2：Python脚本

```bash
# 搜索公众号
python3 exporter.py search "鲁迅"

# 导出单篇文章
python3 exporter.py export "https://mp.weixin.qq.com/s/..." \
  --format html \
  --output article.html

# 批量导出
python3 exporter.py batch urls.txt \
  --format html \
  --output ./articles
```

### 方法3：API调用

```bash
# 搜索公众号
curl "http://localhost:3000/api/web/search/official-account?keyword=鲁迅"

# 导出文章
curl -X POST "http://localhost:3000/api/web/article/export" \
  -H "Content-Type: application/json" \
  -d '{
    "article_url": "https://mp.weixin.qq.com/s/...",
    "format": "html"
  }' > article.html
```

## 支持的格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| HTML | .html | 100%还原排版与样式 |
| JSON | .json | 结构化数据 |
| Excel | .xlsx | 电子表格 |
| TXT | .txt | 纯文本 |
| Markdown | .md | Markdown格式 |
| DOCX | .docx | Word文档 |

## 文件结构

```
wechat-article-exporter/
├── SKILL.md              # Skill文档
├── README.md             # 本文件
├── exporter.py           # Python客户端
├── examples.sh           # 使用示例
└── urls.txt.example      # URL列表示例
```

## 常见问题

### Q: 如何批量下载？

A: 创建一个文本文件，每行一个URL，然后运行：

```bash
python3 exporter.py batch urls.txt --format html --output ./articles
```

### Q: 如何导出为Markdown？

A: 使用 `--format md` 参数：

```bash
python3 exporter.py export "URL" --format md --output article.md
```

### Q: 服务无法访问？

A: 检查Docker容器是否运行：

```bash
docker ps | grep wechat-exporter
```

如果没有运行，启动容器：

```bash
docker start wechat-exporter
```

### Q: 如何更新工具？

A: 拉取最新镜像并重启容器：

```bash
docker pull wechat-article/wechat-article-exporter:latest
docker restart wechat-exporter
```

## 示例

### 示例1：下载单篇文章

```bash
python3 exporter.py export \
  "https://mp.weixin.qq.com/s/u9dXAoBs407hy18Avag3Sg" \
  --format html \
  --output article.html
```

### 示例2：批量下载

创建 `urls.txt`：

```
https://mp.weixin.qq.com/s/url1
https://mp.weixin.qq.com/s/url2
https://mp.weixin.qq.com/s/url3
```

然后运行：

```bash
python3 exporter.py batch urls.txt --format html --output ./articles
```

### 示例3：搜索公众号

```bash
python3 exporter.py search "架构师之路"
```

## 配置

### 自定义API地址

如果服务运行在其他地址，使用 `--base-url` 参数：

```bash
python3 exporter.py --base-url http://example.com:3000 \
  export "URL" --format html
```

### 环境变量

```bash
# 设置API地址
export WECHAT_EXPORTER_URL=http://localhost:3000

# 设置默认格式
export WECHAT_EXPORTER_FORMAT=html
```

## 故障排除

### 导出失败

1. 检查URL是否正确
2. 检查网络连接
3. 查看容器日志：`docker logs wechat-exporter`

### 性能问题

1. 减少并发请求数
2. 增加超时时间
3. 检查服务器资源

## 相关链接

- 官方网站：https://down.mptext.top
- GitHub项目：https://github.com/wechat-article/wechat-article-exporter
- 文档：https://docs.mptext.top

## 许可证

MIT

## 声明

本工具仅供学习和个人使用，请遵守微信公众号的使用条款。

不会利用您的公众号进行任何形式的私有爬虫，您的公众号只会服务于您自己的抓取文章的目的。

通过本工具获取的公众号文章内容，版权归文章原作者所有，请合理使用。
