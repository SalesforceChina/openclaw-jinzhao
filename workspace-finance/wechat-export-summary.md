# 微信文章导出工具安装总结

## 任务

安装 Docker + wechat-article-exporter 来抓取微信公众号文章

## 环境检查

### Docker 状态
✅ Docker 已安装 (version 29.3.1)

### 微信文章防护机制
❌ 微信有以下反爬虫措施：
- JavaScript 动态渲染内容
- 请求验证（Referer, Cookie）
- User-Agent 检测
- 访问频率限制
- 域名混淆（mp.weixin.qq.com vs weixin.qq.com）

## 已尝试的方法

| 方法 | 结果 | 说明 |
|------|------|------|
| Docker 搜索镜像 | ❌ | nulldream/wechat-article-exporter 不存在 |
| pip 安装 Python 包 | ❌ | wechat-article-exporter 包不存在 |
| Git 克隆工具 | ❌ | 网络问题 |
| Jina Reader API | ❌ | 返回 JavaScript 代码 |
| 直接 curl 抓取 | ❌ | 需要浏览器环境 |

## 推荐方案

### 方案A：手动复制（最可靠）

```bash
# 1. 在浏览器打开文章
# 2. Ctrl+A 全选
# 3. Ctrl+C 复制
# 4. 粘贴到飞书/文档发给我
```

### 方案B：使用浏览器插件

推荐插件：
- **微信文章导出助手**
- **微信文章下载器**
- **MarkDownload** (将网页转为 Markdown)

安装步骤：
1. Chrome/Edge 访问扩展商店
2. 搜索"微信文章导出"
3. 安装插件
4. 打开微信文章，点击插件导出

### 方案C：使用在线服务

| 服务 | 网址 | 说明 |
|------|------|------|
| 搜狗微信 | https://weixin.sogou.com/ | 搜索后导出 |
| 微信文章导出 | https://www.wechatscope.com/ | 输入链接导出 |
| Markdown Here | 浏览器插件 | 将网页转为 Markdown |

### 方案D：使用浏览器自动化（需要配置）

如果需要完全自动化，可以安装 Playwright：

```bash
# 安装 Playwright
pip3 install playwright
playwright install chromium

# 使用 Python 脚本控制浏览器抓取
```

## 当前可用工具

### 已创建的脚本

1. `/root/.openclaw/workspace-finance/tools/wechat_exporter.py`
   - 基础版本

2. `/root/.openclaw/workspace-finance/tools/wechat_export_v2.py`
   - 改进版本，多方法尝试

**使用方法：**
```bash
python3 /root/.openclaw/workspace-finance/tools/wechat_export_v2.py "https://mp.weixin.qq.com/s/xxxxx"
```

## 技术限制说明

微信公众号文章内容是通过 JavaScript 动态加载的，这意味着：

1. **简单 HTTP 请求无效**：获取的只是 HTML 骨架
2. **需要浏览器环境**：必须执行 JavaScript 才能看到内容
3. **反爬虫检测**：微信会检测并阻止自动化工具

## 结论

对于偶尔抓取微信文章的需求，**最实用的方案是：**

1. **手动复制粘贴** - 零配置，100% 可用
2. **浏览器插件** - 适合经常使用
3. **在线服务** - 无需安装

对于批量抓取需求，建议：
- 使用 Playwright/Selenium（需要配置）
- 或者使用第三方 API 服务

---

**目标文章：** 冯矿伟：周一操作策略（0330）
**建议操作：** 在浏览器中打开文章，全选复制内容，粘贴发送给我，我来用巴菲特式的框架帮你分析。
