# 🎉 Mac 上安装 OpenClaw「小龙虾」完全指南

> 适用对象：技术小白 | 电脑：Mac（苹果电脑）| 难度：⭐

---

## 📚 在开始之前，先了解一下

**OpenClaw 小龙虾**是什么？

把它想象成一个「私人AI助手」。安装之后，你可以用中文和它聊天，让它帮你：

- 回答问题、写作文
- 搜索网页、管理日程
- 控制智能家居
- 等等很多很多...

**它需要什么？**

只需要你的 Mac 上有 Node.js（一个让电脑可以运行 AI 程序的工具）。

---

## 第一步：检查你的电脑有没有 Node.js

### 怎么检查？

1. 打开 **终端**（Terminal）
   - 按键盘上的 `Command` + `空格键`（🔍搜索框出现）
   - 输入「终端」两个字
   - 点击「终端」应用

2. 在终端里输入这行命令，按回车键：

```
node --version
```

3. 你会看到类似这样的结果：

   ```
   v22.14.0
   ```

   或者

   ```
   -bash: node: command not found
   ```

### 对照结果判断：

| 你看到的 | 意思是 | 怎么办 |
|----------|--------|--------|
| `v22.x.x`（比如 v22.14.0） | ✅ 已经有 Node.js，而且版本够了 | 直接跳到**第二步** |
| `v20.x.x` 或更低的版本 | ⚠️ 版本有点旧 | 需要升级，看下面的「升级方法」 |
| 「command not found」或什么都没显示 | ❌ 没有安装 Node.js | 需要安装，看下面的「安装方法」 |

---

## 如果没有 Node.js（或版本太旧）—— 安装方法

### 方法：使用 nvm 安装（推荐，最简单）

nvm 是一个「Node.js 版本管理器」，它可以让你轻松安装和切换 Node.js 版本。

#### 1. 安装 nvm

在终端里粘贴这行命令，按回车：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

📌 **提示**：安装过程中会要求你输入电脑密码（Password）。输入时屏幕不会显示任何字符，这是正常的，输入完按回车就行。

#### 2. 让终端认识 nvm

安装完成后，**关闭终端，再重新打开**（这样 nvm 才能生效）。

或者复制粘贴这行命令到终端，按回车：

```bash
source ~/.zshrc
```

#### 3. 用 nvm 安装最新版 Node.js

在终端里运行：

```bash
nvm install 22
```

等待一会儿（大约1-2分钟），看到类似这样的提示就成功了：

```
v22.14.0 is installed
```

#### 4. 验证安装成功

再次检查版本：

```bash
node --version
```

看到 `v22.x.x` 就说明成功了！✅

---

## 第二步：安装 OpenClaw 小龙虾

### 打开终端，运行这行命令：

```bash
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

或者没有任何错误提示，就说明安装成功了！🎉

---

## 第三步：验证安装是否成功

在终端里运行：

```bash
openclaw --version
```

如果看到类似这样的版本号，就说明安装成功了！✅

```
openclaw/2.x.x
```

---

## 第四步：开始配置（初始化向导）

### 运行配置向导

在终端里运行：

```bash
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

1. 打开 Safari 或 Chrome
2. 在地址栏输入：`127.0.0.1:18789`
3. 按回车

---

## 🎊 恭喜你！安装完成！

现在你可以：

- 在 **终端**里输入 `openclaw agent --message "你好"` 和它对话
- 或者在 **Web UI**（网页界面）里和它聊天
- 还可以连接微信、Telegram 等聊天工具（后续教程会讲到）

---

## ❓ 遇到问题怎么办？

### 问题 1：终端提示「Permission denied」权限错误

**解决方法**：在命令前面加 `sudo`，它会要求你输入电脑密码：

```bash
sudo npm install -g openclaw@latest
```

---

### 问题 2：安装速度很慢

**解决方法**：使用国内镜像源，先运行：

```bash
npm config set registry https://registry.npmmirror.com
```

然后再运行安装命令。

---

### 问题 3：端口 18789 被占用

**解决方法**：使用另一个端口启动：

```bash
openclaw gateway --port 18790
```

---

### 问题 4：忘记自己选了什么配置

**解决方法**：重新运行配置向导：

```bash
openclaw onboard
```

---

## 📞 获取帮助

- 官方文档：https://docs.openclaw.ai
- 中文教程：https://openclawgithub.cc
- 遇到无法解决的问题，可以在 OpenClaw 的社区群里求助

---

## 🧹 附录：如何卸载（如果以后不需要了）

如果哪天你想卸载 OpenClaw，运行这两行命令：

```bash
# 1. 卸载程序
npm uninstall -g openclaw

# 2. 删除配置文件（可选，会清除所有设置）
rm -rf ~/.openclaw
```

---

*祝你使用愉快！🎉*
