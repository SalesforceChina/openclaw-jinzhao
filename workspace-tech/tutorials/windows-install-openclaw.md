# 🎉 Windows 上安装 OpenClaw「小龙虾」完全指南

> 适用对象：技术小白 | 电脑：Windows 10/11 | 难度：⭐

---

## 📚 在开始之前，先了解一下

**OpenClaw 小龙虾**是什么？

把它想象成一个「私人AI助手」。安装之后，你可以用中文和它聊天，让它帮你：

- 回答问题、写作文
- 搜索网页、管理日程
- 控制智能家居
- 等等很多很多...

**它需要什么？**

只需要你的 Windows 电脑上有 **Node.js**（一个让电脑可以运行 AI 程序的工具）。

---

## 第一步：检查你的电脑有没有 Node.js

### 怎么检查？

1. 按键盘上的 `Windows键 + S`（或者直接点击左下角的搜索图标）
2. 在搜索框里输入「**PowerShell**」
3. 点击「**Windows PowerShell**」（不是 PowerShell ISE）

4. 在 PowerShell 窗口里输入这行命令，按回车键：

```
node --version
```

5. 你会看到类似这样的结果：

   ```
   v22.14.0
   ```

   或者

   ```
   node : 无法将“node”项识别为 cmdlet、函数、脚本文件或可运行程序的名称...
   ```

### 对照结果判断：

| 你看到的 | 意思是 | 怎么办 |
|----------|--------|--------|
| `v22.x.x`（比如 v22.14.0） | ✅ 已经有 Node.js，而且版本够了 | 直接跳到**第二步** |
| `v20.x.x` 或更低的版本 | ⚠️ 版本有点旧 | 需要升级 |
| 「无法识别」或什么都没显示 | ❌ 没有安装 Node.js | 需要安装 |

---

## 如果没有 Node.js（或版本太旧）—— 安装方法

### 使用 nvm-windows 安装（推荐）

nvm-windows 是一个「Node.js 版本管理器」，可以让你轻松安装和切换 Node.js 版本。

#### 1. 下载 nvm-windows

📌 **提示**：先卸载现有的 Node.js（如果有的话），可以避免冲突。

1. 打开浏览器，访问：https://github.com/coreybutler/nvm-windows/releases
2. 找到「**nvm-setup.exe**」下载（大约几MB）

#### 2. 安装 nvm-windows

1. 双击下载的 `nvm-setup.exe` 文件
2. 一路点击「**下一步**」按钮
3. ⚠️ **注意**：安装时会要求你选择 Node.js 的安装目录，保持默认即可
4. 等待安装完成

#### 3. 验证 nvm 安装成功

重新打开一个新的 PowerShell 窗口（**必须重新打开**，这样 nvm 才能生效），输入：

```
nvm version
```

如果显示类似 `1.1.12` 的版本号，说明安装成功！✅

#### 4. 用 nvm 安装最新版 Node.js

在 PowerShell 里运行：

```
nvm install 22
```

等待一会儿（大约1-2分钟），看到类似这样的提示就成功了：

```
Downloading node.js version 22.14.0 (64-bit)...
Extracting...
Complete
```

#### 5. 使用 Node.js 22 版本

```
nvm use 22
```

#### 6. 验证安装成功

```
node --version
```

看到 `v22.x.x` 就说明成功了！✅

---

## 第二步：安装 OpenClaw 小龙虾

### ⚠️ 重要：必须用管理员身份运行 PowerShell

1. 按 `Windows键 + X`
2. 点击「**终端（管理员）**」或「**PowerShell（管理员）**」
3. 如果弹出「用户账户控制」窗口，点击「**是**」

📌 **为什么要用管理员身份？**
因为安装全局工具需要管理员权限，不然会报错。

### 运行安装命令

在 PowerShell（管理员）窗口里输入这行命令，按回车：

```
npm install -g openclaw@latest
```

📌 **提示**：
- `npm` 是用来安装工具的
- `-g` 表示安装到全局（整个电脑都能用）
- `@latest` 表示安装最新版本

### 等待安装完成

你会看到一堆文字滚动过去，最后出现类似这样的内容：

```
added 1 package in 10s
```

或者绿色文字显示「成功」等字样，就说明安装成功了！🎉

---

## 第三步：验证安装是否成功

在 PowerShell 里输入：

```
openclaw --version
```

如果看到类似这样的版本号，就说明安装成功了！✅

```
openclaw/2.x.x
```

---

## 第四步：开始配置（初始化向导）

### 运行配置向导

在 PowerShell 里输入：

```
openclaw onboard --install-daemon
```

### 跟着提示一步一步做：

#### 第 1 步：选择配置模式
```
? 选择配置模式:
  ❯ QuickStart（快速开始，推荐新手）
    Custom（自定义配置）
```
👉 **选 QuickStart**（用键盘上下箭头选中，按回车）

#### 第 2 步：选择 AI 模型
```
? 选择模型供应商:
  ❯ MiniMax（国内可用，中文支持好）
    Kimi
    DeepSeek
    Claude
    Ollama（本地模型）
```
👉 **推荐选 MiniMax**（国内用户首选，中文支持最好）

#### 第 3 步：输入 API Key
```
? 输入 API Key: ___________
```
📌 **API Key 从哪来？**
- 如果你有 MiniMax 账号，登录 [MiniMax 官网](https://www.minimaxi.com/) 就能找到
- 如果没有，可以先去注册一个（使用手机号即可）

#### 第 4 步：跳过可选配置
看到以下提示时，全部选「否」（No）：

```
? 是否配置 Channel（渠道）? No
? 是否安装 Skill（技能）? No
? 是否配置 Hooks? No
```

#### 第 5 步：打开 Web UI
```
? 是否打开 Web UI? Yes
```

---

## 第五步：打开管理界面

配置完成后，浏览器会自动打开一个网页：`http://127.0.0.1:18789`

如果浏览器没有自动打开，你可以**手动打开**：

1. 打开 Edge 或 Chrome
2. 在地址栏输入：`127.0.0.1:18789`
3. 按回车

---

## 🎊 恭喜你！安装完成！

现在你可以：

- 在 **PowerShell** 里输入 `openclaw agent --message "你好"` 和它对话
- 或者在 **Web UI**（网页界面）里和它聊天
- 还可以连接微信、Telegram 等聊天工具（后续教程会讲到）

---

## ❓ 遇到问题怎么办？

### 问题 1：提示「无法识别"npm"」

**原因**：Node.js 没有正确安装

**解决方法**：
1. 重新安装 Node.js（用上面的 nvm 方法）
2. 确保 PowerShell 是「以管理员身份」运行的

---

### 问题 2：提示「Permission denied」权限错误

**原因**：没有管理员权限

**解决方法**：
1. 按 `Windows键 + X`
2. 选择「**终端（管理员）**」或「**PowerShell（管理员）**」
3. 重新运行安装命令

---

### 问题 3：安装速度很慢

**解决方法**：使用国内镜像源，先运行：

```
npm config set registry https://registry.npmmirror.com
```

然后再运行安装命令。

---

### 问题 4：端口 18789 被占用

**解决方法**：使用另一个端口启动：

```
openclaw gateway --port 18790
```

然后浏览器访问 `http://127.0.0.1:18790`

---

### 问题 5：忘记自己选了什么配置

**解决方法**：重新运行配置向导：

```
openclaw onboard
```

---

### 问题 6：nvm use 22 报错「Exit status 1」

**原因**：可能是权限问题或者没有正确安装

**解决方法**：
1. 确保以管理员身份运行 PowerShell
2. 运行 `nvm install 22` 重新安装
3. 再运行 `nvm use 22`

---

## 📞 获取帮助

- 官方文档：https://docs.openclaw.ai
- 中文教程：https://openclawgithub.cc
- 遇到无法解决的问题，可以在 OpenClaw 的社区群里求助

---

## 🧹 附录：如何卸载（如果以后不需要了）

如果哪天你想卸载 OpenClaw，运行这两行命令：

```powershell
# 1. 卸载程序
npm uninstall -g openclaw

# 2. 删除配置文件（可选，会清除所有设置）
Remove-Item -Recurse -Force $env.USERPROFILE\.openclaw
```

---

## 📋 Windows vs Mac 命令对照表

| 操作 | Windows 命令 | Mac 命令 |
|------|------------|---------|
| 打开终端 | `Windows键 + S` → 搜索「PowerShell」 | `Command + 空格` → 搜索「终端」 |
| 以管理员运行 | `Windows键 + X` → 选择「终端（管理员）」 | 不需要（Mac 普通用户权限即可） |
| 检查 Node.js | `node --version` | `node --version` |
| 安装 OpenClaw | `npm install -g openclaw@latest` | `npm install -g openclaw@latest` |
| 验证版本 | `openclaw --version` | `openclaw --version` |
| 开始配置 | `openclaw onboard --install-daemon` | `openclaw onboard --install-daemon` |

---

*祝你使用愉快！🎉*
