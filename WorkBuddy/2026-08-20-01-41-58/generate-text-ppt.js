const path = require("path");
const PptxGen = require("pptxgenjs");

const OUT = "/Users/temu/WorkBuddy/2026-08-20-01-41-58/outputs/中国办公智能体市场洞察_文字版.pptx";
const FONT = "Microsoft YaHei";

const C = {
  primary: "0F4C81",
  secondary: "1B7FA8",
  accent: "16A2B8",
  light: "EAF2F8",
  grey: "F4F7FA",
  dark: "1A2533",
  muted: "5A6B7B",
  white: "FFFFFF",
  line: "D6E2EC",
};

const pres = new PptxGen();
pres.defineLayout({ name: "W16x9", width: 10, height: 5.625 });
pres.layout = "W16x9";
pres.author = "WorkBuddy";
pres.title = "中国办公智能体市场洞察（文字整理版）";

const PW = 10, PH = 5.625;

// ---- helpers ----
function topBar(slide, chapter, title, idx, total) {
  slide.background = { color: C.white };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: PW, h: 0.1, fill: { color: C.accent } });
  slide.addText(chapter, { x: 0.6, y: 0.28, w: 7, h: 0.28, fontSize: 12, fontFace: FONT, bold: true, color: C.accent });
  slide.addText(title, { x: 0.6, y: 0.55, w: 8.6, h: 0.62, fontSize: 20, fontFace: FONT, bold: true, color: C.dark });
  slide.addShape(pres.shapes.LINE, { x: 0.6, y: 1.18, w: 8.8, h: 0, line: { color: C.line, width: 1 } });
  slide.addText(`${idx} / ${total}`, { x: PW - 1.4, y: PH - 0.34, w: 1.0, h: 0.28, fontSize: 9, fontFace: FONT, color: "9CA3AF", align: "right" });
}

function est(text, cpl) { return Math.max(1, Math.ceil(text.length / cpl)); }

// points: array of string OR {h:string, items:[string]}
// table: {headers:[], rows:[[],...], colW:[]}
function contentSlide(chapter, title, idx, total, points, table) {
  const s = pres.addSlide();
  topBar(s, chapter, title, idx, total);
  let y = 1.35;
  const hasTable = table && table.rows.length;
  const bodyBottom = hasTable ? 3.75 : 5.2;

  points.forEach((p) => {
    if (typeof p === "string") {
      const lines = est(p, 30);
      const h = lines * 0.26 + 0.08;
      s.addShape(pres.shapes.OVAL, { x: 0.66, y: y + 0.07, w: 0.08, h: 0.08, fill: { color: C.accent } });
      s.addText(p, { x: 0.85, y: y - 0.02, w: 8.55, h: h, fontSize: 12, fontFace: FONT, color: C.dark, valign: "top", lineSpacingMultiple: 1.02 });
      y += h + 0.1;
    } else {
      const hl = est(p.h, 30);
      const hh = hl * 0.26 + 0.06;
      s.addText(p.h, { x: 0.62, y: y, w: 8.7, h: hh, fontSize: 12.5, fontFace: FONT, bold: true, color: C.secondary, valign: "top" });
      y += hh + 0.04;
      p.items.forEach((it) => {
        const lines = est(it, 28);
        const h = lines * 0.24 + 0.05;
        s.addText("–  " + it, { x: 0.85, y: y, w: 8.4, h: h, fontSize: 11, fontFace: FONT, color: C.muted, valign: "top" });
        y += h + 0.05;
      });
      y += 0.06;
    }
  });

  if (hasTable) {
    const t = table;
    s.addText("关键数据", { x: 0.6, y: 3.6, w: 4, h: 0.26, fontSize: 11.5, fontFace: FONT, bold: true, color: C.primary });
    const headRow = t.headers.map((h) => ({ text: h, options: { fill: { color: C.primary }, color: C.white, bold: true, fontSize: 10, align: "center", valign: "middle" } }));
    const body = t.rows.map((r, ri) =>
      r.map((c, ci) => ({
        text: String(c),
        options: {
          fill: { color: ri % 2 ? C.grey : C.white },
          color: ci === 0 ? C.dark : C.muted,
          bold: ci === 0,
          fontSize: 9.5,
          align: ci === 0 ? "left" : "center",
          valign: "middle",
        },
      }))
    );
    s.addTable([headRow, ...body], {
      x: 0.6, y: 3.88, w: 8.8,
      colW: t.colW,
      border: { pt: 0.5, color: C.line },
      fontFace: FONT,
      rowH: 0.21,
      autoPage: false,
    });
  }
  return s;
}

const TOTAL = 21;

// ---------- COVER ----------
const cv = pres.addSlide();
cv.background = { color: C.primary };
cv.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: PW, h: 0.18, fill: { color: C.accent } });
cv.addText("Analysys 易观分析", { x: 0.8, y: 1.5, w: 8, h: 0.4, fontSize: 14, fontFace: FONT, color: C.accent, bold: true });
cv.addText("中国办公智能体\n市场洞察", { x: 0.8, y: 2.0, w: 8.4, h: 1.6, fontSize: 40, fontFace: FONT, bold: true, color: C.white, lineSpacingMultiple: 1.05 });
cv.addText("报告文字提取整理版 · 共 21 页", { x: 0.8, y: 3.75, w: 8, h: 0.4, fontSize: 15, fontFace: FONT, color: "CFE3F0" });
cv.addText("数据来源：易观分析《中国办公智能体市场洞察》  |  用户调研 N=500（2026年5月）", { x: 0.8, y: 4.7, w: 8.6, h: 0.35, fontSize: 10.5, fontFace: FONT, color: "9FB8CC" });

// ---------- TOC ----------
const tc = pres.addSlide();
tc.background = { color: C.white };
tc.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: PW, h: 0.1, fill: { color: C.accent } });
tc.addText("目录", { x: 0.6, y: 0.4, w: 8, h: 0.6, fontSize: 26, fontFace: FONT, bold: true, color: C.dark });
const toc = [
  ["一、市场概览", "研究界定 · 能力跃迁 · 需求升级 · 产品分类 · 六大能力 · 价值交付 · 生态图谱 · 中美对比 · 挑战演进", "P1–P9"],
  ["二、用户洞察", "用户画像 · 使用习惯 · 应用场景 · 渗透分层 · 选择因素 · 付费转化 · 使用瓶颈 · 核心洞察", "P10–P17"],
  ["三、桌面端爆发与未来", "桌面端价值 · 月访问量 · 环比增速 · 未来竞争关键", "P18–P21"],
];
toc.forEach((row, i) => {
  const y = 1.5 + i * 1.15;
  tc.addShape(pres.shapes.RECTANGLE, { x: 0.6, y, w: 0.12, h: 0.95, fill: { color: [C.primary, C.secondary, C.accent][i] } });
  tc.addText(row[0], { x: 0.9, y: y + 0.02, w: 5, h: 0.4, fontSize: 16, fontFace: FONT, bold: true, color: C.dark });
  tc.addText(row[1], { x: 0.9, y: y + 0.45, w: 6.6, h: 0.5, fontSize: 11, fontFace: FONT, color: C.muted });
  tc.addText(row[2], { x: 7.6, y: y + 0.2, w: 1.8, h: 0.5, fontSize: 14, fontFace: FONT, bold: true, color: [C.primary, C.secondary, C.accent][i], align: "right" });
});

// ---------- CONTENT ----------
contentSlide("研究界定", "办公智能体研究界定与数据说明", 1, TOTAL, [
  { h: "研究界定", items: [
    "办公智能体（Workspace Agents）：以 AI 为核心，面向办公场景的任务自动化与工作流编排的智能体产品。",
    "四大特征：任务自主执行 · 办公场景适配 · 多系统集成 · 开放生态构建。",
  ]},
  { h: "用户调研数据说明", items: [
    "量化调研 N=500（2026年5月），对象为18岁以上、近6个月使用过办公智能体者。",
  ]},
  { h: "统计口径", items: [
    "仅统计 PC 桌面端；排除 Web/插件、移动端、办公软件内嵌智能体。",
    "“月活用量”指周期内用户与 PC 端平台的互动次数。",
  ]},
], null);

contentSlide("能力跃迁", "AI Agent 能力边界从“工具智能”向“行动智能”跃迁", 2, TOTAL, [
  "2026 年范式革命：多模态大模型在推理、规划与工具调用上突破，能力从“感知理解”向“主动执行”延伸。",
  { h: "三大能力增量", items: [
    "长程推理：以 GPT、Claude、DeepSeek、Qwen 为代表，复杂任务可拆解为可执行步骤并纠错。",
    "工具调用：精准可靠地与文件、系统、浏览器及外部 API 深度交互。",
    "多模态理解：读懂屏幕语义、操控 GUI，使桌面级全流程自动化成为可用。",
  ]},
  "基准测试准确率大幅跃升，但综合能力仍低于人类基准，完全开放场景仍需人类监督兜底。",
], {
  headers: ["基准测试", "测试内容", "智能体准确率", "人类基准"],
  colW: [2.1, 3.1, 1.8, 1.8],
  rows: [
    ["GAIA（通用助手）", "多工具复杂任务", "74.5%", "92.2%"],
    ["OSWorld（系统）", "虚拟环境真实操作", "38.2%", "75.2%"],
    ["WebArena（网络）", "真实网站多步操作", "57.2%", "78.24%"],
  ],
});

contentSlide("需求升级", "办公智能化需求升级，智能体成重构工作方式的关键变量", 3, TOTAL, [
  "价值跃迁：从“提升效率”到“填补执行缺口”，能否从“可选项”变为“必装品”的分水岭。",
  { h: "工具使用演变四阶段", items: ["连接（模糊需求）→ 生成（内容生成）→ 调用（功能调用）→ 规划与执行（流程自动化）。"] },
  { h: "企业管理者对 Agent 的预期（Microsoft 2025）", items: [
    "构建多智能体系统适配复杂任务 42% · 训练智能体 41% · 重要业务处理 38% · 管理智能体 36%。",
  ]},
  { h: "三大结构性转变", items: [
    "个人效率提升 → 组织级智能协作；工具堆砌 → 智能体能力激发；提高效率 → 重塑工作方式。",
  ]},
], null);

contentSlide("产品分类", "办公智能体平台产品的主要分类与特征", 4, TOTAL, [
  "三类产品路线：AI 原生办公智能体（任务闭环）· AI 通用对话智能体（知识获取）· 办公软件内容智能体（工作流优化）。详见下表。",
  { h: "终端应用形态", items: [
    "桌面端：深度调用系统 API，与本地文件、桌面应用集成。",
    "浏览器端：Web/插件形态，零安装、基于云端服务。",
    "移动端：手机/平板，即时交互，与移动应用集成。",
  ]},
], {
  headers: ["产品类型", "产品设计目标"],
  colW: [2.6, 6.2],
  rows: [
    ["AI 原生办公智能体", "以智能体为核心，深度系统调用与执行，自主完成端到端任务"],
    ["AI 通用对话智能体", "以对话为出发点，主打能力广度与辅助创作，多场景灵活响应"],
    ["办公软件内容智能体", "场景化赋能，嵌入成熟办公软件，提升现有工作流效率"],
  ],
});

contentSlide("能力体系", "六大能力层级协同驱动，构建自主执行闭环", 5, TOTAL, [
  "主流平台在六个维度形成完整能力体系，实现从指令理解到结果交付的端到端自治。",
  { h: "六大能力层级", items: [
    "① 系统级集成与应用：读写文件、调用系统 API、操控第三方应用。",
    "② 直接交付可用成果：文档类 / 数据类 / 流程类三种交付形态。",
    "③ 深度理解业务场景：接入行业知识库、岗位模板、企业知识库。",
    "④ 持续学习进化：模型、知识、交互三方面自动优化。",
    "⑤ 开放生态：技能市场，支持开发者与企业扩展能力。",
    "⑥ 可控安全策略：本地存储、权限管理、审计追踪，确保合规。",
  ]},
], null);

contentSlide("价值交付", "从卖工具到卖结果，办公智能体的价值交付革命", 6, TOTAL, [
  "付费逻辑转向：用户为节省的时间与获得的成果付费，而非为功能入口预付。",
  { h: "四大定价模式", items: [
    "订阅制：购买“持续优化的能力”，与任务质量挂钩。",
    "Token 用量计费：按消耗量计费，灵活组合。",
    "Skill/插件付费：为特定技能单独付费或订阅，生态丰富度成差异化变量。",
    "私有化部署：面向政企，一次性授权 + 持续维护，国产模型具成本优势。",
  ]},
], {
  headers: ["商业模式", "典型用户", "售卖方式"],
  colW: [2.4, 2.6, 3.8],
  rows: [
    ["订阅制", "普通用户、中小企业", "按使用深度分级付费"],
    ["Token 用量", "深度个人开发者", "直接付模型 API 或 token 包"],
    ["Skill/插件", "长尾/垂直场景", "技能商城单独付费或订阅"],
    ["私有化部署", "大型政企客户", "本地/私有云完整部署"],
  ],
});

contentSlide("产业生态", "中国办公智能体产业生态图谱", 7, TOTAL, [
  { h: "三类产品", items: [
    "AI 原生办公智能体：Manus、Cursor、Codex、WorkBuddy、扣子、Trae 等。",
    "AI 通用对话智能体：豆包、千问、DeepSeek、ChatGPT、Gemini、Claude 等。",
    "办公软件内容智能体：飞书、钉钉、WPS AI、Copilot、Notion 等。",
  ]},
  { h: "三大支撑层", items: [
    "开源智能体框架：OpenClaw、Hermes、PicoClaw、WorkAny 等。",
    "智能体工具与平台：LangChain、AutoGen、LlamaIndex、Zapier 等。",
    "基础模型：DeepSeek、智谱、Qwen、混元、OpenAI、Anthropic 等。",
  ]},
], null);

contentSlide("中美对比", "中美市场办公智能体特征对比", 8, TOTAL, [
  "发展路径由市场土壤、用户习惯与技术生态共同塑造：美国以代码开发切入、强模型驱动垂直专业化；中国以通用办公为主、生态融合快速规模化。",
], {
  headers: ["维度", "美国", "中国"],
  colW: [1.6, 3.6, 3.6],
  rows: [
    ["场景切入", "高价值垂直（代码/法务/分析）", "最大众通用办公场景"],
    ["核心用户", "强技术背景开发者、企业IT", "庞大白领群体，免费渗透"],
    ["产品策略", "单点极致、垂直化壁垒", "通用平台型、一站式集成"],
    ["竞争逻辑", "模型深度与专业数据壁垒", "生态壁垒与流量分发效率"],
  ],
});

contentSlide("挑战演进", "办公智能体发展的核心挑战与演进方向", 9, TOTAL, [
  { h: "核心挑战", items: [
    "长程推理与执行可靠性不稳定，多工具协同稳定性是主要 gap。",
    "平台互操作性缺失、生态割裂，形成“生态锁定”。",
    "高价值场景（财务/供应链/HR）数据孤岛，难触达核心价值链。",
  ]},
  { h: "演进方向", items: [
    "能力筑基与场景验证：提升单点任务完成率与质量。",
    "可靠性与服务交付提升：工具调用从预设工作流向动态规划演进。",
    "成为工作流基础设施：或出现“AI 时代的安卓系统”，基础平台免费、垂直服务盈利。",
  ]},
], null);

contentSlide("用户画像", "用户以职场中青年为主，社媒是主要触达渠道", 10, TOTAL, [
  "25–39 岁用户合计占 80%，为绝对主体；职业以企业白领、IT 开发、产品设计为主。",
  "“公司统一要求”占 15%，反映企业侧从观望转向主动推进，组织驱动增长使用更固定。",
], {
  headers: ["年龄分布", "占比", "职业分布", "占比"],
  colW: [2.2, 1.2, 2.8, 1.2],
  rows: [
    ["18–24 岁", "11%", "企业白领", "31%"],
    ["25–29 岁", "35%", "IT 开发与运维", "22%"],
    ["30–39 岁", "45%", "产品经理", "20%"],
    ["40 岁+", "9%", "内容创作者", "11%"],
    ["—", "—", "学生 / 教师 / 管理者", "10/4/2%"],
  ],
});

contentSlide("使用习惯", "用户以效率为核心诉求，形成稳定使用习惯", 11, TOTAL, [
  "效率工具属性压倒一切：“工作提效”与“减少重复性任务”居前两位。",
  "桌面端近三成使用率已具规模，天然适合多步骤、文件批量处理等深度系统交互。",
  "每天使用 + 每周 3–4 次的高频使用者合计超七成，易形成使用惯性。",
], {
  headers: ["使用目的 Top3", "占比", "使用方式 Top3", "占比"],
  colW: [2.6, 1.1, 2.7, 1.1],
  rows: [
    ["工作提效", "51%", "网页端直接使用", "49%"],
    ["减少重复性任务", "41%", "桌面端独立使用", "29%"],
    ["获取专业知识", "39%", "办公软件插件", "27%"],
    ["激发灵感", "34%", "自行部署框架", "11%"],
    ["高频频率", "每天29%+周3-4次46%", "—", "—"],
  ],
});

contentSlide("应用场景", "主流场景仍以问答交互为主，深度任务空间待打开", 12, TOTAL, [
  { h: "三类场景特征", items: [
    "问答交互基本盘：信息检索、方案策划、文档处理（边界清晰、反馈短）。",
    "桌面端原生代理：编程辅助、文件整理已具规模，从“回答”拓展到“执行”。",
    "垂直协作待爆发：项目管理、客服销售渗透低，依赖业务系统深度集成。",
  ]},
], {
  headers: ["应用场景", "占比", "应用场景", "占比"],
  colW: [2.9, 1.0, 2.9, 1.0],
  rows: [
    ["信息检索与问答", "52%", "编程辅助", "24%"],
    ["方案策划", "43%", "电脑文件管理", "24%"],
    ["文档处理", "43%", "项目管理", "14%"],
    ["数据分析", "36%", "工作流/任务自动化", "10%"],
    ["内容生成", "34%", "客服/销售", "2%"],
  ],
});

contentSlide("渗透分层", "智能体用户渗透呈现“分层化”与“场景化”特征", 13, TOTAL, [
  { h: "三类阵地", items: [
    "桌面端：重度用户主阵地，深度执行驱动多元格局（腾讯系占整体优势）。",
    "网页端：满足轻量即时需求，字节系 Coze 凭低门槛主导。",
    "开源框架：以技术浪潮构建生态共识，OpenClaw 是本轮 Agent 起点。",
  ]},
], {
  headers: ["桌面端渗透率", "占比", "网页端渗透率", "占比"],
  colW: [2.9, 1.0, 2.9, 1.0],
  rows: [
    ["CodeBuddy", "33%", "Coze", "56%"],
    ["QClaw", "31%", "KimiClaw", "39%"],
    ["悟空", "30%", "MaxiClaw", "38%"],
    ["Cursor", "28%", "ArisClaw", "28%"],
    ["开源 OpenClaw", "89%", "DuClaw", "21%"],
  ],
});

contentSlide("选择因素", "安全可信、系统兼容、执行能力是关键考量", 14, TOTAL, [
  "“数据安全与隐私保护”“工具/系统兼容性”“自主执行能力”重要性居前三位。",
  { h: "三大核心决策框架", items: [
    "数据安全是首要门槛：反映“将工作交给 Agent”的安全边界意识，直接影响企业采纳。",
    "系统兼容决定落地：取决于能否与存量生产力工具有效衔接。",
    "自主执行是价值核心：用户希望智能体自主拆解、调用工具、执行多步操作。",
  ]},
  "其余考量（按重要性）：任务完成质量 · 响应速度 · 功能覆盖度 · 学习成本 · 性价比。",
], null);

contentSlide("付费转化", "用户付费转化尚处早期，但付费意愿基础已形成", 15, TOTAL, [
  "已付费 36% / 免费 59% / 试用 5%；已付费中企业采购与订阅制主导。",
  "未付费用户多数持开放态度，Freemium（基础免费+高级解锁）最受青睐。",
  "付费率提升关键：①深度场景建立不可替代性；②定价匹配价格敏感度。",
], {
  headers: ["付费状态", "占比", "月度付费金额", "占比"],
  colW: [2.6, 1.1, 2.8, 1.1],
  rows: [
    ["已付费", "36%", "100–500 元", "29%"],
    ["使用免费版", "59%", "500–1000 元", "22%"],
    ["正在试用", "5%", "企业统一支付", "32%"],
    ["付费意愿:可接受", "43%", "愿意付费", "13%"],
    ["继续免费", "41%", "停止使用", "3%"],
  ],
});

contentSlide("使用瓶颈", "需求理解偏差与产出质量不及预期是主要瓶颈", 16, TOTAL, [
  "46% 与 42% 的用户将“需求理解偏差”与“产出质量不及预期”视为主要痛点。",
  "性能落差：约三成用户认为响应速度、长文本/大文件处理能力不足。",
  "自主执行仍薄弱：缺乏自我纠错与进度可视化，影响深度使用与信任建立。",
], {
  headers: ["使用中存在的主要问题", "占比"],
  colW: [6.8, 2.0],
  rows: [
    ["需求理解偏差，需反复沟通澄清", "46%"],
    ["产出质量不及预期，需大量返工", "42%"],
    ["响应速度慢，等待时间过长", "31%"],
    ["长文本/大文件处理受限", "30%"],
    ["数据隐私与安全担忧", "27%"],
    ["任务执行中断，无法自动完成", "26%"],
  ],
});

// page 17 three columns
(() => {
  const s = pres.addSlide();
  topBar(s, "核心洞察", "办公智能体用户调研核心洞察", 17, TOTAL);
  const cols = [
    ["核心群体已建立高频习惯", "25–39 岁白领、开发者占超八成，高频使用者超七成；当前仍以轻量问答为主，对“多工具协同”与“直接交付结果”的期待正拉动能力演进。"],
    ["桌面端成关键落地形态", "网页端渗透占一半，零安装易上手；用户高度看重系统兼容与自主执行，桌面端更靠近本地文件与工具链，承载多步骤与本地集成。"],
    ["付费意愿基础已初步形成", "付费转化早期但意愿形成，B 端采购撬动规模化；C 端偏好 Freemium，以免费版建习惯、深度场景引导增量付费。"],
  ];
  const cw = 2.85, gap = 0.12, x0 = 0.6, y0 = 1.4, ch = 3.6;
  cols.forEach((c, i) => {
    const x = x0 + i * (cw + gap);
    s.addShape(pres.shapes.RECTANGLE, { x, y: y0, w: cw, h: ch, fill: { color: C.light }, line: { color: C.line, width: 1 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: y0, w: cw, h: 0.5, fill: { color: C.secondary } });
    s.addText(`0${i + 1}`, { x: x + 0.1, y: y0 + 0.06, w: 0.5, h: 0.38, fontSize: 18, fontFace: FONT, bold: true, color: C.white });
    s.addText(c[0], { x: x + 0.6, y: y0 + 0.06, w: cw - 0.7, h: 0.38, fontSize: 12.5, fontFace: FONT, bold: true, color: C.white, valign: "middle" });
    s.addText(c[1], { x: x + 0.15, y: y0 + 0.62, w: cw - 0.3, h: ch - 0.75, fontSize: 11, fontFace: FONT, color: C.dark, valign: "top", lineSpacingMultiple: 1.05 });
  });
})();

contentSlide("桌面端价值", "桌面端的办公应用价值被 Agent 进一步激活放大", 18, TOTAL, [
  "PC 端价值重构：从软件交互界面跃升为智能体执行任务的数字环境。",
  { h: "四大支撑", items: [
    "算力：本地+云端算力支撑持续推理与复杂计算。",
    "环境：完整 OS、开放文件系统、多窗口深度集成。",
    "场景：代码、长文档、分析、多系统协作依赖 PC。",
    "企业集成：与核心业务系统深度集成，统一入口。",
  ]},
  "WorkBuddy 渗透率领先，前六款产品合计覆盖超六成用户首选。",
], {
  headers: ["最常使用的桌面端产品", "占比"],
  colW: [6.8, 2.0],
  rows: [
    ["WorkBuddy", "15%"],
    ["CodeBuddy", "14%"],
    ["Cursor", "12%"],
    ["QClaw", "10%"],
    ["悟空 / Codex", "各 8%"],
    ["QoderWork / LobsterAI", "各 6%"],
  ],
});

contentSlide("桌面端爆发", "桌面端 AI 原生办公智能体应用迎来爆发式增长", 19, TOTAL, [
  "2026 年 3 月头部产品合计月访问量突破 2000 万次，市场进入规模扩张期。",
  "腾讯 WorkBuddy 月访问量 885 万居第一；Trae.cn、QClaw、QoderWork 处第一梯队。",
  "大厂效应显现：WorkBuddy（腾讯）、Trae.cn（字节）、QClaw（腾讯）、QoderWork（阿里）均超 200 万。",
], {
  headers: ["产品（2026年3月）", "月访问量(万)"],
  colW: [6.8, 2.0],
  rows: [
    ["WorkBuddy", "885"],
    ["Trae.cn", "334"],
    ["QClaw", "238"],
    ["QoderWork", "215"],
    ["CodeBuddy", "103"],
    ["AutoClaw / Core.cn", "76 / 72"],
    ["悟空 / LobsterAI", "53 / 47"],
  ],
});

contentSlide("环比增速", "整体增速强劲，产品密集公测释放增长动能", 20, TOTAL, [
  "增速 TOP5 产品月度环比增速普遍超 100%；WorkBuddy 以 831% 领跑。",
  "腾讯系增长势能率先显现：QClaw 123%、CodeBuddy 360%，战略投入与快速迭代形成正向循环。",
  "密集公测后正式迈入市场化竞争，后续考验真实留存与活跃度。",
], {
  headers: ["产品（2026年3月环比）", "增速"],
  colW: [6.8, 2.0],
  rows: [
    ["WorkBuddy", "831%"],
    ["EasyClaw", "449%"],
    ["CodeBuddy", "360%"],
    ["AutoClaw", "238%"],
    ["QClaw", "123%"],
    ["QoderWork / Trae.cn", "82% / 76%"],
    ["LobsterAI / MiniMax", "68% / 22%"],
  ],
});

contentSlide("未来关键", "上下文感知、工作流编排、生态互联决定未来竞争", 21, TOTAL, [
  { h: "① 上下文感知引擎", items: ["构筑工作语境下的全域感知，读取当前文件、关联参考网页与历史操作，实现人机协同意图“零摩擦”。"] },
  { h: "② 自动化工作流编排", items: ["将碎片化任务封装为标准自动流，固化用户工作习惯为“工作流资产”，结构性重塑办公路径。"] },
  { h: "③ 开放协作生态互联", items: ["成为各类生产力软件之间的协同枢纽，串联分散数字工作空间，占据组织内生产力调度中心入口。"] },
], null);

pres.writeFile({ fileName: OUT }).then(() => console.log("Saved:", OUT)).catch((e) => { console.error(e); process.exit(1); });
