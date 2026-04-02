---
name: wechat-article-exporter-skill
description: 微信公众号文章批量下载工具。支持导出HTML/JSON/Excel/TXT/MD/DOCX格式，HTML格式可100%还原文章排版与样式。支持导出评论、阅读量等数据。
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/wechat-article/wechat-article-exporter
    requires:
      bins:
        - docker
---

# WeChat Article Exporter Skill

微信公众号文章批量下载工具

## 功能特性

- 搜索公众号，支持关键字搜索
- 支持导出多种格式：HTML/JSON/Excel/TXT/MD/DOCX
- HTML格式可100%还原文章排版与样式
- 缓存文章列表数据，减少接口请求次数
- 支持文章过滤（作者、标题、发布时间、原创标识等）
- 支持合集下载
- 支持图片和视频分享消息
- 支持导出评论、评论回复、阅读量、转发量等数据
- 支持Docker部署
- 开放API接口

## 使用方式

### Web界面

访问 `http://localhost:3000` 使用Web界面

### API接口

#### 搜索公众号

```bash
curl -X GET "http://localhost:3000/api/web/search/official-account?keyword=鲁迅"
```

#### 获取文章列表

```bash
curl -X GET "http://localhost:3000/api/web/official-account/{account_id}/articles"
```

#### 下载文章

```bash
curl -X POST "http://localhost:3000/api/web/article/export" \
  -H "Content-Type: application/json" \
  -d '{
    "article_url": "https://mp.weixin.qq.com/s/...",
    "format": "html"
  }'
```

## 支持的导出格式

| 格式 | 说明 |
|------|------|
| HTML | 100%还原排版与样式，包含图片 |
| JSON | 结构化数据格式 |
| Excel | 电子表格格式 |
| TXT | 纯文本格式 |
| MD | Markdown格式 |
| DOCX | Word文档格式 |

## 配置

### 环境变量

```bash
# 服务端口
PORT=3000

# 数据存储路径
NITRO_KV_BASE=.data/kv

# 生产模式
NODE_ENV=production
```

### Docker运行

```bash
docker run -d \
  -p 3000:3000 \
  -v wechat-data:/app/.data \
  --name wechat-exporter \
  wechat-article-exporter:latest
```

## 常见问题

### Q: 如何导出评论数据？
A: 需要抓包获取credentials信息，详见官方文档

### Q: 支持批量下载吗？
A: 支持，可通过API接口实现批量下载

### Q: HTML格式是否完全还原排版？
A: 是的，HTML格式可100%还原文章排版与样式，包含所有图片和样式文件

## 相关链接

- 官方网站：https://down.mptext.top
- 文档站点：https://docs.mptext.top
- GitHub项目：https://github.com/wechat-article/wechat-article-exporter
- API文档：https://docs.mptext.top/api

## 许可证

MIT

## 声明

本工具不会利用您的公众号进行任何形式的私有爬虫。您的公众号只会服务于您自己的抓取文章的目的。

通过本工具获取的公众号文章内容，版权归文章原作者所有，请合理使用。