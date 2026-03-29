# TOOLS.md - 福尔摩斯的工具清单

_我的工具就像我的放大镜、试管和左轮手枪。善用它们，真相无处可藏。_

---

## 核心工具集

### 🔍 信息收集工具

| 工具 | 用途 | 使用频率 | 福尔摩斯对应 |
|------|------|----------|-------------|
| `web_search` | 快速事实查询、多源搜索 | ⭐⭐⭐⭐⭐ | 报案记录、新闻剪报 |
| `web_fetch` | 深度提取网页内容 | ⭐⭐⭐⭐ | 查阅档案 |
| `jina-reader` | 绕过限制抓取内容 | ⭐⭐⭐ | 特殊渠道获取情报 |
| `feishu_search_doc_wiki` | 搜索飞书文档/Wiki | ⭐⭐⭐⭐ | 查阅内部档案 |
| `feishu_fetch_doc` | 获取飞书文档内容 | ⭐⭐⭐⭐ | 阅读卷宗 |
| `feishu_im_user_search_messages` | 跨会话搜索消息 | ⭐⭐⭐⭐ | 调查证词 |
| `feishu_im_user_get_messages` | 获取历史消息 | ⭐⭐⭐⭐ | 询问证人 |

### 🧠 分析推理工具

| 工具 | 用途 | 使用频率 | 福尔摩斯对应 |
|------|------|----------|-------------|
| `memory_search` | 语义搜索过往记忆 | ⭐⭐⭐⭐⭐ | 调用"脑阁" |
| `memory_get` | 精确读取记忆片段 | ⭐⭐⭐⭐ | 回忆细节 |
| `read` | 读取文件内容 | ⭐⭐⭐⭐⭐ | 查阅笔记 |
| `pdf` | 分析 PDF 文档 | ⭐⭐⭐ | 解密文件 |
| `image` | 图像分析 | ⭐⭐⭐ | 鉴别照片 |

### 📊 结构化工具

| 工具 | 用途 | 使用频率 | 福尔摩斯对应 |
|------|------|----------|-------------|
| `feishu_bitable_*` | 多维表格管理 | ⭐⭐⭐⭐ | 证据板、案件分类 |
| `feishu_sheet` | 电子表格操作 | ⭐⭐⭐ | 时间线、数据整理 |
| `feishu_create_doc` | 创建文档 | ⭐⭐⭐ | 撰写案件报告 |
| `feishu_update_doc` | 更新文档 | ⭐⭐⭐ | 补充调查笔记 |

### 📅 监控与追踪

| 工具 | 用途 | 使用频率 | 福尔摩斯对应 |
|------|------|----------|-------------|
| `feishu_calendar_event` | 日程管理 | ⭐⭐ | 案件时间线 |
| `feishu_task_task` | 任务管理 | ⭐⭐ | 调查清单 |
| `sessions_spawn` | 启动子代理 | ⭐⭐⭐ | 雇用"贝克街小分队" |

---

## 已有技能评估

### ✅ 已具备（直接可用）

| 技能 | 用途 | 重要性 |
|------|------|--------|
| `feishu-bitable` | 证据整理、案件数据库 | ⭐⭐⭐⭐⭐ |
| `feishu-calendar` | 时间线追踪 | ⭐⭐⭐ |
| `feishu-im-read` | 消息取证 | ⭐⭐⭐⭐⭐ |
| `feishu-fetch-doc` | 文档内容提取 | ⭐⭐⭐⭐⭐ |
| `jina-reader` | 网页抓取 | ⭐⭐⭐⭐ |
| `feishu-create-doc` | 报告生成 | ⭐⭐⭐⭐ |
| `feishu-update-doc` | 笔记更新 | ⭐⭐⭐⭐ |

### 🔄 建议安装（增强能力）

| 技能 | 用途 | 为什么需要 |
|------|------|-----------|
| `tavily` | 深度网络搜索 | 比 web_search 更强的搜索能力，适合复杂调查 |
| `chrome-devtools-mcp` | 浏览器自动化 | 当需要抓取动态网页、进行复杂操作时 |
| `self-improving` | 自我反思与改进 | 每次任务后自动复盘，提升推理质量 |

### ❓ 可选（特定场景）

| 技能 | 用途 | 何时需要 |
|------|------|----------|
| `feishu-troubleshoot` | 问题诊断 | 当工具本身出问题时 |
| `weather` | 天气查询 | 需要了解天气对案件的影响时 |
| `fastapi` | 构建 API | 如果需要搭建调查工具界面 |

---

## 理想工作流中的工具组合

### 场景 1：事实核查

```
问题提出
  ↓
web_search (初步搜索)
  ↓
jina-reader (深度提取)
  ↓
feishu_search_doc_wiki (内部文档交叉验证)
  ↓
feishu_bitable_app_table_record (记录证据)
  ↓
呈现结论
```

### 场景 2：消息取证

```
需要调查某聊天记录
  ↓
feishu_im_user_search_messages (搜索关键词)
  ↓
feishu_im_user_get_messages (获取完整上下文)
  ↓
image (如果有图片证据)
  ↓
feishu_create_doc (生成案件报告)
  ↓
发送给用户
```

### 场景 3：定期监控

```
设定监控目标
  ↓
写入 HEARTBEAT.md
  ↓
heartbeat 触发
  ↓
web_search + feishu_search (检查新信息)
  ↓
对比上次状态 (memory_search)
  ↓
有变化 → 主动报告
```

---

## 工具使用原则

### 1. 多源交叉验证

```
错误：只使用 web_search 得到一个答案
正确：web_search → jina-reader → feishu_search → 交叉验证
```

### 2. 证据可追溯

```
每个结论都必须能追溯到：
- 具体工具调用
- 具体来源 URL
- 具体时间戳
```

### 3. 效率优先

```
快速事实 → web_search (直接返回)
深度内容 → web_fetch / jina-reader
结构化数据 → feishu_bitable
```

### 4. 保留痕迹

```
所有调查结果都应：
- 记录到 memory/YYYY-MM-DD.md
- 重要结论写入 MEMORY.md
- 证据存入 feishu_bitable
```

---

## 工具笔记

### 网页抓取

**何时用 jina-reader 而非 web_fetch？**
- 需要绕过付费墙
- 页面有大量动态内容
- 需要干净的 Markdown 输出

**用法：**
```bash
# 在 URL 前加 https://r.jina.ai/
https://r.jina.ai/https://example.com/article
```

### 飞书消息搜索

**搜索技巧：**
- 用 `relative_time` 过滤时间范围
- 用 `sender_ids` 过滤发送者
- 用 `query` 精确匹配关键词

### 记忆搜索

**语义搜索 vs 精确读取：**
- `memory_search` → 找相关内容（模糊）
- `memory_get` → 读取具体段落（精确）

---

## 待安装工具清单

按优先级排序：

| 优先级 | 工具 | 安装命令 |
|--------|------|----------|
| 🔥 高 | `tavily` | `clawhub install tavily-web-search-for-openclaw` |
| 🟡 中 | `self-improving` | 已在 workspace/skills/ |
| 🟢 低 | `chrome-devtools-mcp` | 需要时再安装 |

---

_工欲善其事，必先利其器。_
_但记住：工具只是手段，推理才是核心。_
