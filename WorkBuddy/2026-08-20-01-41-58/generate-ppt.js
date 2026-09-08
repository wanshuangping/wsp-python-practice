const pptxgen = require("pptxgenjs");

const C = {
  primary: "1E3A8A",
  secondary: "3B82F6",
  accent: "06B6D4",
  light: "E0F2FE",
  darkText: "1E293B",
  muted: "64748B",
  bgLight: "F8FAFC",
  darkBg: "0F172A",
  white: "FFFFFF",
  coral: "F43F5E",
  amber: "F59E0B",
  emerald: "10B981",
};

const FONT_CN = "Microsoft YaHei";

function freshShadow() {
  return { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.12 };
}

function addFooter(slide, dark = false) {
  slide.addText("易观分析 | 中国办公智能体市场洞察 | 2026.5", {
    x: 0.5, y: 5.25, w: 9, h: 0.25,
    fontSize: 9, fontFace: FONT_CN, color: dark ? "94A3B8" : C.muted,
  });
  slide.addText("数据来源：易观办公智能体平台用户调研（N=500），2026年5月；公开资料整理", {
    x: 0.5, y: 5.25, w: 9, h: 0.25, align: "right",
    fontSize: 9, fontFace: FONT_CN, color: dark ? "94A3B8" : C.muted,
  });
}

function addSlideTitle(slide, title, subtitle = null, dark = false) {
  slide.addText(title, {
    x: 0.5, y: 0.45, w: 9, h: 0.55,
    fontSize: 28, fontFace: FONT_CN, bold: true, color: dark ? C.white : C.primary,
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.5, y: 1.0, w: 9, h: 0.35,
      fontSize: 14, fontFace: FONT_CN, color: dark ? "CBD5E1" : C.muted,
    });
  }
}

function chartOptions(opts = {}) {
  return {
    x: 0.5, y: 1.5, w: 9, h: 3.6,
    chartColors: [C.secondary, C.accent, C.primary, C.coral, C.emerald, C.amber],
    chartArea: { fill: { color: C.white }, roundedCorners: false },
    catAxisLabelColor: C.muted,
    valAxisLabelColor: C.muted,
    valGridLine: { color: "E2E8F0", size: 0.5 },
    catGridLine: { style: "none" },
    showLegend: false,
    showValue: true,
    dataLabelColor: C.darkText,
    dataLabelFontSize: 10,
    dataLabelPosition: "outEnd",
    barGapWidthPct: 35,
    ...opts,
  };
}

function hbarChart(data, labels, opts = {}) {
  return [[{
    name: "数值",
    labels,
    values: data,
  }], chartOptions({ barDir: "bar", ...opts })];
}

function vbarChart(data, labels, opts = {}) {
  return [[{
    name: "数值",
    labels,
    values: data,
  }], chartOptions({ barDir: "col", ...opts })];
}

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "WorkBuddy";
pres.title = "中国办公智能体市场洞察";
pres.subject = "基于易观分析2026年5月报告";

// ---------- 1. Cover ----------
let s1 = pres.addSlide();
s1.background = { color: C.darkBg };
s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.darkBg } });
s1.addShape(pres.shapes.RECTANGLE, { x: 0, y: 4.6, w: 10, h: 1.025, fill: { color: C.primary } });
s1.addText("中国办公智能体市场洞察", {
  x: 0.7, y: 1.6, w: 8.6, h: 1.0,
  fontSize: 44, fontFace: FONT_CN, bold: true, color: C.white,
});
s1.addText("Workspace Agents: 从工具智能到行动智能的跃迁", {
  x: 0.7, y: 2.7, w: 8.6, h: 0.5,
  fontSize: 18, fontFace: FONT_CN, color: C.accent,
});
s1.addText("基于易观分析 2026 年 5 月报告整理", {
  x: 0.7, y: 3.3, w: 8.6, h: 0.4,
  fontSize: 14, fontFace: FONT_CN, color: "94A3B8",
});
s1.addText("2026 年 8 月", {
  x: 0.7, y: 4.85, w: 8.6, h: 0.35,
  fontSize: 14, fontFace: FONT_CN, color: C.white,
});

// ---------- 2. Agenda ----------
let s2 = pres.addSlide();
s2.background = { color: C.bgLight };
addSlideTitle(s2, "报告结构", null, false);
const agendaItems = [
  { num: "01", title: "市场概览", desc: "定义、能力边界、产品分类、生态与挑战" },
  { num: "02", title: "用户洞察", desc: "用户画像、使用习惯、场景、付费与瓶颈" },
  { num: "03", title: "桌面端爆发与未来", desc: "桌面端价值、增长动能与未来竞争关键" },
];
agendaItems.forEach((item, i) => {
  const y = 1.7 + i * 1.15;
  s2.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y, w: 8.6, h: 0.95, fill: { color: C.white },
    line: { color: "E2E8F0", width: 1 }, shadow: freshShadow(),
  });
  s2.addShape(pres.shapes.RECTANGLE, { x: 0.7, y, w: 0.12, h: 0.95, fill: { color: C.secondary } });
  s2.addText(item.num, { x: 1.0, y, w: 0.7, h: 0.95, fontSize: 28, fontFace: FONT_CN, bold: true, color: C.secondary, valign: "middle" });
  s2.addText(item.title, { x: 1.9, y: y + 0.18, w: 3, h: 0.35, fontSize: 20, fontFace: FONT_CN, bold: true, color: C.darkText });
  s2.addText(item.desc, { x: 1.9, y: y + 0.52, w: 6.8, h: 0.3, fontSize: 13, fontFace: FONT_CN, color: C.muted });
});
addFooter(s2);

// ---------- 3. Section 01 ----------
let s3 = pres.addSlide();
s3.background = { color: C.primary };
s3.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.primary } });
s3.addText("01", { x: 0.7, y: 1.9, w: 8.6, h: 1.0, fontSize: 72, fontFace: FONT_CN, bold: true, color: C.white });
s3.addText("市场概览", { x: 0.7, y: 2.9, w: 8.6, h: 0.8, fontSize: 40, fontFace: FONT_CN, bold: true, color: C.white });
s3.addText("定义演进 · 产品分类 · 生态格局 · 核心挑战", { x: 0.7, y: 3.7, w: 8.6, h: 0.4, fontSize: 16, fontFace: FONT_CN, color: C.light });

// ---------- 4. Definition ----------
let s4 = pres.addSlide();
s4.background = { color: C.bgLight };
addSlideTitle(s4, "办公智能体研究界定", "以 AI 为核心，面向办公场景提供任务自动化、工作流编排与信息处理服务的智能体产品");
s4.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.45, w: 8.8, h: 2.4, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
s4.addText("核心定义", { x: 0.85, y: 1.6, w: 8.3, h: 0.35, fontSize: 16, fontFace: FONT_CN, bold: true, color: C.primary });
s4.addText("面向办公场景用户，提供任务自动化、工作流编排与信息处理服务的智能体产品；研究范围覆盖具备独立操作空间与执行能力的独立智能体，以及平台级智能体。", {
  x: 0.85, y: 1.95, w: 8.3, h: 0.7, fontSize: 13, fontFace: FONT_CN, color: C.darkText,
});
const defCaps = [
  ["任务自主执行", "接受用户指令，自主拆解目标、规划步骤并调用工具完成多步骤任务"],
  ["办公场景适配", "在文档处理、代码开发、数据分析、会议管理、日程安排等场景实现自动化"],
  ["多系统集成", "与操作系统、企业应用、第三方工具交互，实现跨系统数据同步与流程联动"],
  ["资源与生态", "具备丰富的技能库、插件生态或模型接入能力，支持第三方开发者扩展"],
];
defCaps.forEach((c, i) => {
  const x = 0.6 + (i % 2) * 4.5;
  const y = 3.9 + Math.floor(i / 2) * 0.7;
  s4.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.08, h: 0.55, fill: { color: C.accent } });
  s4.addText(c[0], { x: x + 0.18, y, w: 1.8, h: 0.3, fontSize: 13, fontFace: FONT_CN, bold: true, color: C.darkText });
  s4.addText(c[1], { x: x + 0.18, y: y + 0.28, w: 4.1, h: 0.35, fontSize: 11, fontFace: FONT_CN, color: C.muted });
});
addFooter(s4);

// ---------- 5. Capability evolution ----------
let s5 = pres.addSlide();
s5.background = { color: C.bgLight };
addSlideTitle(s5, "能力边界：从“工具智能”向“行动智能”跃迁", "2026 年，多模态大模型在推理、规划与工具调用上实现突破");
const trends = [
  { title: "大模型推理增强", desc: "GPT、Claude、DeepSeek、Qwen 等在长程推理与多步规划上显著进步，可将复杂任务分解为可执行中间步骤。" },
  { title: "工具调用标准化", desc: "主流大模型 API 支持结构化工具调用，使 Agent 能更精准、可靠地与文件系统、浏览器及外部 API 交互。" },
  { title: "多模态 GUI 理解", desc: "Agent 能够“读懂”屏幕内容、识别图标与按钮含义、感知操作结果，桌面端全场景自动化成为可能。" },
];
trends.forEach((t, i) => {
  const y = 1.45 + i * 0.78;
  s5.addShape(pres.shapes.OVAL, { x: 0.65, y: y + 0.08, w: 0.28, h: 0.28, fill: { color: C.secondary } });
  s5.addText(String(i + 1), { x: 0.65, y: y + 0.08, w: 0.28, h: 0.28, align: "center", valign: "middle", fontSize: 13, fontFace: FONT_CN, bold: true, color: C.white });
  s5.addText(t.title, { x: 1.1, y, w: 8.0, h: 0.3, fontSize: 15, fontFace: FONT_CN, bold: true, color: C.darkText });
  s5.addText(t.desc, { x: 1.1, y: y + 0.32, w: 8.0, h: 0.4, fontSize: 12, fontFace: FONT_CN, color: C.muted });
});
const benchData = [
  ["基准测试", "测试内容", "智能体表现"],
  ["GAIA（通用助手任务）", "面向真实工作场景的综合任务评估", "74.5%"],
  ["OSWorld（操作系统任务）", "在虚拟操作系统环境中完成真实用户任务", "66.3%"],
  ["WebArena（网络任务）", "在真实网站环境中完成多步骤网络任务", "74.3%"],
];
s5.addTable(benchData, {
  x: 0.6, y: 3.85, w: 8.8, h: 1.1,
  colW: [2.6, 4.4, 1.8],
  border: { pt: 0.5, color: "E2E8F0" },
  fill: { color: C.white },
  fontFace: FONT_CN,
  fontSize: 11,
  color: C.darkText,
});
addFooter(s5);

// ---------- 6. Demand upgrade ----------
let s6 = pres.addSlide();
s6.background = { color: C.bgLight };
addSlideTitle(s6, "办公智能化需求升级", "智能体成为重构工作方式的关键变量");
const stages = [
  { name: "连接", desc: "远程办公/混合办公成为常态，核心是解决远程协作与信息同步" },
  { name: "生成", desc: "从海量信息中提取所需，搜索与摘要需求上升，AI 辅助提升内容生成效率" },
  { name: "调用", desc: "流程自动化与智能化需求凸显，生成式 AI 嵌入工作流，AI 协助完成部分工作" },
  { name: "规划与执行", desc: "需求进一步向具备任务自主规划、理解目标并拆解任务、多工具调用与协同演进" },
];
stages.forEach((st, i) => {
  const x = 0.55 + i * 2.25;
  s6.addShape(pres.shapes.RECTANGLE, { x, y: 1.55, w: 2.05, h: 2.0, fill: { color: i === 3 ? C.primary : C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
  s6.addText(st.name, { x, y: 1.68, w: 2.05, h: 0.4, align: "center", fontSize: 17, fontFace: FONT_CN, bold: true, color: i === 3 ? C.white : C.secondary });
  s6.addText(st.desc, { x: x + 0.1, y: 2.15, w: 1.85, h: 1.2, align: "center", fontSize: 11, fontFace: FONT_CN, color: i === 3 ? "E2E8F0" : C.muted });
  if (i < 3) {
    s6.addShape(pres.shapes.LINE, { x: x + 2.07, y: 2.55, w: 0.18, h: 0, line: { color: C.accent, width: 2 } });
    s6.addText(">", { x: x + 2.0, y: 2.35, w: 0.2, h: 0.2, align: "center", valign: "middle", fontSize: 14, fontFace: FONT_CN, bold: true, color: C.accent });
  }
});
const msData = [
  ["企业管理者对 Agent 的预期", "比例"],
  ["构建多智能体系统以自动化复杂任务", "42%"],
  ["训练智能体", "41%"],
  ["管理智能体", "38%"],
  ["用 AI 重新设计业务流程", "36%"],
];
s6.addText("企业管理者对 Agent 在团队管理中应用的预期", { x: 0.6, y: 3.75, w: 8.8, h: 0.3, fontSize: 12, fontFace: FONT_CN, bold: true, color: C.darkText });
s6.addTable(msData, {
  x: 0.6, y: 3.95, w: 8.8, h: 1.1,
  colW: [7.0, 1.8],
  border: { pt: 0.5, color: "E2E8F0" }, fill: { color: C.white },
  fontFace: FONT_CN, fontSize: 11, color: C.darkText,
});
addFooter(s6);

// ---------- 7. Product classification ----------
let s7 = pres.addSlide();
s7.background = { color: C.bgLight };
addSlideTitle(s7, "办公智能体平台产品的主要分类与特征", "市场已形成三条相对清晰的产品路线");
const prodTypes = [
  { title: "AI 原生办公智能体", sub: "目标驱动，实现任务闭环", desc: "从“任务闭环”出发设计产品，让 AI 替代用户完成完整工作流，适合跨应用、多步骤、有明确交付物的复杂任务。", examples: "Manus、Cursor、Claude Code、Codex、WorkBuddy" },
  { title: "AI 通用对话智能体", sub: "对话驱动，知识获取", desc: "核心价值在于降低信息获取，适合知识问答、内容草稿生成、创意发散、学习与研究辅助等以信息获取为核心的任务。", examples: "豆包、ChatGPT、Kimi、Claude、Gemini、Grok" },
  { title: "办公软件内嵌智能体", sub: "场景触发，即时辅助", desc: "从“现有工作流优化”出发，在不改变用户习惯的前提下提供即时辅助，适合特定应用内的标准化、重复性操作。", examples: "飞书、钉钉、WPS AI、Microsoft Copilot、Notion" },
];
prodTypes.forEach((p, i) => {
  const x = 0.55 + i * 3.05;
  s7.addShape(pres.shapes.RECTANGLE, { x, y: 1.55, w: 2.85, h: 3.2, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
  s7.addShape(pres.shapes.RECTANGLE, { x, y: 1.55, w: 2.85, h: 0.55, fill: { color: i === 0 ? C.primary : (i === 1 ? C.secondary : C.accent) } });
  s7.addText(p.title, { x, y: 1.62, w: 2.85, h: 0.35, align: "center", fontSize: 15, fontFace: FONT_CN, bold: true, color: C.white });
  s7.addText(p.sub, { x: x + 0.12, y: 2.2, w: 2.61, h: 0.3, fontSize: 12, fontFace: FONT_CN, bold: true, color: C.darkText });
  s7.addText(p.desc, { x: x + 0.12, y: 2.55, w: 2.61, h: 1.3, fontSize: 11, fontFace: FONT_CN, color: C.muted });
  s7.addText("典型产品", { x: x + 0.12, y: 3.9, w: 2.61, h: 0.25, fontSize: 11, fontFace: FONT_CN, bold: true, color: C.darkText });
  s7.addText(p.examples, { x: x + 0.12, y: 4.15, w: 2.61, h: 0.45, fontSize: 10, fontFace: FONT_CN, color: C.muted });
});
addFooter(s7);

// ---------- 8. Six capabilities ----------
let s8 = pres.addSlide();
s8.background = { color: C.bgLight };
addSlideTitle(s8, "六大能力层级协同驱动", "构建办公智能体自主执行闭环");
const caps = [
  ["系统集成与调用", "读写本地文件、调用系统 API、操控浏览器与办公软件、跨应用数据流转"],
  ["直接交付可用成果", "文档稿、数据表、流程页等输出形态，将“辅助办公”升级为“替代执行”"],
  ["深度理解业务语境", "行业、岗位、企业特有规则与知识，提供精准上下文服务"],
  ["持续进化", "基于反馈优化任务规划与执行策略，自动吸收新信息、优化交互"],
  ["开放 Skill 生态", "构建技能框架、训练专属技能、通过自然语言生成个人技能"],
  ["端到端安全", "本地敏感数据不上云、端云加密传输、权限与日志审计"],
];
caps.forEach((c, i) => {
  const x = 0.55 + (i % 3) * 3.05;
  const y = 1.55 + Math.floor(i / 3) * 1.7;
  s8.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.85, h: 1.5, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
  s8.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.1, h: 1.5, fill: { color: C.secondary } });
  s8.addText(c[0], { x: x + 0.2, y: y + 0.15, w: 2.55, h: 0.35, fontSize: 14, fontFace: FONT_CN, bold: true, color: C.darkText });
  s8.addText(c[1], { x: x + 0.2, y: y + 0.55, w: 2.55, h: 0.85, fontSize: 11, fontFace: FONT_CN, color: C.muted });
});
addFooter(s8);

// ---------- 9. Value delivery ----------
let s9 = pres.addSlide();
s9.background = { color: C.bgLight };
addSlideTitle(s9, "从卖工具到卖结果", "办公智能体的价值交付革命");
const models = [
  { title: "订阅制", desc: "用户购买的是“持续进化的能力”，费用与智能体完成任务的质量挂钩。", target: "普通用户、中小企业" },
  { title: "Token 用量计费", desc: "调用量优先模型完成指令，用户感知付费单元为“任务/额度”而非 Token。", target: "个人开发者等深度用户" },
  { title: "Skill/插件付费", desc: "按 Skill 订阅或调用次数计费，Skill 生态丰富度构成核心壁垒。", target: "长尾/垂直场景用户" },
  { title: "私有化部署", desc: "政企客户对数据安全、合规审计的强需求驱动，国产大模型在私有化场景更具成本优势。", target: "大型政企客户" },
];
models.forEach((m, i) => {
  const x = 0.55 + i * 2.25;
  s9.addShape(pres.shapes.RECTANGLE, { x, y: 1.55, w: 2.05, h: 2.6, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
  s9.addShape(pres.shapes.OVAL, { x: x + 0.75, y: 1.75, w: 0.55, h: 0.55, fill: { color: [C.primary, C.secondary, C.accent, C.coral][i] } });
  s9.addText(String(i + 1), { x: x + 0.75, y: 1.75, w: 0.55, h: 0.55, align: "center", valign: "middle", fontSize: 18, fontFace: FONT_CN, bold: true, color: C.white });
  s9.addText(m.title, { x, y: 2.45, w: 2.05, h: 0.35, align: "center", fontSize: 15, fontFace: FONT_CN, bold: true, color: C.darkText });
  s9.addText(m.desc, { x: x + 0.1, y: 2.85, w: 1.85, h: 0.9, align: "center", fontSize: 10, fontFace: FONT_CN, color: C.muted });
  s9.addText(m.target, { x: x + 0.1, y: 3.8, w: 1.85, h: 0.25, align: "center", fontSize: 10, fontFace: FONT_CN, bold: true, color: C.secondary });
});
s9.addText("价值交换逻辑变化：从功能权限付费 → 为节省的时间与获得的成果付费", {
  x: 0.6, y: 4.4, w: 8.8, h: 0.4, align: "center", fontSize: 14, fontFace: FONT_CN, bold: true, color: C.primary,
});
addFooter(s9);

// ---------- 10. Ecosystem ----------
let s10 = pres.addSlide();
s10.background = { color: C.bgLight };
addSlideTitle(s10, "中国办公智能体产业生态图谱", "多元玩家共同塑造市场格局");
const ecoLayers = [
  { layer: "应用层", color: C.primary, items: ["AI 原生：Manus、Cursor、Claude Code、Codex、CodeBuddy、WorkBuddy", "通用对话：豆包、Kimi、ChatGPT、Claude、Gemini、Grok", "办公嵌入：飞书、钉钉、WPS AI、Copilot、Notion"] },
  { layer: "基础设施与工具", color: C.secondary, items: ["开源框架：OpenClaw、Hermes Agent、CrewClaw、PicoClaw、ZeroClaw", "开发工具：LangChain、AutoGen、LlamaIndex、Make、Zapier", "Agent 分发：扣子、腾讯元器、ModelScope、SkillHub"] },
  { layer: "基础模型", color: C.accent, items: ["DeepSeek、智谱、MiniMax、Kimi、通义千问、豆包、腾讯混元、文心、OpenAI、Google、Anthropic、Meta"] },
];
ecoLayers.forEach((e, i) => {
  const y = 1.55 + i * 1.15;
  s10.addShape(pres.shapes.RECTANGLE, { x: 0.6, y, w: 1.6, h: 0.9, fill: { color: e.color } });
  s10.addText(e.layer, { x: 0.6, y, w: 1.6, h: 0.9, align: "center", valign: "middle", fontSize: 14, fontFace: FONT_CN, bold: true, color: C.white });
  e.items.forEach((it, j) => {
    s10.addText(it, { x: 2.35, y: y + j * 0.28, w: 7.0, h: 0.32, fontSize: 10, fontFace: FONT_CN, color: C.darkText });
  });
});
addFooter(s10);

// ---------- 11. China vs US + challenges ----------
let s11 = pres.addSlide();
s11.background = { color: C.bgLight };
addSlideTitle(s11, "中美市场特征对比与核心挑战", "不同市场土壤塑造差异化发展路径");
const compareData = [
  ["维度", "美国", "中国"],
  ["场景切入", "高价值、高复杂度的垂直场景，如代码生成、法律文书", "通用办公场景为主，依托庞大用户基数快速市场教育"],
  ["核心用户", "开发者、IT 与研发部门，愿为生产力工具支付高费用", "白领群体为主，通过免费/低门槛方式快速渗透大众市场"],
  ["产品策略", "“单点极致”的垂直化定位，建立技术壁垒", "“通用平台型”，强调一站式集成多种 Agent 能力"],
  ["竞争逻辑", "模型深度与专业数据壁垒，构建护城河", "生态壁垒与流量分发效率，插件生态与应用场景丰富度"],
];
s11.addTable(compareData, {
  x: 0.55, y: 1.5, w: 5.5, h: 3.4,
  colW: [1.0, 2.25, 2.25],
  border: { pt: 0.5, color: "E2E8F0" }, fill: { color: C.white },
  fontFace: FONT_CN, fontSize: 10, color: C.darkText,
});
const challenges = [
  "长期推理与执行可靠性仍不稳定，幻觉和错误累积影响复杂任务",
  "平台互操作标准缺失与生态割裂，插件迁移成本高",
  "高价值场景数据孤岛问题严重，深度集成成本高、接口标准化程度低",
];
s11.addShape(pres.shapes.RECTANGLE, { x: 6.25, y: 1.5, w: 3.2, h: 3.4, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
s11.addText("核心挑战", { x: 6.4, y: 1.65, w: 2.9, h: 0.35, fontSize: 15, fontFace: FONT_CN, bold: true, color: C.coral });
challenges.forEach((c, i) => {
  s11.addShape(pres.shapes.OVAL, { x: 6.45, y: 2.15 + i * 0.85, w: 0.18, h: 0.18, fill: { color: C.coral } });
  s11.addText(c, { x: 6.75, y: 2.05 + i * 0.85, w: 2.55, h: 0.65, fontSize: 11, fontFace: FONT_CN, color: C.darkText });
});
addFooter(s11);

// ---------- 12. Section 02 ----------
let s12 = pres.addSlide();
s12.background = { color: C.secondary };
s12.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.secondary } });
s12.addText("02", { x: 0.7, y: 1.9, w: 8.6, h: 1.0, fontSize: 72, fontFace: FONT_CN, bold: true, color: C.white });
s12.addText("用户洞察", { x: 0.7, y: 2.9, w: 8.6, h: 0.8, fontSize: 40, fontFace: FONT_CN, bold: true, color: C.white });
s12.addText("用户画像 · 使用习惯 · 场景渗透 · 付费与瓶颈", { x: 0.7, y: 3.7, w: 8.6, h: 0.4, fontSize: 16, fontFace: FONT_CN, color: C.light });

// ---------- 13. User profile ----------
let s13 = pres.addSlide();
s13.background = { color: C.bgLight };
addSlideTitle(s13, "用户群体以职场中青年为主", "社交内容平台与同事推荐是主要触达渠道");
s13.addChart(pres.charts.BAR, ...hbarChart([11, 35, 45, 9], ["18-24岁", "25-29岁", "30-39岁", "40岁+"], { x: 0.55, y: 1.5, w: 2.8, h: 3.1, title: "用户年龄分布", showValue: true, dataLabelPosition: "outEnd", chartColors: [C.secondary] }));
s13.addChart(pres.charts.BAR, ...hbarChart([31, 22, 20, 11, 10, 4, 2], ["企业白领", "IT开发", "产品经理", "内容创作", "学生", "教育培训", "企业管理者"], { x: 3.55, y: 1.5, w: 2.9, h: 3.1, title: "用户职业分布", showValue: true, dataLabelPosition: "outEnd", chartColors: [C.accent] }));
s13.addChart(pres.charts.BAR, ...hbarChart([34, 23, 15, 15, 8, 3, 2], ["社交媒体/内容平台", "同事/朋友推荐", "开源社区", "公司统一要求", "产品官方发布", "媒体报道", "搜索引擎"], { x: 6.65, y: 1.5, w: 2.8, h: 3.1, title: "了解/开始使用渠道", showValue: true, dataLabelPosition: "outEnd", chartColors: [C.primary] }));
s13.addText("25-39 岁用户合计占比达 80%，构成办公智能体使用的绝对主体", {
  x: 0.6, y: 4.75, w: 8.8, h: 0.25, align: "center", fontSize: 13, fontFace: FONT_CN, bold: true, color: C.darkText,
});
addFooter(s13);

// ---------- 14. Usage habits ----------
let s14 = pres.addSlide();
s14.background = { color: C.bgLight };
addSlideTitle(s14, "效率提升是核心诉求，稳定使用习惯正在形成", "但使用深度仍受限于产品实际执行能力");
s14.addChart(pres.charts.BAR, ...hbarChart([51, 41, 39, 34, 28, 14, 11], ["工作提效", "减少重复性任务", "获取专业知识", "激发灵感", "完成多工具任务", "追踪任务结果", "协同办公"], { x: 0.55, y: 1.5, w: 4.5, h: 3.2, title: "用户使用主要目的", showValue: true, chartColors: [C.secondary] }));
s14.addChart(pres.charts.BAR, ...hbarChart([49, 29, 27, 11], ["网页端使用", "桌面端独立使用", "办公软件插件", "自行部署框架"], { x: 5.35, y: 1.5, w: 2.0, h: 1.5, title: "使用方式", showValue: true, chartColors: [C.accent] }));
s14.addChart(pres.charts.BAR, ...hbarChart([29, 46, 22, 3], ["每天使用", "每周3-4次", "每周1-2次", "每周几次"], { x: 5.35, y: 3.2, w: 2.0, h: 1.4, title: "使用频率", showValue: true, chartColors: [C.primary] }));
s14.addText("每天使用与每周 3-4 次的高频使用者合计超过七成", {
  x: 5.35, y: 4.75, w: 4.0, h: 0.25, fontSize: 12, fontFace: FONT_CN, bold: true, color: C.darkText,
});
addFooter(s14);

// ---------- 15. Application scenarios ----------
let s15 = pres.addSlide();
s15.background = { color: C.bgLight };
addSlideTitle(s15, "主流应用场景仍以问答交互为主", "深度任务渗透空间有望进一步打开");
s15.addChart(pres.charts.BAR, ...hbarChart([52, 43, 43, 36, 34, 32, 27, 24, 24, 14, 10, 10, 2], ["信息检索", "方案策划", "文档处理", "数据分析", "内容生成", "日程管理", "作业/论文", "编程辅助", "文件管理", "项目管理", "翻译", "沟通/任务", "客服/销售"], { x: 0.55, y: 1.5, w: 5.0, h: 3.7, title: "主要应用场景", showValue: true, chartColors: [C.secondary] }));
s15.addShape(pres.shapes.RECTANGLE, { x: 5.75, y: 1.5, w: 3.7, h: 3.7, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
const insights = [
  ["问答交互仍是基本盘", "满足轻量级、即时性辅助需求，但本质是问答交互延伸"],
  ["桌面端“原生代理”能力显现", "编程辅助、电脑文件整理等场景已积累可观使用占比"],
  ["垂直协作场景受限于工具链深度", "项目管理、客服销售等场景依赖企业存量业务系统无缝集成"],
];
insights.forEach((ins, i) => {
  const y = 1.75 + i * 1.1;
  s15.addShape(pres.shapes.RECTANGLE, { x: 5.9, y, w: 0.08, h: 0.8, fill: { color: [C.primary, C.accent, C.coral][i] } });
  s15.addText(ins[0], { x: 6.1, y, w: 3.2, h: 0.3, fontSize: 12, fontFace: FONT_CN, bold: true, color: C.darkText });
  s15.addText(ins[1], { x: 6.1, y: y + 0.32, w: 3.2, h: 0.5, fontSize: 10, fontFace: FONT_CN, color: C.muted });
});
addFooter(s15);

// ---------- 16. Product penetration ----------
let s16 = pres.addSlide();
s16.background = { color: C.bgLight };
addSlideTitle(s16, "用户渗透呈现“分层化”与“场景化”特征", "桌面端是深度执行主阵地，浏览器满足轻量即时需求");
s16.addChart(pres.charts.BAR, ...hbarChart([33, 31, 30, 28, 28, 22, 19, 19, 15, 15, 12], ["CodeBuddy", "QClaw", "悟空", "Cursor", "WorkBuddy", "Codex", "LobeClawAI", "QoderWork", "Trae.cn", "AutoClaw", "Manus"], { x: 0.55, y: 1.5, w: 2.9, h: 3.5, title: "桌面端用户渗透率", showValue: true, chartColors: [C.primary] }));
s16.addChart(pres.charts.BAR, ...hbarChart([56, 39, 38, 28, 21, 18, 4], ["Coze", "KimiClaw", "MaxClaw", "ArkClaw", "DuClaw", "Copaw", "HappyClaw"], { x: 3.65, y: 1.5, w: 2.9, h: 3.5, title: "浏览器端用户渗透率", showValue: true, chartColors: [C.secondary] }));
s16.addChart(pres.charts.BAR, ...hbarChart([89, 18, 16, 13, 9, 7, 7], ["OpenClaw", "Hermes Agent", "CrewClaw", "WorkanyBot", "HanoClaw", "PicoClaw", "ZeroClaw"], { x: 6.75, y: 1.5, w: 2.65, h: 3.5, title: "开源智能体用户渗透率", showValue: true, chartColors: [C.accent] }));
addFooter(s16);

// ---------- 17. Selection + payment ----------
let s17 = pres.addSlide();
s17.background = { color: C.bgLight };
addSlideTitle(s17, "选择因素与付费转化", "安全可信、系统兼容、执行能力是关键考量；付费意愿基础已形成");
s17.addShape(pres.shapes.RECTANGLE, { x: 0.55, y: 1.5, w: 4.6, h: 3.6, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
s17.addText("用户选择办公智能体的关键考量", { x: 0.7, y: 1.65, w: 4.3, h: 0.3, fontSize: 13, fontFace: FONT_CN, bold: true, color: C.darkText });
s17.addText("数据安全是首要门槛，系统兼容决定落地可行性，自主执行是价值核心", { x: 0.7, y: 2.0, w: 4.3, h: 0.4, fontSize: 10, fontFace: FONT_CN, color: C.muted });
const factorScores = [95, 90, 82, 78, 70, 62, 55, 50];
const factorLabels = ["任务完成质量", "自主执行能力", "响应速度", "数据安全与隐私保护", "功能覆盖度", "学习成本", "工具/系统兼容性", "性价比"];
factorLabels.forEach((f, i) => {
  const y = 2.55 + i * 0.3;
  const barW = 3.0 * (factorScores[i] / 100);
  s17.addText(f, { x: 0.75, y: y - 0.02, w: 3.8, h: 0.2, fontSize: 10, fontFace: FONT_CN, bold: true, color: C.darkText });
  s17.addShape(pres.shapes.RECTANGLE, { x: 0.75, y: y + 0.16, w: 3.0, h: 0.12, fill: { color: C.light } });
  s17.addShape(pres.shapes.RECTANGLE, { x: 0.75, y: y + 0.16, w: barW, h: 0.12, fill: { color: C.secondary } });
});
s17.addShape(pres.shapes.RECTANGLE, { x: 5.35, y: 1.5, w: 4.1, h: 1.65, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
s17.addText("付费情况", { x: 5.5, y: 1.65, w: 3.8, h: 0.3, fontSize: 13, fontFace: FONT_CN, bold: true, color: C.darkText });
s17.addText("已付费使用 36%", { x: 5.5, y: 2.05, w: 3.8, h: 0.3, fontSize: 12, fontFace: FONT_CN, bold: true, color: C.primary });
s17.addText("使用免费版 59%", { x: 5.5, y: 2.4, w: 3.8, h: 0.3, fontSize: 12, fontFace: FONT_CN, color: C.muted });
s17.addText("正在试用体验版 5%", { x: 5.5, y: 2.75, w: 3.8, h: 0.3, fontSize: 12, fontFace: FONT_CN, color: C.muted });
s17.addShape(pres.shapes.RECTANGLE, { x: 5.35, y: 3.3, w: 4.1, h: 1.9, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
s17.addText("付费方式", { x: 5.5, y: 3.45, w: 3.8, h: 0.3, fontSize: 13, fontFace: FONT_CN, bold: true, color: C.darkText });
const payMethods = ["企业统一采购 35%", "订阅制 34%", "Token 额度充值 24%", "开源产品/技术支持 5%", "免费版+高级功能 2%"];
payMethods.forEach((m, i) => {
  s17.addText(m, { x: 5.5, y: 3.8 + i * 0.28, w: 3.8, h: 0.25, fontSize: 10, fontFace: FONT_CN, color: C.darkText });
});
addFooter(s17);

// ---------- 18. Pain points + insights ----------
let s18 = pres.addSlide();
s18.background = { color: C.bgLight };
addSlideTitle(s18, "使用瓶颈与核心洞察", "需求理解偏差与产出质量不及预期是当前主要痛点");
s18.addChart(pres.charts.BAR, ...hbarChart([46, 42, 31, 30, 27, 26, 16, 13, 9, 9], ["需求理解偏差", "产出质量不及预期", "响应速度慢", "长文本/大文件处理受限", "数据隐私安全担忧", "任务执行中断", "自主操作出错", "过程缺乏透明度", "使用门槛高", "暂无明显问题"], { x: 0.55, y: 1.5, w: 4.6, h: 3.6, title: "用户使用中存在的主要问题", showValue: true, chartColors: [C.coral] }));
s18.addShape(pres.shapes.RECTANGLE, { x: 5.35, y: 1.5, w: 4.1, h: 3.6, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
s18.addText("核心洞察", { x: 5.5, y: 1.65, w: 3.8, h: 0.3, fontSize: 15, fontFace: FONT_CN, bold: true, color: C.primary });
const coreInsights = [
  ["高频习惯已建立", "核心群体已建立高频使用习惯，应用场景正从基础问答向高价值工作流拓展"],
  ["多形态并存", "桌面端成为承载深度场景的关键落地形态，网页端满足轻量即时需求"],
  ["付费基础形成", "组织驱动的 B 端采购与个人订阅两条路径占比相当，未来增长取决于安全合规与不可替代性"],
];
coreInsights.forEach((ci, i) => {
  const y = 2.1 + i * 0.95;
  s18.addShape(pres.shapes.OVAL, { x: 5.55, y: y + 0.08, w: 0.22, h: 0.22, fill: { color: C.secondary } });
  s18.addText(String(i + 1), { x: 5.55, y: y + 0.08, w: 0.22, h: 0.22, align: "center", valign: "middle", fontSize: 11, fontFace: FONT_CN, bold: true, color: C.white });
  s18.addText(ci[0], { x: 5.9, y, w: 3.4, h: 0.28, fontSize: 12, fontFace: FONT_CN, bold: true, color: C.darkText });
  s18.addText(ci[1], { x: 5.9, y: y + 0.32, w: 3.4, h: 0.5, fontSize: 10, fontFace: FONT_CN, color: C.muted });
});
addFooter(s18);

// ---------- 19. Section 03 ----------
let s19 = pres.addSlide();
s19.background = { color: C.accent };
s19.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.accent } });
s19.addText("03", { x: 0.7, y: 1.9, w: 8.6, h: 1.0, fontSize: 72, fontFace: FONT_CN, bold: true, color: C.white });
s19.addText("桌面端爆发与未来", { x: 0.7, y: 2.9, w: 8.6, h: 0.8, fontSize: 40, fontFace: FONT_CN, bold: true, color: C.white });
s19.addText("桌面端价值 · 爆发式增长 · 未来竞争关键", { x: 0.7, y: 3.7, w: 8.6, h: 0.4, fontSize: 16, fontFace: FONT_CN, color: C.light });

// ---------- 20. Desktop value ----------
let s20 = pres.addSlide();
s20.background = { color: C.bgLight };
addSlideTitle(s20, "桌面端办公应用价值被进一步激活和放大", "PC 端承载的核心价值正从“操作软件交互界面”跃升为“智能体调用工具与执行任务的数字环境”");
s20.addChart(pres.charts.BAR, ...hbarChart([15, 14, 12, 10, 8, 8, 6, 6, 5, 4, 4, 3, 2, 1, 1], ["WorkBuddy", "CodeBuddy", "Cursor", "QClaw", "悟空", "Codex", "QoderWork", "LobeClawAI", "AutoClaw", "Manus", "Trae.cn", "元气Bot", "Loomy", "Ajis", "YiClaw"], { x: 0.55, y: 1.5, w: 4.6, h: 3.6, title: "用户最常使用的桌面端办公智能体产品", showValue: true, chartColors: [C.primary] }));
s20.addShape(pres.shapes.RECTANGLE, { x: 5.35, y: 1.5, w: 4.1, h: 3.6, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
const desktopValues = [
  ["算力支撑持续性", "充分调用本地并协同云端算力，支撑大模型持续推理"],
  ["环境完整性", "依托完整桌面操作系统、开放文件系统及多窗口交互，提供深度集成执行环境"],
  ["场景匹配度", "代码开发、长文档、数据分析、多系统协作等任务本质上仍高度依赖 PC"],
  ["企业生态集成", "与企业核心业务系统深度集成，实现自动化流程流转与统一入口管理"],
];
desktopValues.forEach((dv, i) => {
  const y = 1.75 + i * 0.8;
  s20.addShape(pres.shapes.RECTANGLE, { x: 5.5, y, w: 0.08, h: 0.65, fill: { color: C.accent } });
  s20.addText(dv[0], { x: 5.7, y, w: 3.6, h: 0.28, fontSize: 12, fontFace: FONT_CN, bold: true, color: C.darkText });
  s20.addText(dv[1], { x: 5.7, y: y + 0.3, w: 3.6, h: 0.4, fontSize: 10, fontFace: FONT_CN, color: C.muted });
});
addFooter(s20);

// ---------- 21. Explosive growth ----------
let s21 = pres.addSlide();
s21.background = { color: C.bgLight };
addSlideTitle(s21, "桌面端 AI 原生办公智能体迎来爆发式增长", "2026 年 3 月头部产品合计月访问量突破 2000 万次");
const visitData = [885, 334, 238, 215, 101, 76, 72, 53, 47, 38, 33, 12, 3, 2, 2];
const visitLabels = ["WorkBuddy", "Trae.cn", "QClaw", "QoderWork", "CodeBuddy", "AutoClaw", "Core.on", "悟空", "LobsterAI", "EasyClaw", "MiniMax Agent", "元气Bot", "JVS Claw", "Moli", "Loomy"];
s21.addChart(pres.charts.BAR, ...vbarChart(visitData, visitLabels, { x: 0.55, y: 1.5, w: 8.9, h: 3.25, title: "2026 年 3 月中国桌面端 AI 原生办公智能体平台月访问量（万）", showValue: true, dataLabelPosition: "outEnd", chartColors: [C.secondary] }));
s21.addText("市场进入规模扩张期，头部产品开始建立先发优势；大厂依托生态整合，独立厂商聚焦垂直场景深度", {
  x: 0.6, y: 4.85, w: 8.8, h: 0.25, align: "center", fontSize: 12, fontFace: FONT_CN, bold: true, color: C.darkText,
});
addFooter(s21);

// ---------- 22. Growth momentum ----------
let s22 = pres.addSlide();
s22.background = { color: C.bgLight };
addSlideTitle(s22, "整体增速强劲，产品密集公测释放增长动能", "2026 年 3 月桌面端 AI 原生办公智能体平台月访问量环比增速");
const growthData = [831, 449, 360, 226, 123, 82, 76, 69, 68, 22, 6];
const growthLabels = ["WorkBuddy", "EasyClaw", "CodeBuddy", "AutoClaw", "QClaw", "QoderWork", "Trae.cn", "Core.on", "LobsterAI", "MiniMax Agent", "元气Bot"];
s22.addChart(pres.charts.BAR, ...vbarChart(growthData, growthLabels, { x: 0.55, y: 1.5, w: 8.9, h: 3.25, title: "月访问量环比增速（%）", showValue: true, dataLabelPosition: "outEnd", chartColors: [C.accent] }));
s22.addText("密集公测直接带来用户基数自然扩容，标志着桌面端 AI 办公智能体正式迈入市场化竞争阶段", {
  x: 0.6, y: 4.85, w: 8.8, h: 0.25, align: "center", fontSize: 12, fontFace: FONT_CN, bold: true, color: C.darkText,
});
addFooter(s22);

// ---------- 23. Future competition ----------
let s23 = pres.addSlide();
s23.background = { color: C.bgLight };
addSlideTitle(s23, "未来竞争关键", "上下文感知、工作流编排、生态互联能力决定产品竞争力");
const futureCaps = [
  { title: "构筑上下文引擎", desc: "准确识别用户在整个桌面环境中的逻辑链路，自动完成上下文理解与内容创作，实现人机协同“零摩擦”。" },
  { title: "打造自动化工作流编排", desc: "将碎片化任务封装为标准化自动流，使用户习惯固化为“工作流资产”，从单点能力演进为自我循环生产力中枢。" },
  { title: "构建开放生态互联", desc: "成为工具间的协同枢纽，通过跨系统调度本地或云端专业化能力，实现从办公工具向高效协作网络管理者的角色跃升。" },
];
futureCaps.forEach((fc, i) => {
  const x = 0.55 + i * 3.05;
  s23.addShape(pres.shapes.RECTANGLE, { x, y: 1.55, w: 2.85, h: 3.2, fill: { color: C.white }, line: { color: "E2E8F0", width: 1 }, shadow: freshShadow() });
  s23.addShape(pres.shapes.RECTANGLE, { x, y: 1.55, w: 2.85, h: 0.55, fill: { color: [C.primary, C.secondary, C.accent][i] } });
  s23.addText(fc.title, { x, y: 1.62, w: 2.85, h: 0.4, align: "center", fontSize: 15, fontFace: FONT_CN, bold: true, color: C.white });
  s23.addText(fc.desc, { x: x + 0.15, y: 2.25, w: 2.55, h: 2.2, align: "center", fontSize: 12, fontFace: FONT_CN, color: C.muted });
});
addFooter(s23);

// ---------- 24. Conclusion ----------
let s24 = pres.addSlide();
s24.background = { color: C.darkBg };
s24.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 5.625, fill: { color: C.darkBg } });
s24.addText("核心结论", { x: 0.7, y: 1.2, w: 8.6, h: 0.6, fontSize: 36, fontFace: FONT_CN, bold: true, color: C.white });
const conclusions = [
  "办公智能体正从“工具智能”跃迁为“行动智能”，能力边界向自主规划、多工具调用、图形界面操作延伸",
  "用户以效率提升为核心诉求，高频使用习惯已建立，但深度任务渗透仍受限于执行可靠性与场景集成度",
  "桌面端成为承载深度执行的关键形态，2026 年 3 月头部产品月访问量突破 2000 万，增速强劲",
  "未来竞争将围绕上下文感知、工作流编排与生态互联能力展开，安全合规与商业化路径是规模化关键",
];
conclusions.forEach((c, i) => {
  const y = 2.05 + i * 0.75;
  s24.addShape(pres.shapes.OVAL, { x: 0.75, y: y + 0.08, w: 0.22, h: 0.22, fill: { color: C.accent } });
  s24.addText(String(i + 1), { x: 0.75, y: y + 0.08, w: 0.22, h: 0.22, align: "center", valign: "middle", fontSize: 12, fontFace: FONT_CN, bold: true, color: C.white });
  s24.addText(c, { x: 1.15, y, w: 8.0, h: 0.55, fontSize: 14, fontFace: FONT_CN, color: "E2E8F0" });
});
s24.addText("谢谢观看", { x: 0.7, y: 5.0, w: 8.6, h: 0.4, align: "center", fontSize: 20, fontFace: FONT_CN, bold: true, color: C.white });

// Save
pres.writeFile({ fileName: "/Users/temu/WorkBuddy/2026-08-20-01-41-58/outputs/中国办公智能体市场洞察.pptx" })
  .then(() => console.log("PPT generated successfully"))
  .catch(err => console.error(err));
