# SKILLS.md - 柳比歇夫的技能配置

## 核心配置

柳比歇夫使用以下飞书技能作为主要工具：

### 1. feishu-calendar（日历管理）
- **文件位置：** `~/.openclaw/extensions/openclaw-lark/skills/feishu-calendar/SKILL.md`
- **主要用途：**
  - 每日时间规划
  - 深度工作时段安排
  - 定期提醒设置（每日/每周/年度回顾）
- **API 工具：**
  - `feishu_calendar_event` - 创建/查询/更新日程
  - `feishu_calendar_freebusy` - 查询忙闲状态
  - `feishu_calendar_calendar` - 管理日历

### 2. feishu-task（任务管理）
- **文件位置：** `~/.openclaw/extensions/openclaw-lark/skills/feishu-task/SKILL.md`
- **主要用途：**
  - 目标分解（毕生 → 年度 → 月度 → 周 → 日）
  - 任务跟踪
  - 任务评论和子任务
- **API 工具：**
  - `feishu_task_task` - 创建/查询/更新任务
  - `feishu_task_tasklist` - 管理任务清单
  - `feishu_task_subtask` - 子任务管理

### 3. feishu-bitable（数据表）
- **文件位置：** `~/.openclaw/extensions/openclaw-lark/skills/feishu-bitable/SKILL.md`
- **主要用途：**
  - 时间记录（每日时间日志）
  - 目标跟踪（进度、投入时间）
  - 数据分析和报告生成
- **API 工具：**
  - `feishu_bitable_app` - 创建/管理多维表格
  - `feishu_bitable_app_table` - 创建/管理数据表
  - `feishu_bitable_app_table_record` - 记录管理（增删改查）
  - `feishu_bitable_app_table_field` - 字段管理
  - `feishu_bitable_app_table_view` - 视图管理

### 4. feishu-create-doc（文档创建）
- **文件位置：** `~/.openclaw/extensions/openclaw-lark/skills/feishu-create-doc/SKILL.md`
- **主要用途：**
  - 创建每日日记
  - 生成每周/年度总结
  - 建立知识库文档
- **API 工具：**
  - `feishu_create_doc` - 从 Markdown 创建文档

### 5. feishu-fetch-doc（文档读取）
- **文件位置：** `~/.openclaw/extensions/openclaw-lark/skills/feishu-fetch-doc/SKILL.md`
- **主要用途：**
  - 读取历史文档
  - 提取知识库内容
  - 回顾过去总结
- **API 工具：**
  - `feishu_fetch_doc` - 获取文档内容（Markdown）

### 6. feishu-im-read（消息读取）
- **文件位置：** `~/.openclaw/extensions/openclaw-lark/skills/feishu-im-read/SKILL.md`
- **主要用途：**
  - 批量处理飞书消息
  - 搜索历史对话
  - 减少消息切换成本
- **API 工具：**
  - `feishu_im_user_get_messages` - 获取历史消息
  - `feishu_im_user_search_messages` - 搜索消息
  - `feishu_im_user_get_thread_messages` - 获取话题回复

### 7. jina-reader（网页内容提取）
- **文件位置：** `~/.openclaw/extensions/openclaw-lark/skills/jina-reader/SKILL.md`
- **主要用途：**
  - 抓取网页文章并转为 Markdown
  - 批量阅读主题资料
  - 建立个人知识库
- **使用方法：**
  - 在 URL 前添加 `https://r.jina.ai/`

---

## 辅助技能

### 8. proactive-agent-lite（主动提醒）
- **文件位置：** `/www/server/nodejs/v24.13.1/lib/node_modules/openclaw/skills/proactive-agent-lite/SKILL.md`
- **主要用途：**
  - 主动提醒用户记录时间
  - 定期检查目标进度
  - 数据分析和建议

### 9. tavily（网络搜索）
- **文件位置：** `/www/server/nodejs/v24.13.1/lib/node_modules/openclaw/skills/tavily-web-search-for-openclaw/SKILL.md`
- **主要用途：**
  - 查找跨学科资料
  - 验证信息准确性
  - 研究主题深入

---

## 技能使用优先级

### 每日使用（高频）
1. feishu-calendar - 查看日程、安排时间
2. feishu-task - 查看任务、更新进度
3. feishu-bitable - 记录时间、查看统计

### 每周使用（中频）
4. feishu-create-doc - 生成周报
5. feishu-fetch-doc - 回顾历史总结
6. feishu-im-read - 批量处理消息

### 按需使用（低频）
7. jina-reader - 阅读新资料时
8. tavily - 研究主题时
9. proactive-agent-lite - 需要自动化时

---

## 飞书多维表格结构参考

### 表1：daily_time_log（时间记录表）
```
字段：
- date（日期）- 类型：日期
- task_name（任务名称）- 类型：文本
- category（类别）- 类型：单选（纯工作/间接工作/休息/机动）
- planned_minutes（计划分钟数）- 类型：数字
- actual_minutes（实际分钟数）- 类型：数字
- status（状态）- 类型：单选（完成/部分完成/未完成）
- notes（备注）- 类型：文本
- created_time（创建时间）- 类型：创建时间
```

### 表2：goals_tracker（目标跟踪表）
```
字段：
- goal_name（目标名称）- 类型：文本
- goal_level（目标层级）- 类型：单选（毕生/年度/月度/周/日）
- status（状态）- 类型：单选（进行中/已完成/已暂停）
- due_date（截止日期）- 类型：日期
- total_minutes（累计投入分钟）- 类型：数字
- progress（进度百分比）- 类型：数字
- parent_goal（父目标）- 类型：关联（可选）
- notes（备注）- 类型：文本
- created_time（创建时间）- 类型：创建时间
```

---

## API 调用示例

### 创建每日时间记录
```javascript
feishu_bitable_app_table_record({
  action: "create",
  app_token: "xxx",
  table_id: "xxx",
  fields: {
    date: 1740441600000, // 毫秒时间戳
    task_name: "写作",
    category: "纯工作",
    planned_minutes: 120,
    actual_minutes: 90,
    status: "部分完成",
    notes: "被消息打断，需要调整环境"
  }
})
```

### 创建日程事件
```javascript
feishu_calendar_event({
  action: "create",
  summary: "深度工作：写作",
  start_time: "2026-03-29T09:00:00+08:00",
  end_time: "2026-03-29T11:00:00+08:00",
  user_open_id: "ou_xxx" // 从消息上下文获取
})
```

---

## 常见工作流程

### 1. 每日规划流程
```
1. feishu_calendar_event({ action: "list" }) - 查看今日日程
2. feishu_task_task({ action: "list" }) - 查看今日任务
3. 询问用户今日计划
4. 创建/调整日程和任务
```

### 2. 每日记录流程
```
1. 询问用户今日完成情况
2. feishu_bitable_app_table_record({ action: "batch_create" }) - 批量记录时间
3. 计算时间偏差
4. 给出改进建议
```

### 3. 每周回顾流程
```
1. feishu_bitable_app_table_record({ action: "list", filter: {...} }) - 获取本周数据
2. 分析时间分布、效率指标
3. feishu_create_doc() - 生成周报
4. 调整下周计划
```

---

*SKILLS.md 版本：1.0*
*最后更新：2026-03-29*
