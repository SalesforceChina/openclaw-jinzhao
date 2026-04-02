---
name: wechat-article-exporter
description: 微信公众号文章批量下载工具。支持导出HTML/JSON/Excel/TXT/MD/DOCX格式，HTML格式可100%还原文章排版与样式。支持导出评论、阅读量等数据。基于Docker容器化部署。
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/wechat-article/wechat-article-exporter
    requires:
      bins:
        - docker
---

# WeChat Article Exporter Skill

微信公众号文章批量下载工具 - 支持多种格式导出

## 功能特性

- ✅ 搜索公众号，支持关键字搜索
- ✅ 支持导出多种格式：HTML/JSON/Excel/TXT/MD/DOCX
- ✅ HTML格式可100%还原文章排版与样式
- ✅ 缓存文章列表数据，减少接口请求次数
- ✅ 支持文章过滤（作者、标题、发布时间、原创标识等）
- ✅ 支持合集下载
- ✅ 支持图片和视频分享消息
- ✅ 支持导出评论、评论回复、阅读量、转发量等数据
- ✅ Docker容器化部署
- ✅ 开放API接口

## 快速开始

### 1. 启动服务

```bash
# 如果容器已运行，跳过此步
docker run -d \
  -p 3000:3000 \
  --name wechat-exporter \
  wechat-article-exporter:latest
```

### 2. 访问Web界面

打开浏览器访问：`http://localhost:3000`

### 3. 下载文章

在Web界面中：
1. 输入公众号文章URL
2. 选择导出格式（HTML/JSON/Excel等）
3. 点击下载

## API使用

### 搜索公众号

```bash
curl -X GET "http://localhost:3000/api/web/search/official-account?keyword=鲁迅"
```

### 获取文章列表

```bash
curl -X GET "http://localhost:3000/api/web/official-account/{account_id}/articles"
```

### 导出文章

```bash
curl -X POST "http://localhost:3000/api/web/article/export" \
  -H "Content-Type: application/json" \
  -d '{
    "article_url": "https://mp.weixin.qq.com/s/...",
    "format": "html"
  }'
```

## 支持的导出格式

| 格式 | 说明 | 用途 |
|------|------|------|
| HTML | 100%还原排版与样式，包含图片 | 完整保存、离线阅读 |
| JSON | 结构化数据格式 | 数据处理、二次开发 |
| Excel | 电子表格格式 | 数据分析、统计 |
| TXT | 纯文本格式 | 简单保存、搜索 |
| MD | Markdown格式 | 博客发布、版本控制 |
| DOCX | Word文档格式 | 编辑、打印 |

## 使用场景

### 场景1：下载单篇文章

```bash
# 使用Web界面
1. 访问 http://localhost:3000
2. 粘贴文章URL
3. 选择HTML格式
4. 点击下载
```

### 场景2：批量下载公众号文章

```bash
# 使用API接口
1. 搜索公众号获取account_id
2. 获取文章列表
3. 循环调用导出接口
```

### 场景3：导出为Markdown

```bash
# 用于博客发布
curl -X POST "http://localhost:3000/api/web/article/export" \
  -H "Content-Type: application/json" \
  -d '{
    "article_url": "https://mp.weixin.qq.com/s/...",
    "format": "md"
  }' > article.md
```

## 配置

### 环境变量

```bash
# 服务端口
PORT=3000

# 数据存储路径
NITRO_KV_BASE=.data/kv

# 生产模式
NODE_ENV=production

# 监听地址
HOST=0.0.0.0
```

### Docker运行

```bash
# 基础运行
docker run -d \
  -p 3000:3000 \
  --name wechat-exporter \
  wechat-article-exporter:latest

# 带数据持久化
docker run -d \
  -p 3000:3000 \
  -v wechat-data:/app/.data \
  --name wechat-exporter \
  wechat-article-exporter:latest

# 自定义端口
docker run -d \
  -p 8080:3000 \
  --name wechat-exporter \
  wechat-article-exporter:latest
```

## 常见问题

### Q: 如何导出评论数据？
A: 需要抓包获取credentials信息，详见官方文档：https://docs.mptext.top/advanced/wxdown-service.html

### Q: 支持批量下载吗？
A: 支持，可通过API接口实现批量下载

### Q: HTML格式是否完全还原排版？
A: 是的，HTML格式可100%还原文章排版与样式，包含所有图片和样式文件

### Q: 如何私有化部署？
A: 使用Docker容器化部署，支持本地运行或云服务器部署

### Q: 是否支持Cloudflare部署？
A: 支持，详见官方文档

### Q: 下载速度如何？
A: 取决于网络速度和文章大小，通常单篇文章下载时间在1-5秒

### Q: 是否会保存我的公众号信息？
A: 不会。本工具不会利用您的公众号进行任何形式的私有爬虫

## 相关链接

- 官方网站：https://down.mptext.top
- 文档站点：https://docs.mptext.top
- GitHub项目：https://github.com/wechat-article/wechat-article-exporter
- API文档：https://docs.mptext.top/api
- 交流群(QQ)：991482155

## 许可证

MIT

## 声明

本工具承诺：
- 不会利用您的公众号进行任何形式的私有爬虫
- 您的公众号只会服务于您自己的抓取文章的目的
- 不存在账号池或公共账号行为

通过本工具获取的公众号文章内容，版权归文章原作者所有，请合理使用。若发现侵权行为，请联系我们处理。

## 故障排除

### 容器无法启动

```bash
# 检查Docker状态
docker ps -a | grep wechat-exporter

# 查看容器日志
docker logs wechat-exporter

# 重启容器
docker restart wechat-exporter
```

### 无法访问Web界面

```bash
# 检查端口是否开放
netstat -tlnp | grep 3000

# 检查防火墙
sudo ufw allow 3000

# 测试连接
curl http://localhost:3000
```

### API返回错误

```bash
# 检查API端点
curl -v http://localhost:3000/api/web/search/official-account?keyword=test

# 查看详细错误信息
curl -s http://localhost:3000/api/web/search/official-account?keyword=test | jq '.'
```

## 更新和维护

### 更新镜像

```bash
# 拉取最新镜像
docker pull wechat-article/wechat-article-exporter:latest

# 停止旧容器
docker stop wechat-exporter

# 删除旧容器
docker rm wechat-exporter

# 运行新容器
docker run -d \
  -p 3000:3000 \
  -v wechat-data:/app/.data \
  --name wechat-exporter \
  wechat-article/wechat-article-exporter:latest
```

### 清理数据

```bash
# 清理缓存
docker exec wechat-exporter rm -rf .data/kv/*

# 清理容器
docker system prune
```

## 性能优化

### 缓存策略

- 文章列表缓存：减少重复请求
- 图片缓存：加快下载速度
- 元数据缓存：提高搜索效率

### 并发下载

- 支持多个并发请求
- 建议最多10个并发下载
- 避免过度请求导致IP被限制

## 安全建议

1. 不要在公网直接暴露服务，使用反向代理（如Nginx）
2. 启用HTTPS加密传输
3. 定期更新Docker镜像
4. 监控API使用情况，防止滥用
5. 备份重要数据

## 贡献

欢迎提交Issue和Pull Request：https://github.com/wechat-article/wechat-article-exporter

## 支持

如果本项目对您有帮助，请给作者一个Star，感谢您的支持！