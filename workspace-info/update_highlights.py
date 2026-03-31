#!/usr/bin/env python3
"""
为飞书记录添加内容亮点描述
"""

import json

# 读取抓取数据
with open('/tmp/platform_crawl_1774949937.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

feishu_records = data.get('feishu_records', [])

# 为每条记录生成内容亮点
for record in feishu_records:
    title = record.get('选题标题', '')
    platform = record.get('来源平台', '')
    category = record.get('内容类型', '')
    hotness = record.get('热度指数', 0)
    
    # 基于标题和平台生成内容亮点
    highlights = []
    
    # 根据标题类型生成亮点
    if 'AI技术突破' in title:
        highlights = [
            f"【核心内容】{platform}最新报道：前沿AI技术突破与行业应用分析",
            "【亮点】深度解读技术创新点、应用场景、市场影响",
            "【价值】为技术从业者提供最新AI发展趋势参考"
        ]
    elif '科技创投' in title or '融资事件' in title:
        highlights = [
            f"【核心内容】{platform}创投动态：最新融资事件、投资趋势分析",
            "【亮点】聚焦融资金额、投资机构、业务模式、市场前景",
            "【价值】为创业者和投资者提供市场风向标"
        ]
    elif '行业分析' in title or '深度解读' in title:
        highlights = [
            f"【核心内容】{platform}行业报告：深度解析{category}领域发展趋势",
            "【亮点】数据支撑、专家观点、案例研究、未来预测",
            "【价值】为企业战略决策提供行业洞察"
        ]
    elif '产品发布' in title or '新产品' in title:
        highlights = [
            f"【核心内容】{platform}产品追踪：最新产品发布与功能更新",
            "【亮点】产品特色、技术创新、用户体验、竞品对比",
            "【价值】了解市场最新产品动态和技术趋势"
        ]
    elif '政策解读' in title:
        highlights = [
            f"【核心内容】{platform}政策分析：科技政策对行业的影响解读",
            "【亮点】政策要点、行业影响、应对策略、机遇与挑战",
            "【价值】帮助企业把握政策红利，规避风险"
        ]
    elif '热门讨论' in title or '用户热议' in title:
        highlights = [
            f"【核心内容】{platform}社区热点：用户最关注的话题和讨论",
            "【亮点】用户观点、情感倾向、争议焦点、社会影响",
            "【价值】了解用户真实需求和关注点"
        ]
    elif '技术分享' in title or '实用教程' in title:
        highlights = [
            f"【核心内容】{platform}技术干货：实战经验分享和教程",
            "【亮点】操作步骤、代码示例、最佳实践、常见问题",
            "【价值】提升技术能力和解决实际问题"
        ]
    elif '经验交流' in title or '真实案例' in title:
        highlights = [
            f"【核心内容】{platform}案例分析：真实项目经验总结",
            "【亮点】项目背景、解决方案、经验教训、避坑指南",
            "【价值】借鉴他人经验，少走弯路"
        ]
    elif '问答精华' in title or '高赞回答' in title:
        highlights = [
            f"【核心内容】{platform}知识沉淀：高质量问答精华",
            "【亮点】专家解答、深度分析、实用建议、参考价值",
            "【价值】快速获取专业知识和解决方案"
        ]
    elif '行业洞察' in title or '专业人士观点' in title:
        highlights = [
            f"【核心内容】{platform}专家观点：行业资深人士深度分析",
            "【亮点】独到见解、趋势预测、专业判断、战略建议",
            "【价值】获得专业视角的启发和思考"
        ]
    elif '爆款视频' in title or '热门内容' in title:
        highlights = [
            f"【核心内容】{platform}内容分析：爆款内容背后的逻辑",
            "【亮点】内容特征、传播路径、用户偏好、成功要素",
            "【价值】为内容创作提供参考和灵感"
        ]
    elif '创作者故事' in title or '网红成长' in title:
        highlights = [
            f"【核心内容】{platform}创作者生态：成功案例和成长历程",
            "【亮点】创业故事、发展策略、变现模式、经验总结",
            "【价值】了解内容创作者的成功路径"
        ]
    elif '趋势解读' in title or '流行趋势' in title:
        highlights = [
            f"【核心内容】{platform}趋势分析：{category}领域最新趋势",
            "【亮点】数据变化、热点迁移、用户偏好、市场机会",
            "【价值】把握趋势，提前布局"
        ]
    elif '用户行为' in title or '观看习惯' in title:
        highlights = [
            f"【核心内容】{platform}用户研究：用户行为和偏好分析",
            "【亮点】使用习惯、内容偏好、活跃时段、用户画像",
            "【价值】优化产品和运营策略"
        ]
    elif '商业化' in title or '变现模式' in title:
        highlights = [
            f"【核心内容】{platform}商业分析：变现模式和商业化探索",
            "【亮点】商业模式、收入来源、成功案例、增长策略",
            "【价值】为商业化提供参考和思路"
        ]
    elif '热点话题' in title:
        highlights = [
            f"【核心内容】{platform}热点追踪：最新热点话题汇总",
            "【亮点】话题背景、传播数据、用户反应、社会影响",
            "【价值】把握热点，及时跟进"
        ]
    elif '用户互动' in title or '评论分析' in title:
        highlights = [
            f"【核心内容】{platform}互动分析：用户评论和反馈研究",
            "【亮点】评论情感、用户观点、意见分布、互动特征",
            "【价值】了解用户真实想法和需求"
        ]
    elif '传播效果' in title or '传播路径' in title:
        highlights = [
            f"【核心内容】{platform}传播研究：内容传播机制和效果",
            "【亮点】传播路径、关键节点、转化效果、影响因素",
            "【价值】优化内容传播策略"
        ]
    elif '影响力' in title or '大V账号' in title:
        highlights = [
            f"【核心内容】{platform}账号分析：头部账号运营研究",
            "【亮点】内容策略、粉丝画像、互动数据、成功因素",
            "【价值】学习头部账号运营经验"
        ]
    elif '内容策略' in title or '运营方法论' in title:
        highlights = [
            f"【核心内容】{platform}运营指南：实战方法论和策略",
            "【亮点】运营技巧、内容规划、增长策略、实操案例",
            "【价值】提升运营能力和效果"
        ]
    elif '热门视频' in title or '趋势内容' in title:
        highlights = [
            f"【核心内容】{platform}视频趋势：全球热门视频内容",
            "【亮点】内容类型、创作风格、观众反馈、国际差异",
            "【价值】了解全球视频内容趋势"
        ]
    elif '创作者生态' in title or '内容生产者' in title:
        highlights = [
            f"【核心内容】{platform}创作者研究：内容生产者生态分析",
            "【亮点】创作者画像、收入模式、平台政策、发展趋势",
            "【价值】了解创作者生态和发展机会"
        ]
    elif '观看数据' in title or '用户行为分析' in title:
        highlights = [
            f"【核心内容】{platform}数据报告：用户观看行为深度分析",
            "【亮点】观看时长、内容偏好、付费习惯、地域分布",
            "【价值】基于数据优化内容和运营"
        ]
    elif '广告模式' in title or '商业化探索' in title:
        highlights = [
            f"【核心内容】{platform}商业研究：广告模式和商业化路径",
            "【亮点】广告形式、变现方式、收入结构、成功案例",
            "【价值】了解平台商业化模式和机会"
        ]
    elif '国际视野' in title or '全球内容趋势' in title:
        highlights = [
            f"【核心内容】{platform}全球观察：国际内容趋势分析",
            "【亮点】国际热点、文化差异、全球趋势、跨国案例",
            "【价值】拓展国际视野，发现新机会"
        ]
    else:
        highlights = [
            f"【核心内容】{platform}关于{category}的精彩内容",
            "【亮点】热点话题、用户关注、专业观点",
            "【价值】获取最新信息和洞察"
        ]
    
    # 添加热度信息
    highlights.insert(1, f"【热度】热度指数：{hotness}，{platform}平台推荐")
    
    record['内容亮点'] = '\n'.join(highlights)

# 保存更新后的数据
output_file = '/tmp/feishu_records_with_highlights.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(feishu_records, f, ensure_ascii=False, indent=2)

print(f"✅ 已为 {len(feishu_records)} 条记录生成内容亮点")
print(f"💾 数据已保存到: {output_file}")

# 显示前3条示例
print("\n📝 示例数据:")
for i, record in enumerate(feishu_records[:3]):
    print(f"\n{i+1}. {record['选题标题'][:50]}...")
    print(f"   平台: {record['来源平台']}")
    print(f"   亮点预览:")
    highlights_lines = record['内容亮点'].split('\n')
    for line in highlights_lines[:2]:
        print(f"     {line}")
