# OpenClaw 情报汇总

> 更新时间：2026-03-29

---

## 一、项目概述

**OpenClaw** 是一款开源的个人 AI 助手框架，曾用名 Moltbot、ClawdBot。

**GitHub**: https://github.com/openclaw/openclaw  
**官网**: https://openclaw.ai  
**文档**: https://docs.openclaw.ai  
**Discord**: https://discord.gg/clawd

### 核心定位

```
本地优先 + 自托管 + 多通道 + AI Agent 框架
```

- 在你自己的设备上运行（本地优先）
- 连接各种聊天应用（多通道）
- 连接 AI 模型（支持 OpenAI、Claude、DeepSeek 等）
- 支持 Skills 扩展功能

---

## 二、核心特性

### 1. 多通道支持

| 通道 | 状态 |
|------|------|
| WhatsApp | ✅ 官方支持 |
| Telegram | ✅ 官方支持 |
| Discord | ✅ 官方支持 |
| Slack | ✅ 官方支持 |
| 飞书 (Feishu) | ✅ 官方支持 |
| iMessage | ✅ 官方支持 |
| Signal | ✅ 官方支持 |
| Microsoft Teams | ✅ 官方支持 |
| WeChat | ✅ 官方支持 |
| LINE | ✅ 官方支持 |
| Matrix | ✅ 官方支持 |
| IRC | ✅ 官方支持 |
| Mattermost | ✅ 官方支持 |
| Nextcloud Talk | ✅ 官方支持 |
| Nostr | ✅ 官方支持 |
| Synology Chat | ✅ 官方支持 |
| WebChat | ✅ 官方支持 |

### 2. 平台支持

| 平台 | 支持情况 |
|------|----------|
| macOS | ✅ 菜单栏 App + Voice Wake + Talk Mode |
| iOS | ✅ 节点模式 + Canvas + 语音 |
| Android | ✅ 节点模式 + Canvas + 语音 |
| Windows | ✅ (WSL2 模式) |
| Linux | ✅ 原生支持 |
| Docker | ✅ 官方镜像 |

### 3. AI 模型支持

- **OpenAI** (ChatGPT/Codex) - OAuth 订阅
- **Claude** (Anthropic)
- **DeepSeek**
- **MiniMax**
- **OpenRouter** (聚合多个模型)
- 理论上支持任何兼容 OpenAI API 的模型

### 4. 核心功能

| 功能 | 说明 |
|------|------|
| 多通道网关 | 一个进程连接所有聊天应用 |
| 多 Agent 路由 | 按工作区/用户隔离会话 |
| 语音模式 | Voice Wake + Talk Mode |
| 实时 Canvas | 可视化工作区 |
| 浏览器控制 | Chrome/Chromium CDP 控制 |
| Skills 系统 | 扩展功能模块 |
| Cron 定时任务 | 自动化任务 |
| 移动节点 | iOS/Android 设备作为节点 |

---

## 三、安装部署

### 方式一：npm 全局安装（推荐）

```bash
# Node.js 22+ 或 24+ (推荐)
npm install -g openclaw@latest

# 启动引导安装
openclaw onboard --install-daemon

# 或直接启动网关
openclaw gateway --port 18789 --verbose
```

### 方式二：Docker

```bash
# 拉取镜像
docker pull ghcr.io/openclaw/openclaw:latest

# 运行容器
docker run -d \
  --restart always \
  --name openclaw \
  -p 18789:18789 \
  ghcr.io/openclaw/openclaw:latest
```

### 方式三：从源码构建

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
pnpm openclaw onboard --install-daemon
```

---

## 四、Skills 生态

### 官方 Skills

| Skill | 用途 |
|-------|------|
| feishu-bitable | 飞书多维表格 |
| feishu-calendar | 飞书日历 |
| feishu-im-read | 飞书消息读取 |
| feishu-fetch-doc | 飞书文档获取 |
| feishu-create-doc | 飞书文档创建 |
| tavily | 深度网络搜索 |
| coding-agent | 代码 Agent 委托 |
| chrome-devtools-mcp | 浏览器自动化 |
| weather | 天气查询 |

### Skills 安装

```bash
# 通过 clawhub 安装
openclaw skills install <skill-name>

# 或访问 https://clawhub.ai 搜索
```

---

## 五、飞书集成

### 已知兼容的 Skill

1. **feishu-bitable** - 多维表格管理
2. **feishu-calendar** - 日历与日程
3. **feishu-im-read** - 消息读取与搜索
4. **feishu-fetch-doc** - 文档内容获取
5. **feishu-create-doc** - 创建云文档
6. **feishu-update-doc** - 更新云文档

### 飞书消息处理

- 支持私聊 (DM)
- 支持群聊
- 支持话题回复 (Thread)
- 支持消息引用
- 支持文件/图片下载

---

## 六、竞品对比

| 特性 | OpenClaw | Claude AI | ChatGPT | 其他 Agent |
|------|-----------|-----------|---------|------------|
| 自托管 | ✅ | ❌ | ❌ | 部分支持 |
| 多通道 | ✅ 20+ | ❌ | ❌ | 部分支持 |
| Skills 扩展 | ✅ | ❌ | ❌ | ❌ |
| 本地优先 | ✅ | ❌ | ❌ | 部分 |
| 开源 | ✅ MIT | ❌ | ❌ | 部分 |
| 免费 | ✅ | 部分 | 部分 | 视情况 |

---

## 七、资源链接

### 官方资源

- [GitHub](https://github.com/openclaw/openclaw)
- [官方文档](https://docs.openclaw.ai)
- [Discord 社区](https://discord.gg/clawd)
- [ClawHub (Skills 市场)](https://clawhub.ai)

### 第三方教程

- [OpenClaw Complete Guide](https://www.jitendrazaa.com/blog/ai/clawdbot-complete-guide-open-source-ai-assistant-2026/)
- [How to Install OpenClaw](https://www.witechpedia.com/guide/how-to-install-openclaw/)
- [Setup Guide 2026](https://clawd-bot.com/install/)

### 公众号文章

- [使用OpenClaw+Skill自动发布微信公众号文章 - 博客园](https://www.cnblogs.com/xuxueli/p/19721838)
- [AI自动化发文神器!OpenClaw部署+集成wechat-publisher - 知乎](https://zhuanlan.zhihu.com/p/2017266321478406689)
- [OpenClaw从0到1搭建个人AI助理 - 阿里云](https://developer.aliyun.com/article/1718554)

---

## 八、常见问题

### Q: Node 版本要求？
**A**: Node 24 (推荐) 或 Node 22.16+

### Q: 免费吗？
**A**: 核心框架免费，需要自备 API Key

### Q: 支持中文吗？
**A**: 支持，主要取决于所使用的 AI 模型

### Q: 如何更新？
```bash
npm install -g openclaw@latest
openclaw doctor  # 检查配置
```

---

## 九、我的当前配置

```
OpenClaw 版本: 最新版
运行状态: ✅ 运行中
端口: 3000 (wechat-article-exporter)
Gateway 端口: 18789
通道: 飞书 (Feishu)
模型: minimax/MiniMax-M2.7
```

---

_最后更新：2026-03-29_
