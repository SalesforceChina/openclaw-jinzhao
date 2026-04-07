# 🎉 Windows 本地部署 OpenClaw「小龙虾」详细图文教程

> 适用对象：Windows 用户（技术小白到进阶用户）| 难度：⭐

---

## 📚 在开始之前

**什么是 OpenClaw 小龙虾？**

OpenClaw 是一个开源的 AI 助手框架，你可以把它部署在自己的电脑上，完全掌控你的数据和对话。它支持连接各种 AI 模型（MiniMax、Kimi、DeepSeek、Claude 等）和聊天渠道（飞书、微信、Telegram 等）。

**本地部署 vs 云部署**

| 部署方式 | 优点 | 缺点 |
|----------|------|------|
| 本地部署（本章） | 免费、数据隐私、简单 | 需要电脑一直开着 |
| 云服务器部署 | 24小时在线、远程访问 | 需要付费（约100+/月） |

---

## 🧰 准备工作

### 需要准备的东西

1. ✅ 一台 Windows 电脑（Windows 10 或 Windows 11）
2. ✅ 网络连接
3. ✅ 一个 AI 模型 API Key（可选，MiniMax、Kimi 等）

---

## 📥 第一步：官方一键安装（推荐）

这是最简单的方式，脚本会自动检测你的系统、安装 Node.js（如果需要）、安装 OpenClaw，并启动配置向导。

### 打开 PowerShell

**方法 1（推荐）**：
1. 按 `Windows键 + X`
2. 选择「**终端（管理员）**」或「**Windows PowerShell（管理员）**」

**方法 2**：
1. 按 `Windows键 + S`
2. 搜索「PowerShell」
3. 右键选择「以管理员身份运行」

### ⚠️ 重要提示

**必须用管理员身份运行！** 否则安装可能会失败。

### 运行安装命令

在 PowerShell 窗口里粘贴以下命令，按回车：

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

### 等待安装完成

你会看到类似这样的输出：

```
✅ 检测到 Windows 系统
✅ 正在下载 Node.js 安装程序...
✅ Node.js 安装完成
✅ OpenClaw 安装完成
🚀 正在启动配置向导...
```

---

## 📋 如果你没有 API Key——先获取 MiniMax API Key

### 什么是 API Key？

API Key 就像是打开 AI 服务大门的「钥匙」。没有这个钥匙，OpenClaw 就无法连接 AI 模型。

### 获取 MiniMax API Key（国内用户首选）

1. 打开浏览器，访问：[https://www.minimaxi.com/](https://www.minimaxi.com/)
2. 点击「注册」或「登录」（可以用手机号注册）
3. 登录后，进入「控制台」
4. 找到「API Key」选项
5. 点击「创建 API Key」
6. 复制这个 Key（一串字母和数字的组合）

📌 **重要**：API Key 就像密码，一定要保存好！不要告诉别人！

---

## ⚙️ 第二步：运行配置向导

安装完成后，配置向导会自动启动。如果没有自动启动，你可以手动运行：

```powershell
openclaw onboard --install-daemon
```

### 跟着提示操作：

#### 📌 步骤 1：选择配置模式

```
? 选择配置模式:
  ❯ QuickStart（快速开始，推荐新手）
    Custom（自定义配置）
```

👉 **按回车选择 QuickStart**

#### 📌 步骤 2：选择 AI 模型供应商

```
? 选择模型供应商:
  ❯ MiniMax（国内可用，中文支持好）
    Kimi（长文本处理强）
    DeepSeek（推理能力强）
    Claude（需要国际网络）
    Ollama（本地模型，完全离线）
```

👉 **推荐选 MiniMax**（用键盘上下箭头选中，按回车）

#### 📌 步骤 3：输入 API Key

```
? 输入 API Key: ___________
```

👉 **粘贴你的 API Key**（右键选择「粘贴」）

#### 📌 步骤 4：跳过可选配置

```
? 是否配置 Channel（渠道）? No
? 是否安装 Skill（技能）? No  
? 是否配置 Hooks? No
```

👉 **全部输入 n 或 No**

#### 📌 步骤 5：打开 Web UI

```
? 是否打开 Web UI? Yes
```

👉 **输入 y 或 Yes**

---

## 🌐 第三步：打开管理界面

配置完成后，浏览器会自动打开 `http://127.0.0.1:18789`

如果没有自动打开，手动操作：
1. 打开 Edge 或 Chrome
2. 在地址栏输入：`127.0.0.1:18789`
3. 按回车

### 你看到的界面

恭喜你！这就是 OpenClaw 的 Web 管理界面。你可以在这里：
- 和 AI 助手聊天
- 配置各种设置
- 管理渠道和技能

---

## ✅ 验证安装成功

打开 PowerShell，输入以下命令检查状态：

```powershell
openclaw --version
```

应该显示类似：`openclaw/2.x.x`

```powershell
openclaw gateway status
```

应该显示：`Gateway is running`

---

## 🎊 恭喜！安装完成！

现在你可以开始使用 OpenClaw 小龙虾了！

### 常用命令

| 操作 | 命令 |
|------|------|
| 和助手对话 | `openclaw agent --message "你好"` |
| 打开管理界面 | `openclaw dashboard` |
| 查看状态 | `openclaw status` |
| 查看日志 | `openclaw logs` |
| 停止服务 | `openclaw stop` |
| 启动服务 | `openclaw gateway` |

---

## ❓ 常见问题

### 问题 1：提示「无法识别"openclaw"」

**原因**：安装没有成功，或者 PowerShell 没有管理员权限

**解决方法**：
1. 确认用管理员身份运行 PowerShell
2. 重新运行安装命令

---

### 问题 2：安装速度很慢

**解决方法**：使用国内镜像源，先运行：

```powershell
npm config set registry https://registry.npmmirror.com
```

然后重新运行安装命令。

---

### 问题 3：端口 18789 被占用

**解决方法**：使用另一个端口：

```powershell
openclaw gateway --port 18790
```

然后浏览器访问 `http://127.0.0.1:18790`

---

### 问题 4：提示「执行策略错误」

**原因**：PowerShell 执行策略阻止了脚本运行

**解决方法**：
1. 关闭当前 PowerShell
2. 用管理员身份重新打开
3. 运行以下命令允许脚本执行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 问题 5：API Key 错误

**检查步骤**：
1. 确认复制的 API Key 完整（没有遗漏）
2. 确认 API Key 还有额度
3. 重新配置：`openclaw onboard`

---

## 🔧 进阶配置

### 配置开机自启动

让 OpenClaw 在 Windows 启动时自动运行：

```powershell
openclaw onboard --install-daemon
```

### 安装更多技能

```powershell
# 查看可用技能
openclaw skills list

# 安装技能
clawhub install <技能名称>
```

### 连接聊天渠道

```powershell
# 查看可用渠道
openclaw channels list

# 添加渠道
openclaw channels add
```

---

## 🧹 卸载 OpenClaw

如果以后不需要了，运行：

```powershell
# 卸载程序
npm uninstall -g openclaw

# 删除配置文件
Remove-Item -Recurse -Force $env:USERPROFILE\.openclaw
```

---

## 📞 获取帮助

- 官方文档：https://docs.openclaw.ai
- 中文教程：https://openclawgithub.cc
- GitHub：https://github.com/openclaw/openclaw
- 社区 Discord：https://discord.com/invite/clawd

---

## 💡 下一步

安装完成后，你可以：

- 📱 [配置飞书渠道](/guide/channels/) - 连接飞书机器人
- 💬 [配置微信渠道](/guide/channels/) - 连接微信
- 🛠️ [安装技能](/guide/skills/) - 扩展能力
- 🔧 [配置模型](/guide/models/) - 切换 AI 模型

---

*祝你使用愉快！有任何问题欢迎交流！🎉*
