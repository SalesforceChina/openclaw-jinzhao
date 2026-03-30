# OpenClaw GitHub 仓库 - 深入学习笔记

## 文档来源
- URL: https://github.com/OpenClaw/OpenClaw/
- 获取时间: 2026-03-28
- 文档类型: GitHub仓库主页

## 项目概述

OpenClaw 是一个个人AI助手，可以在自己的设备上运行。它在您已经使用的渠道上回答您（WhatsApp、Telegram、Slack、Discord、Google Chat、Signal、iMessage、BlueBubbles、IRC、Microsoft Teams、Matrix、Feishu、LINE、Mattermost、Nextcloud Talk、Nostr、Synology Chat、Tlon、Twitch、Zalo、Zalo Personal、WeChat、WebChat）。它可以在macOS/iOS/Android上说话和收听，并可以渲染您控制的实时画布。Gateway只是控制平面——产品是助手。

## 核心特性

### 1. 多渠道支持
支持以下渠道：
- **即时通讯**: WhatsApp, Telegram, Signal, LINE, WeChat, Zalo
- **办公协作**: Slack, Discord, Google Chat, Microsoft Teams, Mattermost, Feishu
- **社交媒体**: Twitch, Nostr
- **企业通讯**: Nextcloud Talk, Synology Chat, Tlon
- **其他**: IRC, iMessage (BlueBubbles), WebChat

### 2. 平台支持
- **桌面端**: macOS, Linux, Windows (通过WSL2)
- **移动端**: iOS, Android
- **服务器端**: 可以在小型Linux实例上运行

### 3. 核心功能
- **语音唤醒** + **对话模式** - macOS/iOS上的唤醒词和Android上的连续语音
- **实时画布** - 代理驱动的可视化工作空间，支持A2UI
- **多智能体路由** - 将入站渠道/账户/对等方路由到隔离的智能体
- **工具系统** - 浏览器、画布、节点、cron、会话等一流工具
- **技能平台** - 捆绑、管理和工作区技能

## 架构概述

### 网关架构
```
WhatsApp / Telegram / Slack / Discord / ... → Gateway (控制平面) → 多个客户端
                                                              ├─ Pi agent (RPC)
                                                              ├─ CLI (openclaw …)
                                                              ├─ WebChat UI
                                                              ├─ macOS app
                                                              └─ iOS / Android nodes
```

### 关键组件
1. **Gateway WebSocket网络** - 客户端、工具和事件的单一WS控制平面
2. **Tailscale暴露** - Gateway仪表板+WS的Serve/Funnel
3. **浏览器控制** - openclaw管理的Chrome/Chromium，带CDP控制
4. **画布 + A2UI** - 代理驱动的可视化工作空间
5. **语音唤醒 + 对话模式** - macOS/iOS上的唤醒词和Android上的连续语音
6. **节点** - 画布、相机快照/剪辑、屏幕录制、位置获取、通知

## 安装与配置

### 安装方式
```bash
# 使用npm
npm install -g openclaw@latest

# 使用pnpm
pnpm add -g openclaw@latest
```

### 推荐设置
```bash
# 运行引导程序
openclaw onboard --install-daemon

# 启动网关
openclaw gateway --port 18789 --verbose
```

### 开发设置
```bash
# 克隆仓库
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 安装依赖
pnpm install
pnpm ui:build  # 首次运行自动安装UI依赖
pnpm build

# 开发循环（源代码/配置更改时自动重新加载）
pnpm gateway:watch
```

## 配置示例

### 最小配置
```json
{
  "agent": {
    "model": "anthropic/claude-opus-4-6"
  }
}
```

### 完整配置结构
```json
{
  "meta": {},
  "wizard": {},
  "auth": {
    "profiles": {}
  },
  "models": {
    "mode": "merge",
    "providers": {}
  },
  "agents": {
    "defaults": {},
    "list": []
  },
  "tools": {
    "profile": "full"
  },
  "bindings": [],
  "commands": {},
  "session": {},
  "channels": {},
  "gateway": {},
  "plugins": {}
}
```

## 渠道配置

### WhatsApp 配置
```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "dmPolicy": "open",
      "allowFrom": ["*"]
    }
  }
}
```

### Telegram 配置
```json
{
  "channels": {
    "telegram": {
      "botToken": "123456:ABCDEF"
    }
  }
}
```

### Discord 配置
```json
{
  "channels": {
    "discord": {
      "token": "1234abcd"
    }
  }
}
```

### Feishu 配置（与我们相关）
```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "yyy",
      "accounts": {
        "account1": {
          "appId": "cli_xxx",
          "appSecret": "yyy",
          "botName": "机器人名称",
          "dmPolicy": "open",
          "allowFrom": ["*"],
          "enabled": true
        }
      }
    }
  }
}
```

## 多智能体配置

### 智能体列表配置
```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "主智能体",
        "workspace": "~/.openclaw/workspace",
        "agentDir": "~/.openclaw/agents/main/agent"
      },
      {
        "id": "writer",
        "name": "写作智能体",
        "workspace": "~/.openclaw/workspace-writer",
        "agentDir": "~/.openclaw/agents/writer/agent"
      }
    ]
  }
}
```

### 绑定配置
```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "feishu",
        "accountId": "default"
      }
    },
    {
      "agentId": "writer",
      "match": {
        "channel": "feishu",
        "accountId": "bot-xxx"
      }
    }
  ]
}
```

## 安全配置

### 默认安全行为
- **DM配对** - 未知发送者收到短配对代码，机器人不处理他们的消息
- **批准方式** - `openclaw pairing approve` 将发送者添加到本地允许列表
- **公共入站DM** - 需要明确选择加入：设置 `dmPolicy="open"` 并在渠道允许列表中包含 `"*"`

### 安全检查
```bash
# 运行医生检查风险/配置错误的DM策略
openclaw doctor
```

### 沙箱配置
```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main"
      }
    }
  }
}
```

## 工具系统

### 可用工具类别
1. **核心工具**: exec, read, write, edit, process
2. **会话工具**: sessions_list, sessions_history, sessions_send, sessions_spawn
3. **渠道工具**: message, browser, canvas
4. **节点工具**: camera.snap, screen.record, location.get
5. **自动化工具**: cron, webhook

### 工具权限控制
```json
{
  "tools": {
    "allow": ["read", "exec", "sessions_list"],
    "deny": ["write", "edit", "browser"]
  }
}
```

## 技能平台

### 技能类型
1. **捆绑技能** - 随OpenClaw一起提供
2. **管理技能** - 通过ClawHub安装
3. **工作区技能** - 在工作区目录中自定义

### ClawHub集成
ClawHub是一个最小的技能注册表。启用ClawHub后，代理可以自动搜索技能并根据需要引入新技能。

## 命令系统

### 可用命令
- `/status` - 紧凑的会话状态（模型+令牌，可用时显示成本）
- `/new` 或 `/reset` - 重置会话
- `/compact` - 压缩会话上下文（摘要）
- `/think` - off|minimal|low|medium|high|xhigh
- `/verbose` on|off
- `/usage` off|tokens|full - 每响应使用页脚
- `/restart` - 重启网关（群组中仅限所有者）
- `/activation` mention|always - 群组激活切换（仅限群组）

## 开发与贡献

### 开发流程
1. **从源代码构建** - 使用pnpm进行构建
2. **开发循环** - 使用 `pnpm gateway:watch` 自动重新加载
3. **测试** - 通过实际渠道进行测试

### 贡献指南
- AI/氛围编码的PR欢迎！🤖
- 遵循CONTRIBUTING.md中的指南

## 社区与支持

### 官方资源
- **网站**: https://openclaw.ai
- **文档**: https://docs.openclaw.ai
- **Discord**: https://discord.gg/clawd
- **GitHub**: https://github.com/openclaw/openclaw

### 赞助商
- OpenAI
- Vercel
- Blacksmith
- Convex

## 与当前项目的关联

### 我们正在使用的特性
1. **多智能体路由** - 创建了鲁迅和IT两个智能体
2. **Feishu渠道集成** - 配置了多个飞书机器人账户
3. **技能管理** - 使用了feishu-bot-manager技能
4. **工作区隔离** - 每个智能体有独立的工作区和配置
5. **绑定系统** - 通过accountId将机器人绑定到特定智能体

### 最佳实践实施
1. **明确分离** - 鲁迅专注于写作，IT专注于技术
2. **独立配置** - 每个智能体有自己的agent.json配置
3. **安全绑定** - 通过accountId精确路由消息
4. **技能利用** - 使用现有技能简化机器人管理
5. **文档学习** - 基于官方文档进行配置和优化