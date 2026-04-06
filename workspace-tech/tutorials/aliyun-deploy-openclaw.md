# ☁️ 阿里云 ECS 部署 OpenClaw「小龙虾」完全指南

> 适用对象：有基本Linux操作基础的用户 | 服务器：阿里云 ECS | 难度：⭐⭐

---

## 📚 在开始之前，先了解一下

**为什么要把 OpenClaw 部署到云服务器？**

把 AI 助手部署到阿里云服务器，意味着你可以：

- 🚀 **24小时在线** — 不需要开着电脑，服务器一直运行
- 🌐 **远程访问** — 随时随地通过网页或渠道访问你的 AI 助手
- 🤖 **连接更多渠道** — 可以接入微信公众号、企业微信、钉钉等
- 💪 **更稳定** — 专业服务器比个人电脑更稳定可靠

---

## 第一步：购买阿里云 ECS 实例

### 1.1 选择配置

1. 进入 [阿里云 ECS 购买页面](https://www.aliyun.com/product/ecs)
2. 选择以下配置：

| 配置项 | 推荐选择 |
|--------|----------|
| **地域** | 选择离你最近的地域（如华东1杭州） |
| **实例规格** | 推荐 2核2G 以上（ecs.e5-c4m2.large） |
| **操作系统** | 选择 **Ubuntu 22.04 LTS** 或 **CentOS 7.6** |
| **带宽** | 推荐 5Mbps 以上 |
| **存储** | 40GB SSD 云盘起步 |

### 1.2 设置登录密码

- 创建实例时，设置一个 **root 密码**
- 或者选择 **密钥对** 登录（更安全，推荐）

### 1.3 配置安全组

⚠️ **重要**：安全组规则必须开放以下端口，否则外部无法访问！

| 端口 | 用途 | 说明 |
|------|------|------|
| 22 | SSH | 远程连接服务器 |
| 80 | HTTP | Web 访问 |
| 443 | HTTPS | 安全 Web 访问 |
| 18789 | OpenClaw Dashboard | OpenClaw 管理界面 |
| 3000-3001 | WebSocket | 实时通信 |

**添加安全组规则方法：**
1. 进入 ECS 控制台 → 实例 → 更多 → 网络和安全组 → 安全组配置
2. 点击「配置规则」→「入方向」→「添加安全组规则」
3. 按上表添加端口，记得授权对象填 `0.0.0.0/0`

---

## 第二步：连接到服务器

### 方法 1：使用密码登录（适合新手）

1. 打开终端（Mac 用「终端」，Windows 用 PowerShell）
2. 输入以下命令：

```bash
ssh root@你的服务器IP
```

3. 提示密码时，输入你设置的 root 密码

📌 **提示**：输入密码时屏幕不会显示任何字符，这是正常的，输入完按回车即可。

### 方法 2：使用密钥登录（更安全）

1. 本地生成密钥对（如果还没有）：
```bash
ssh-keygen -t rsa -b 4096
```

2. 在阿里云控制台上传公钥

3. 连接时：
```bash
ssh -i ~/.ssh/你的私钥文件 root@你的服务器IP
```

---

## 第三步：安装 Node.js 环境

### 3.1 Ubuntu 系统

```bash
# 更新系统
apt update && apt upgrade -y

# 安装 Node.js 22.x
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# 验证安装
node --version
npm --version
```

### 3.2 CentOS 系统

```bash
# 安装 Node.js 22.x
curl -fsSL https://rpm.nodesource.com/setup_22.x | bash -
yum install -y nodejs

# 验证安装
node --version
npm --version
```

---

## 第四步：安装 OpenClaw 小龙虾

### 4.1 全局安装 OpenClaw

```bash
npm install -g openclaw@latest
```

### 4.2 验证安装

```bash
openclaw --version
```

看到版本号就说明安装成功了！✅

---

## 第五步：配置 OpenClaw

### 5.1 运行初始化向导

```bash
openclaw onboard --install-daemon
```

### 5.2 配置流程

跟着提示操作：

```
? 选择配置模式: QuickStart

? 选择模型供应商:
  ❯ MiniMax（国内可用，推荐）

? 输入 API Key: [粘贴你的API Key]

? 是否配置 Channel（渠道）? No

? 是否安装 Skill（技能）? No

? 是否打开 Web UI? Yes
```

### 5.3 开放外网访问

默认情况下，OpenClaw 只允许本地访问。要开放外网访问：

```bash
# 编辑配置文件
nano ~/.openclaw/config.json
```

找到类似这样的配置：

```json
{
  "gateway": {
    "port": 18789
  }
}
```

修改为：

```json
{
  "gateway": {
    "port": 18789,
    "host": "0.0.0.0"
  }
}
```

保存并退出（Ctrl+X → Y → 回车）

---

## 第六步：配置开机自启动（systemd）

让 OpenClaw 在服务器开机时自动启动：

### 6.1 创建 systemd 服务文件

```bash
sudo nano /etc/systemd/system/openclaw.service
```

### 6.2 写入以下内容

```ini
[Unit]
Description=OpenClaw AI Agent
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/openclaw gateway
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 6.3 启用并启动服务

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启用开机自启
sudo systemctl enable openclaw

# 启动服务
sudo systemctl start openclaw

# 查看状态
sudo systemctl status openclaw
```

看到「active (running)」就说明成功了！🎉

---

## 第七步：配置域名访问（可选但推荐）

### 7.1 购买域名（可选）

1. 在阿里云万网购买一个域名
2. 进行域名备案（国内服务器必须备案）

### 7.2 申请 SSL 证书

1. 进入阿里云 SSL 证书控制台
2. 免费申请 DV 证书
3. 下载证书文件

### 7.3 使用 Nginx 反向代理

```bash
# 安装 Nginx
apt install -y nginx

# 配置反向代理
sudo nano /etc/nginx/sites-available/openclaw
```

写入以下配置：

```nginx
server {
    listen 80;
    server_name 你的域名;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

启用配置：

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/openclaw /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

---

## 第八步：安全加固

### 8.1 配置防火墙

```bash
# Ubuntu
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 18789
ufw enable

# CentOS
firewall-cmd --permanent --add-port=22/tcp
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --permanent --add-port=443/tcp
firewall-cmd --permanent --add-port=18789/tcp
firewall-cmd --reload
```

### 8.2 修改 SSH 端口

```bash
# 编辑 SSH 配置
sudo nano /etc/ssh/sshd_config
```

找到 `#Port 22`，修改为其他端口（如 `Port 2222`）

```bash
# 重启 SSH
sudo systemctl restart sshd
```

---

## 第九步：日常维护

### 查看服务状态

```bash
sudo systemctl status openclaw
```

### 查看日志

```bash
# 实时查看日志
sudo journalctl -u openclaw -f

# 查看历史日志
sudo journalctl -u openclaw --since "1 hour ago"
```

### 重启服务

```bash
sudo systemctl restart openclaw
```

### 更新 OpenClaw

```bash
npm update -g openclaw@latest
sudo systemctl restart openclaw
```

---

## ❓ 常见问题

### 问题 1：安全组规则已添加但仍无法访问

**检查步骤**：
1. 确认安全组入方向规则已添加
2. 确认服务器内部防火墙已开放端口
3. 确认 OpenClaw 配置允许外部访问（host: "0.0.0.0"）

### 问题 2：服务器重启后 OpenClaw 没有启动

**解决方法**：
```bash
sudo systemctl status openclaw
# 如果没有运行：
sudo systemctl start openclaw
# 如果没有启用自启：
sudo systemctl enable openclaw
```

### 问题 3：Nginx 反向代理后无法访问

**检查步骤**：
1. 确认 Nginx 已启动：`sudo systemctl status nginx`
2. 确认 OpenClaw 正在运行：`sudo systemctl status openclaw`
3. 查看 Nginx 错误日志：`sudo tail -f /var/log/nginx/error.log`

### 问题 4：域名无法访问

**检查步骤**：
1. 确认域名已备案（国内服务器）
2. 确认 DNS 解析已生效
3. 确认 SSL 证书已配置

---

## 📊 整体架构图

```
用户
  │
  │  HTTPS (443)
  ▼
Nginx 反向代理
  │
  │  HTTP (18789)
  ▼
OpenClaw Gateway
  │
  ├── Dashboard (Web UI)
  ├── AI 模型 (MiniMax/Kimi/DeepSeek)
  └── 渠道 (微信/钉钉/飞书等)
```

---

## 💰 费用预估

| 项目 | 推荐配置 | 月费用参考 |
|------|----------|-----------|
| ECS 实例 | 2核2G, 5Mbps | 约 80-150 元 |
| 域名 | .cn 后缀 | 约 20-30 元/年 |
| SSL 证书 | 免费 DV | 免费 |
| 对象存储（可选） | 40GB | 约 10 元/月 |
| **合计** | | **约 100-170 元/月** |

---

## 📞 获取帮助

- 阿里云文档：https://help.aliyun.com
- OpenClaw 文档：https://docs.openclaw.ai
- OpenClaw 中文教程：https://openclawgithub.cc

---

*祝你部署顺利！有任何问题欢迎交流！🎉*
