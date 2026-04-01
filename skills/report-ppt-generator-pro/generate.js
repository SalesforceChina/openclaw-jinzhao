const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const outputDir = '/tmp/ppt-output';

// Weekly work report data
const report = {
  title: '本周工作汇报',
  subtitle: '2026年第13周（3.31 - 4.4）',
  author: '产品研发部',
  date: '2026年4月1日',
  sections: [
    {
      title: '本周工作概览',
      items: [
        '完成用户调研报告初版，收集有效问卷 328 份',
        '推进后台管理系统 v2.3 版本迭代，已完成 UAT 测试',
        '参加行业峰会，分享技术实践心得',
        '优化核心算法性能，响应速度提升 40%'
      ]
    },
    {
      title: '项目进展',
      items: [
        '【后台管理系统】进度 85%，预计下周上线',
        '【数据看板】进度 60%，正在开发第三版图表组件',
        '【移动端优化】进度 45%，已完成首页重构'
      ]
    },
    {
      title: '下周计划',
      items: [
        '完成后台管理系统 v2.3 正式发布',
        '启动数据看板 Beta 用户测试',
        '开展移动端 A/B 测试方案设计',
        '筹备 Q2 产品规划会议'
      ]
    },
    {
      title: '需要协调事项',
      items: [
        '需市场部确认数据看板上线宣传方案',
        '需设计资源支持移动端新功能 UI',
        '建议召开跨部门项目进度同步会'
      ]
    }
  ]
};

// Create presentation
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = report.title;
pres.author = report.author;

// Color scheme
const colors = {
  primary: '1E3A8A',    // Deep blue
  secondary: '3B82F6',  // Bright blue
  accent: '60A5FA',     // Light blue
  background: 'FFFFFF',
  text: '1F2937',
  lightBg: 'F8FAFC'
};

// Helper function to add shadow
const makeShadow = () => ({
  type: 'outer',
  color: '000000',
  blur: 8,
  offset: 3,
  angle: 135,
  opacity: 0.12
});

// ============ Slide 1: Cover ============
let slide1 = pres.addSlide();
slide1.background = { color: colors.primary };

// Decorative shape - top right
slide1.addShape(pres.shapes.OVAL, {
  x: 7, y: -1.5, w: 5, h: 5,
  fill: { color: colors.secondary, transparency: 30 }
});

// Decorative shape - bottom left
slide1.addShape(pres.shapes.OVAL, {
  x: -1.5, y: 4, w: 4, h: 4,
  fill: { color: colors.accent, transparency: 40 }
});

// Main title
slide1.addText(report.title, {
  x: 0.5, y: 2.0, w: 9, h: 1.2,
  fontSize: 54, fontFace: 'Microsoft YaHei',
  color: 'FFFFFF', bold: true, align: 'center'
});

// Subtitle
slide1.addText(report.subtitle, {
  x: 0.5, y: 3.3, w: 9, h: 0.6,
  fontSize: 24, fontFace: 'Microsoft YaHei',
  color: colors.accent, align: 'center'
});

// Author and date
slide1.addText(`${report.author}  |  ${report.date}`, {
  x: 0.5, y: 4.5, w: 9, h: 0.5,
  fontSize: 16, fontFace: 'Microsoft YaHei',
  color: 'FFFFFF', align: 'center', transparency: 30
});

// ============ Slide 2: TOC ============
let slide2 = pres.addSlide();
slide2.background = { color: colors.background };

// Header bar
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 1.2,
  fill: { color: colors.primary }
});

slide2.addText('目录', {
  x: 0.6, y: 0.3, w: 3, h: 0.6,
  fontSize: 28, fontFace: 'Microsoft YaHei',
  color: 'FFFFFF', bold: true, margin: 0
});

// TOC items
const tocItems = [
  { num: '01', title: '本周工作概览' },
  { num: '02', title: '项目进展' },
  { num: '03', title: '下周计划' },
  { num: '04', title: '需要协调事项' }
];

tocItems.forEach((item, i) => {
  const y = 1.8 + i * 0.9;

  // Number circle
  slide2.addShape(pres.shapes.OVAL, {
    x: 1, y: y, w: 0.6, h: 0.6,
    fill: { color: colors.secondary }
  });

  slide2.addText(item.num, {
    x: 1, y: y + 0.05, w: 0.6, h: 0.5,
    fontSize: 16, fontFace: 'Microsoft YaHei',
    color: 'FFFFFF', bold: true, align: 'center', valign: 'middle', margin: 0
  });

  slide2.addText(item.title, {
    x: 1.8, y: y, w: 6, h: 0.6,
    fontSize: 22, fontFace: 'Microsoft YaHei',
    color: colors.text, valign: 'middle', margin: 0
  });

  // Divider line
  if (i < tocItems.length - 1) {
    slide2.addShape(pres.shapes.LINE, {
      x: 1.8, y: y + 0.7, w: 6, h: 0,
      line: { color: 'E5E7EB', width: 1 }
    });
  }
});

// ============ Slide 3: 本周工作概览 ============
let slide3 = pres.addSlide();
slide3.background = { color: colors.background };

// Left accent bar
slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.15, h: 5.625,
  fill: { color: colors.primary }
});

// Section number
slide3.addText('01', {
  x: 0.4, y: 0.3, w: 1, h: 0.6,
  fontSize: 36, fontFace: 'Microsoft YaHei',
  color: colors.secondary, bold: true, margin: 0
});

// Section title
slide3.addText('本周工作概览', {
  x: 1.4, y: 0.35, w: 4, h: 0.5,
  fontSize: 26, fontFace: 'Microsoft YaHei',
  color: colors.primary, bold: true, margin: 0
});

// Horizontal line
slide3.addShape(pres.shapes.LINE, {
  x: 0.4, y: 1.0, w: 9.2, h: 0,
  line: { color: colors.secondary, width: 2 }
});

// Content items - 2x2 grid
const overviewItems = report.sections[0].items;
const gridData = [
  { icon: '📊', title: '用户调研', desc: overviewItems[0] },
  { icon: '💻', title: '版本迭代', desc: overviewItems[1] },
  { icon: '🎤', title: '行业峰会', desc: overviewItems[2] },
  { icon: '⚡', title: '性能优化', desc: overviewItems[3] }
];

gridData.forEach((item, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const x = 0.5 + col * 4.7;
  const y = 1.4 + row * 2.0;

  // Card background
  slide3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: x, y: y, w: 4.4, h: 1.7,
    fill: { color: colors.lightBg },
    rectRadius: 0.1,
    shadow: makeShadow()
  });

  // Icon
  slide3.addText(item.icon, {
    x: x + 0.2, y: y + 0.2, w: 0.6, h: 0.6,
    fontSize: 28, align: 'center', margin: 0
  });

  // Title
  slide3.addText(item.title, {
    x: x + 0.9, y: y + 0.25, w: 3.3, h: 0.4,
    fontSize: 18, fontFace: 'Microsoft YaHei',
    color: colors.primary, bold: true, margin: 0
  });

  // Description
  slide3.addText(item.desc, {
    x: x + 0.2, y: y + 0.75, w: 4.0, h: 0.8,
    fontSize: 13, fontFace: 'Microsoft YaHei',
    color: colors.text, margin: 0
  });
});

// ============ Slide 4: 项目进展 ============
let slide4 = pres.addSlide();
slide4.background = { color: colors.background };

// Left accent bar
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.15, h: 5.625,
  fill: { color: colors.primary }
});

// Section number
slide4.addText('02', {
  x: 0.4, y: 0.3, w: 1, h: 0.6,
  fontSize: 36, fontFace: 'Microsoft YaHei',
  color: colors.secondary, bold: true, margin: 0
});

// Section title
slide4.addText('项目进展', {
  x: 1.4, y: 0.35, w: 4, h: 0.5,
  fontSize: 26, fontFace: 'Microsoft YaHei',
  color: colors.primary, bold: true, margin: 0
});

// Horizontal line
slide4.addShape(pres.shapes.LINE, {
  x: 0.4, y: 1.0, w: 9.2, h: 0,
  line: { color: colors.secondary, width: 2 }
});

// Project items
const projects = [
  { name: '后台管理系统 v2.3', progress: 85, status: '预计下周上线', color: '22C55E' },
  { name: '数据看板', progress: 60, status: '开发图表组件中', color: 'F59E0B' },
  { name: '移动端优化', progress: 45, status: '已完成首页重构', color: '3B82F6' }
];

projects.forEach((proj, i) => {
  const y = 1.3 + i * 1.35;

  // Card
  slide4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 1.15,
    fill: { color: colors.lightBg },
    rectRadius: 0.08,
    shadow: makeShadow()
  });

  // Project name
  slide4.addText(proj.name, {
    x: 0.7, y: y + 0.15, w: 4, h: 0.4,
    fontSize: 18, fontFace: 'Microsoft YaHei',
    color: colors.primary, bold: true, margin: 0
  });

  // Status
  slide4.addText(proj.status, {
    x: 0.7, y: y + 0.55, w: 4, h: 0.4,
    fontSize: 13, fontFace: 'Microsoft YaHei',
    color: colors.text, margin: 0
  });

  // Progress bar background
  slide4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 5.5, y: y + 0.35, w: 3.5, h: 0.35,
    fill: { color: 'E5E7EB' },
    rectRadius: 0.05
  });

  // Progress bar fill
  slide4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 5.5, y: y + 0.35, w: 3.5 * (proj.progress / 100), h: 0.35,
    fill: { color: proj.color },
    rectRadius: 0.05
  });

  // Progress text
  slide4.addText(`${proj.progress}%`, {
    x: 5.5, y: y + 0.35, w: 3.5, h: 0.35,
    fontSize: 14, fontFace: 'Microsoft YaHei',
    color: proj.progress > 50 ? 'FFFFFF' : colors.text,
    bold: true, align: 'center', valign: 'middle', margin: 0
  });
});

// ============ Slide 5: 下周计划 ============
let slide5 = pres.addSlide();
slide5.background = { color: colors.background };

// Left accent bar
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.15, h: 5.625,
  fill: { color: colors.primary }
});

// Section number
slide5.addText('03', {
  x: 0.4, y: 0.3, w: 1, h: 0.6,
  fontSize: 36, fontFace: 'Microsoft YaHei',
  color: colors.secondary, bold: true, margin: 0
});

// Section title
slide5.addText('下周计划', {
  x: 1.4, y: 0.35, w: 4, h: 0.5,
  fontSize: 26, fontFace: 'Microsoft YaHei',
  color: colors.primary, bold: true, margin: 0
});

// Horizontal line
slide5.addShape(pres.shapes.LINE, {
  x: 0.4, y: 1.0, w: 9.2, h: 0,
  line: { color: colors.secondary, width: 2 }
});

// Plan items with timeline
const plans = report.sections[2].items;
plans.forEach((plan, i) => {
  const y = 1.3 + i * 1.0;

  // Timeline dot
  slide5.addShape(pres.shapes.OVAL, {
    x: 0.7, y: y + 0.15, w: 0.3, h: 0.3,
    fill: { color: colors.secondary }
  });

  // Timeline line
  if (i < plans.length - 1) {
    slide5.addShape(pres.shapes.LINE, {
      x: 0.85, y: y + 0.45, w: 0, h: 0.55,
      line: { color: colors.accent, width: 2 }
    });
  }

  // Plan text
  slide5.addText(plan, {
    x: 1.2, y: y, w: 8, h: 0.6,
    fontSize: 18, fontFace: 'Microsoft YaHei',
    color: colors.text, valign: 'middle', margin: 0
  });
});

// ============ Slide 6: 需要协调事项 ============
let slide6 = pres.addSlide();
slide6.background = { color: colors.background };

// Left accent bar
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 0.15, h: 5.625,
  fill: { color: colors.primary }
});

// Section number
slide6.addText('04', {
  x: 0.4, y: 0.3, w: 1, h: 0.6,
  fontSize: 36, fontFace: 'Microsoft YaHei',
  color: colors.secondary, bold: true, margin: 0
});

// Section title
slide6.addText('需要协调事项', {
  x: 1.4, y: 0.35, w: 4, h: 0.5,
  fontSize: 26, fontFace: 'Microsoft YaHei',
  color: colors.primary, bold: true, margin: 0
});

// Horizontal line
slide6.addShape(pres.shapes.LINE, {
  x: 0.4, y: 1.0, w: 9.2, h: 0,
  line: { color: colors.secondary, width: 2 }
});

// Coordination items
const coords = report.sections[3].items;
coords.forEach((item, i) => {
  const y = 1.3 + i * 1.0;

  // Warning icon shape
  slide6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.6, y: y + 0.05, w: 0.5, h: 0.5,
    fill: { color: 'FEF3C7' },
    rectRadius: 0.05
  });

  slide6.addText('!', {
    x: 0.6, y: y + 0.05, w: 0.5, h: 0.5,
    fontSize: 20, fontFace: 'Microsoft YaHei',
    color: 'D97706', bold: true, align: 'center', valign: 'middle', margin: 0
  });

  // Text
  slide6.addText(item, {
    x: 1.3, y: y, w: 8, h: 0.6,
    fontSize: 18, fontFace: 'Microsoft YaHei',
    color: colors.text, valign: 'middle', margin: 0
  });
});

// ============ Slide 7: Thank You ============
let slide7 = pres.addSlide();
slide7.background = { color: colors.primary };

// Decorative circles
slide7.addShape(pres.shapes.OVAL, {
  x: -2, y: -2, w: 6, h: 6,
  fill: { color: colors.secondary, transparency: 30 }
});

slide7.addShape(pres.shapes.OVAL, {
  x: 7, y: 3, w: 5, h: 5,
  fill: { color: colors.accent, transparency: 40 }
});

// Thank you text
slide7.addText('感谢聆听', {
  x: 0.5, y: 2.0, w: 9, h: 1.0,
  fontSize: 56, fontFace: 'Microsoft YaHei',
  color: 'FFFFFF', bold: true, align: 'center'
});

// Subtitle
slide7.addText('欢迎提问与交流', {
  x: 0.5, y: 3.2, w: 9, h: 0.6,
  fontSize: 24, fontFace: 'Microsoft YaHei',
  color: colors.accent, align: 'center'
});

// Save the file
const outputPath = path.join(outputDir, '本周工作汇报.pptx');
pres.writeFile({ fileName: outputPath })
  .then(() => {
    console.log('PPT generated successfully: ' + outputPath);
  })
  .catch(err => {
    console.error('Error generating PPT:', err);
  });
