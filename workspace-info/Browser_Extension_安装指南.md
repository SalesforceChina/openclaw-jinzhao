# 🔧 OpenCLI Browser Extension 安装指南

## 📦 **已下载的文件**

扩展文件已下载到：`/tmp/opencli-extension-new/`

### 文件结构：
```
/tmp/opencli-extension-new/
├── manifest.json      # 扩展配置文件
├── popup.html         # 扩展弹出页面
├── popup.js           # 扩展JavaScript
├── dist/              # 核心代码
│   └── background.js  # 后台脚本
└── icons/             # 扩展图标
    ├── icon-16.png
    ├── icon-32.png
    ├── icon-48.png
    └── icon-128.png
```

## 🚀 **安装步骤**

### 方法1：手动安装（推荐）

#### 步骤1：打开Chrome扩展管理页面
1. 在Chrome浏览器中打开：`chrome://extensions/`
2. 开启 **开发者模式**（右上角开关）

#### 步骤2：加载已解压的扩展程序
1. 点击 **"加载已解压的扩展程序"** 按钮
2. 选择目录：`/tmp/opencli-extension-new/`
3. 点击 **"选择文件夹"**

#### 步骤3：验证安装
1. 扩展列表中应该出现 **"OpenCLI Browser Bridge"**
2. 扩展图标应该出现在Chrome工具栏中

### 方法2：使用命令行（如果支持）

```bash
# 复制扩展文件到Chrome扩展目录
cp -r /tmp/opencli-extension-new/ ~/.config/google-chrome/Default/Extensions/opencli-extension/
```

## 🔗 **连接OpenCLI Daemon**

### 步骤1：启动OpenCLI Daemon
```bash
# 检查Daemon状态
opencli doctor

# 如果Daemon未运行，启动它
opencli start
```

### 步骤2：验证连接
```bash
# 运行诊断命令
opencli doctor

# 应该看到：
# [OK] Daemon: running on port 19825
# [OK] Extension: connected
# [OK] Connectivity: passed
```

## 🔐 **登录目标平台**

### 重要：必须在Chrome中登录以下平台

| 平台 | 登录状态 | 重要性 |
|------|----------|--------|
| **知乎** | ✅ 必须登录 | 抓取热榜需要 |
| **Bilibili** | ✅ 必须登录 | 抓取热榜需要 |
| **小红书** | ✅ 建议登录 | 搜索内容需要 |
| **Twitter/X** | ⚠️ 需要VPN | 需要VPN访问 |
| **Reddit** | ⚠️ 需要VPN | 需要VPN访问 |

### 登录步骤：
1. **打开Chrome浏览器**
2. **访问目标平台网站**
3. **使用账号密码登录**
4. **保持Chrome运行**（不要关闭）

## 🧪 **测试完整功能**

### 测试知乎热榜
```bash
opencli zhihu hot --limit 5 -f json
```

### 测试Bilibili热榜
```bash
opencli bilibili hot --limit 5 -f json
```

### 测试小红书搜索
```bash
opencli xiaohongshu search --query "AI" --limit 5 -f json
```

### 测试完整诊断
```bash
opencli doctor
```

## 🛠️ **故障排除**

### 问题1：Extension not connected
```
[MISSING] Extension: not connected
```

**解决方案：**
1. 确保Chrome扩展已安装并启用
2. 刷新扩展页面：`chrome://extensions/`
3. 重启Chrome浏览器
4. 重启OpenCLI Daemon：`opencli restart`

### 问题2：需要登录
```
[FAIL] 需要登录 (退出码: 77)
```

**解决方案：**
1. 在Chrome中登录目标平台
2. 刷新页面确保登录状态
3. 重新测试命令

### 问题3：Daemon未运行
```
[FAIL] Daemon: not running
```

**解决方案：**
```bash
# 启动Daemon
opencli start

# 检查状态
opencli status
```

## 📝 **验证脚本**

创建一个验证脚本：

```bash
#!/bin/bash
echo "=== OpenCLI Browser Extension 验证 ==="

# 检查Daemon
echo "1. 检查Daemon状态..."
opencli doctor

# 测试知乎
echo ""
echo "2. 测试知乎热榜..."
opencli zhihu hot --limit 2 -f json 2>&1 | head -20

# 测试Bilibili
echo ""
echo "3. 测试Bilibili热榜..."
opencli bilibili hot --limit 2 -f json 2>&1 | head -20

echo ""
echo "=== 验证完成 ==="
```

## 🎯 **完整功能启用后的优势**

### ✅ **可以使用的平台**
1. **知乎热榜** - 真实热点问题
2. **Bilibili热榜** - 热门视频
3. **小红书搜索** - 用户生成内容
4. **Twitter/X** - 社交媒体热点
5. **Reddit** - 社区讨论

### ✅ **数据质量提升**
- **真实链接** - 不再是模拟ID
- **完整内容** - 包含标题、描述、链接
- **实时更新** - 最新的热点内容

### ✅ **系统集成**
- **自动抓取** - 定时任务每小时运行
- **飞书同步** - 自动写入多维表格
- **数据分析** - 结构化数据便于分析

## 📊 **安装状态检查清单**

- [ ] Chrome扩展已安装
- [ ] 开发者模式已开启
- [ ] OpenCLI Daemon已运行
- [ ] Extension连接正常
- [ ] 知乎已登录
- [ ] Bilibili已登录
- [ ] 测试命令正常运行

## 🚨 **重要提醒**

1. **保持Chrome运行** - 扩展需要Chrome后台运行
2. **不要退出登录** - 保持目标平台登录状态
3. **定期检查连接** - 使用 `opencli doctor` 检查状态
4. **更新扩展** - 定期检查GitHub更新

---

**安装时间**: 2026-03-31 02:33 UTC  
**扩展位置**: `/tmp/opencli-extension-new/`  
**下一步**: 按照指南在Chrome中加载扩展

**完成安装后，运行测试命令验证功能！** 🎉