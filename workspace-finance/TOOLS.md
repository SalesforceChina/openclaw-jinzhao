# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## 投资分析工具

### 九龙戏珠选股框架

**九条龙（9个筛选维度）+ 重要排除规则：**
1. **时间** - 涨停时间（上午>下午，10:30前最佳）
2. **空间** - 股价位置（底部启动或突破关键压力位）
3. **异动** - 盘口语言（试盘动作如脉冲式拉升）
4. **缺口** - 跳空高开（代表强势突破）
5. **龙头** - 板块地位（必须是领涨股，非跟风）
6. **转势** - 趋势反转（下跌转上升或超跌反转）
7. **股价** - 绝对价格（偏好10元以下低价股）
8. **强度** - 封单力度（封单越大，次日高开概率越大）
9. **热点** - 题材共振（必须契合市场主流热点）

**重要排除规则：**
- **上市不满一年的股票不考虑**
  - 原因：估值不稳定、限售股解禁压力、财务数据少、游资炒作风险
  - 实践：在分析表中添加"上市时间"和"上市满一年"字段
  - 筛选：创建"上市满一年股票"视图，只分析符合条件的股票

**辅助判断技巧：**
- 量比：温和放量（1-3）为佳，过大（>7）可能一日游
- 异动细节：盘中分时线脉冲式拉升后回落是重要信号
- 叠加鱼跃龙门：MACD在0轴附近金叉，成功率提升

**数据来源：**
- 涨停板数据：东方财富网、同花顺财经
- 冯矿伟分析：新浪博客、新浪财经直播
- 视频教程：优酷《股票讲座》第02-03集

### 价值投资框架

**巴菲特核心原则：**
1. 护城河分析
2. 管理层诚信评估
3. 安全边际计算
4. 能力圈坚守

**结合方法：**
- 先用九龙戏珠筛选技术面标的
- 再用价值投资分析基本面质量
- 等待回调机会，不追高
- 分批买入，设好止损

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.