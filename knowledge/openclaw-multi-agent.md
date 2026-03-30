# OpenClaw 多智能体路由 - 深入学习笔记

## 文档来源
- URL: https://docs.OpenClaw.ai/zh-CN/concepts/multi-agent
- 获取时间: 2026-03-28
- 文档类型: 官方概念文档

## 核心概念

### 什么是"一个智能体"？
一个**智能体**是一个完全独立作用域的大脑，拥有自己的：

1. **工作区** - 文件、AGENTS.md/SOUL.md/USER.md、本地笔记、人设规则
2. **状态目录** - `agentDir` 用于认证配置文件、模型注册表和每智能体配置
3. **会话存储** - 聊天历史 + 路由状态，位于 `~/.openclaw/agents/<agentId>/sessions` 下

### 认证独立性
- 认证配置文件是**每智能体独立的**
- 每个智能体从自己的位置读取：`~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- 主智能体凭证**不会**自动共享
- 切勿在智能体之间重用 `agentDir`（这会导致认证/会话冲突）

### Skills 独立性
- Skills 通过每个工作区的 `skills/` 文件夹实现每智能体独立
- 共享的 Skills 可从 `~/.openclaw/skills` 获取

## 路径映射

### 关键路径
- **配置**: `~/.openclaw/openclaw.json`（或 `OPENCLAW_CONFIG_PATH`）
- **状态目录**: `~/.openclaw`（或 `OPENCLAW_STATE_DIR`）
- **工作区**: `~/.openclaw/workspace`（或 `~/.openclaw/workspace-<agentId>`）
- **智能体目录**: `~/.openclaw/agents/<agentId>/agent`（或 `agents.list[].agentDir`）
- **会话**: `~/.openclaw/agents/<agentId>/sessions`

### 单智能体模式（默认）
如果什么都不做，OpenClaw 运行单个智能体：
- `agentId` 默认为 **`main`**
- 会话键为 `agent:main:<mainKey>`
- 工作区默认为 `~/.openclaw/workspace`
- 状态默认为 `~/.openclaw/agents/main/agent`

## 多智能体 = 多个人、多种人格

使用**多个智能体**，每个 `agentId` 成为一个**完全隔离的人格**：

1. **不同的电话号码/账户**（每渠道 `accountId`）
2. **不同的人格**（每智能体工作区文件如 `AGENTS.md` 和 `SOUL.md`）
3. **独立的认证 + 会话**（除非明确启用，否则无交叉通信）

这让**多个人**共享一个 Gateway 网关服务器，同时保持他们的 AI"大脑"和数据隔离。

## 路由规则（消息如何选择智能体）

绑定是**确定性的**，**最具体的优先**：

1. `peer` 匹配（精确私信/群组/频道 id）
2. `guildId`（Discord）
3. `teamId`（Slack）
4. 渠道的 `accountId` 匹配
5. 渠道级匹配（`accountId: "*"`）
6. 回退到默认智能体（`agents.list[].default`，否则列表中的第一个条目，默认：`main`）

## 多账户/电话号码

支持**多账户**的渠道（如 WhatsApp）使用 `accountId` 来识别每个登录。每个 `accountId` 可以路由到不同的智能体，因此一个服务器可以托管多个电话号码而不混合会话。

## 关键概念总结

- **`agentId`**: 一个"大脑"（工作区、每智能体认证、每智能体会话存储）
- **`accountId`**: 一个渠道账户实例（例如 WhatsApp 账户 `"personal"` vs `"biz"`）
- **`binding`**: 通过 `(channel, accountId, peer)` 以及可选的 guild/team id 将入站消息路由到 `agentId`
- **直接聊天折叠**到 `agent:<agentId>:<mainKey>`（每智能体"主"；`session.mainKey`）

## 配置示例

### 示例1：两个 WhatsApp → 两个智能体
```json5
{
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
      },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

### 示例2：WhatsApp 日常聊天 + Telegram 深度工作
```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-5",
      },
    ],
  },
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

### 示例3：同一渠道，一个对等方到 Opus
```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-5",
      },
    ],
  },
  bindings: [
    { agentId: "opus", match: { channel: "whatsapp", peer: { kind: "dm", id: "+15551234567" } } },
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

## 每智能体沙箱和工具配置

从 v2026.1.6 开始，每个智能体可以有自己的沙箱和工具限制：

```js
{
  agents: {
    list: [
      {
        id: "personal",
        workspace: "~/.openclaw/workspace-personal",
        sandbox: {
          mode: "off",  // 个人智能体无沙箱
        },
        // 无工具限制 - 所有工具可用
      },
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: {
          mode: "all",     // 始终沙箱隔离
          scope: "agent",  // 每智能体一个容器
          docker: {
            setupCommand: "apt-get update && apt-get install -y git curl",
          },
        },
        tools: {
          allow: ["read"],                    // 仅 read 工具
          deny: ["exec", "write", "edit", "apply_patch"],    // 拒绝其他
        },
      },
    ],
  },
}
```

## 重要注意事项

### 工作区注意事项
- 每个智能体的工作区是**默认 cwd**，而不是硬性沙箱
- 相对路径在工作区内解析，但绝对路径可以访问主机的其他位置，除非启用了沙箱隔离

### 工具允许/拒绝列表
- 工具允许/拒绝列表是**工具**，不是 Skills
- 如果 skill 需要运行二进制文件，请确保 `exec` 被允许且二进制文件存在于沙箱中

### 群组定向
- 对于更严格的限制，设置 `agents.list[].groupChat.mentionPatterns`
- 为渠道保持群组允许列表启用

## 实际应用场景

### 场景1：家庭与工作分离
- 家庭智能体：处理家庭群组消息，有限工具权限
- 工作智能体：处理工作群组消息，完整工具权限

### 场景2：不同专业领域
- 技术智能体：处理技术问题，有编程工具权限
- 写作智能体：处理写作任务，有文档工具权限
- 客服智能体：处理客户咨询，有限工具权限

### 场景3：多语言支持
- 中文智能体：处理中文对话，中文知识库
- 英文智能体：处理英文对话，英文知识库

## 最佳实践

1. **明确分离**：为不同用途创建独立的智能体
2. **权限控制**：根据需求配置工具权限
3. **工作区组织**：为每个智能体创建独立的工作区
4. **绑定清晰**：确保路由绑定准确无误
5. **测试验证**：创建后测试消息路由是否正确

## 与当前项目的关联

基于这个文档，我们现在正在正确实施多智能体架构：

1. **鲁迅 Agent** (`writer`) - 专注于公众号文章写作
2. **比尔·盖茨 Agent** (`IT`) - 专注于IT技术和商业战略
3. **主 Agent** (`main`) - 默认处理其他消息

每个智能体都有：
- 独立的工作区
- 独立的身份和角色
- 独立的技能配置
- 通过 `accountId` 绑定到不同的飞书机器人账户