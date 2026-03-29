# SKILLS_STATUS.md — 乔布斯的技能配置状态

*最后更新：2026-03-29*

---

## ✅ 已安装的核心 Skills

### 优先级 1：研究与搜索
| Skill | 状态 | 位置 |
|-------|------|------|
| 🔍 tavily | ✅ 已安装 | /www/server/nodejs/v24.13.1/lib/node_modules/openclaw/skills/tavily-web-search-for-openclaw |
| 🌐 jina-reader | ✅ 已安装 | /root/.openclaw/extensions/openclaw-lark/skills/jina-reader |

### 优先级 2：飞书协作套件
| Skill | 状态 | 位置 |
|-------|------|------|
| 📄 feishu-create-doc | ✅ 已安装 | /root/.openclaw/extensions/openclaw-lark/skills/feishu-create-doc |
| 📖 feishu-fetch-doc | ✅ 已安装 | /root/.openclaw/extensions/openclaw-lark/skills/feishu-fetch-doc |
| ✏️ feishu-update-doc | ✅ 已安装 | /root/.openclaw/extensions/openclaw-lark/skills/feishu-update-doc |
| 📊 feishu-bitable | ✅ 已安装 | /root/.openclaw/extensions/openclaw-lark/skills/feishu-bitable |
| 📅 feishu-calendar | ✅ 已安装 | /root/.openclaw/extensions/openclaw-lark/skills/feishu-calendar |
| 💬 feishu-im-read | ✅ 已安装 | /root/.openclaw/extensions/openclaw-lark/skills/feishu-im-read |

### 优先级 3：产品验证
| Skill | 状态 | 位置 |
|-------|------|------|
| ⌨️ coding-agent | ✅ 已安装 | /www/server/nodejs/v24.13.1/lib/node_modules/openclaw/skills/coding-agent |
| 🌐 chrome-devtools-mcp | ✅ 已安装 | /www/server/nodejs/v24.13.1/lib/node_modules/openclaw/skills/chrome-devtools-mcp |

---

## 📋 可用但非核心的 Skills

以下 skills 已安装但不在乔布斯的核心工具箱中（按需使用）：

- clawhub — 技能管理
- feishu-task — 任务管理
- feishu-troubleshoot — 问题排查
- feishu-channel-rules — 频道规则
- 其他系统技能（skill-creator, skill-vetter, tmux 等）

---

## 🎯 工作流就绪

```
问题 → tavily/jina-reader → 深度思考 → feishu-doc
        → coding-agent → 验证 → feishu 协作
```

所有乔布斯需要的核心能力已就绪。可以开始工作。

---

*Keep it simple. Stay focused.*
