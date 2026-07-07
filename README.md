<div align="center">

# tailored-resume-generator

把基础简历沉淀成可复用经历库，再为每个 JD 生成可追踪、可审阅、可迭代的定制简历。

<sub>Codex Skill · Resume Bank · JD Matching · PDF QA · Expert Gate</sub>

</div>

---

## 项目定位

`tailored-resume-generator` 是一个面向求职投递的 Codex Skill。它从一份基础简历和可复用项目库出发，为不同 JD 生成定制简历、HTML/PDF 版本、项目筛选记录、修改历史和专家审阅结果。

它不做无依据的“花式改写”，而是把投递流程拆成可复现的工程化步骤：

| 目标 | 产物 | 价值 |
| --- | --- | --- |
| 沉淀经历 | `base-profile.md`、`projects/*.md` | 把一次性简历拆成可复用证据库 |
| 匹配 JD | `jd-analysis.md` | 明确岗位优先级、关键词和风险点 |
| 选择项目 | `selected-projects.md` | 记录为什么选这些经历、不选哪些经历 |
| 生成版本 | `resume_vN.md/html/pdf` | 每个岗位都有独立版本链 |
| 质量门禁 | `expert-review_vN.md` | 交付前检查事实边界、岗位匹配和版面问题 |
| 持续迭代 | `CHANGELOG.md` | 所有修改可追踪，不覆盖已审版本 |

## 工作流总览

| 阶段 | 输入 | 动作 | 输出 |
| --- | --- | --- | --- |
| 1. 建库 | 原始简历 PDF / DOCX / MD / HTML | 抽取身份、教育、技能、经历、项目 | `resume-bank/` |
| 2. 核对 | `base-profile.md`、`projects/*.md` | 人工确认日期、指标、作者排序、项目边界 | 已审核项目卡 |
| 3. 分析 JD | 公司、岗位、完整 JD | 拆解硬性要求、偏好项、关键词和缺口 | `jd-analysis.md` |
| 4. 筛选经历 | 项目库 + JD 分析 | 按相关性、证据强度、风险打分 | `selected-projects.md` |
| 5. 生成简历 | 已确认项目卡 | 输出 Markdown、HTML、PDF | `resume_vN.*` |
| 6. 版面 QA | 当前 HTML/PDF | 渲染截图，检查裁切、重叠、资源泄漏 | QA 记录 |
| 7. 专家门禁 | 简历 + 证据包 | 对抗性检查事实、表达、匹配度 | `expert-review_vN.md` |
| 8. 交付或修复 | PASS / BLOCKED | 通过则人工审阅；阻塞则写修复计划并生成下一版 | 投递版本或 `review-fix-plan_vN.md` |

### 产物关系

| 来源 | 生成 | 继续流向 |
| --- | --- | --- |
| 原始简历 | `base-profile.md`、`projects/*.md` | 项目筛选、事实核对 |
| 目标 JD | `jd.md`、`metadata.md`、`jd-analysis.md` | 项目打分、专家身份生成 |
| 项目库 + JD 分析 | `selected-projects.md` | 简历组装 |
| 简历草稿 | `resume_vN.md`、`resume_vN.html`、`resume_vN.pdf` | PDF QA、专家审核 |
| 专家审核 | `expert-review_vN.md` | PASS 后交付；BLOCKED 后生成修复计划 |
| 用户反馈 | `CHANGELOG.md`、`resume_vN+1.*` | 新一轮 QA 和门禁 |

## 目录结构

```text
tailored-resume-generator/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── resume-template.html
├── references/
│   ├── adversarial-resume-review.md
│   ├── application-package.md
│   ├── chinese-technical-resume-finalization.md
│   ├── output-contract.md
│   ├── project-card-template.md
│   └── role-fit-rubric.md
└── scripts/
    ├── create_application_package.py
    ├── generate_resume_html.py
    └── init_resume_bank.py
```

生成后的 `resume-bank` 通常长这样：

```text
resume-bank/
├── base-profile.md
├── projects/
│   └── project-id.md
├── outputs/
└── applications/
    └── YYYYMMDD-company-role/
        ├── jd.md
        ├── metadata.md
        ├── jd-analysis.md
        ├── selected-projects.md
        ├── resume_v1.md
        ├── resume_v1.html
        ├── resume_v1.pdf
        ├── expert-review_v1.md
        ├── review-fix-plan_v1.md
        ├── CHANGELOG.md
        └── notes.md
```

## 快速安装

克隆到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Hfx-J/tailored-resume-generator.git \
  ~/.codex/skills/tailored-resume-generator
```

已有同名目录时更新：

```bash
cd ~/.codex/skills/tailored-resume-generator
git pull --ff-only
```

## 快速上手

### 1. 初始化经历库

对 Codex 说：

```text
请用 tailored-resume-generator，根据我的简历 /path/to/my_resume.pdf 初始化 resume-bank，
工作目录放在 /path/to/job-plan
```

也可以直接运行脚本：

```bash
python scripts/init_resume_bank.py \
  --resume /path/to/my_resume.pdf \
  --output /path/to/resume-bank
```

初始化后的项目卡是草稿，必须人工核对日期、指标、作者排序、项目边界、保密信息和不能声称的内容。

### 2. 创建 JD 投递包

把目标 JD 发给 Codex：

```text
请基于这个 JD 生成一版简历：
公司：...
岗位：...
岗位职责：...
任职要求：...
```

或先创建标准投递包：

```bash
python scripts/create_application_package.py \
  --bank /path/to/resume-bank \
  --company 公司名 \
  --role 岗位名 \
  --jd-file /path/to/jd.md
```

### 3. 生成 HTML 简历

```bash
python scripts/generate_resume_html.py \
  --markdown /path/to/resume_v1.md \
  --template assets/resume-template.html \
  --output /path/to/resume_v1.html
```

### 4. 迭代版本

可以继续给具体反馈：

```text
研究经历太短了，把论文和项目展开一点
```

```text
第一页太空，保持当前版式但提高内容密度
```

```text
论文标题下面加论文链接
```

每次修改都生成新版本，例如 `resume_v2.md/html/pdf`，不要覆盖已经审核过的版本。

## 简历视觉规则

视觉规则不是固定模板。中文技术简历最终排版时，skill 应先分析原简历风格，再继承其视觉语言。

| 维度 | 需要从原简历提取的规则 |
| --- | --- |
| 页面 | A4/Letter、页数、边距、页眉页脚、是否有照片或 Logo |
| 结构 | 单栏/双栏、时间线样式、模块顺序、标题层级 |
| 字体 | 中文/英文字体倾向、字号、行高、粗体节奏 |
| 色彩 | 主色、强调色、分隔线颜色、链接颜色 |
| 标题 | section 标题形式、横线、底色、编号或标签样式 |
| 密度 | 段落间距、项目符号间距、每页信息量 |
| 强调 | 哪些内容加粗、是否使用标签、是否突出指标 |

规则优先级：

| 优先级 | 来源 |
| --- | --- |
| 1 | 用户明确指定的视觉要求 |
| 2 | 原始简历 PDF / DOCX / HTML / Markdown 的风格分析 |
| 3 | 最新已接受的 `resume_vN.html/pdf` |
| 4 | 无可用来源时，采用中性、可读、ATS 友好的技术简历样式 |

只有当原简历本身就是红色强调、单栏、宋体或其他特定风格时，才继承这些风格。不要把任何颜色、栏数、字体或“营销风 hero”禁令当成所有简历的默认规则。

## 专家门禁

每个 JD 定制版本在交付前都要通过对抗性专家审核。

| 审核输入 | 审核重点 | 输出 |
| --- | --- | --- |
| 原始简历 / 项目卡 | 是否有证据支撑 | 事实风险 |
| JD 与 JD 分析 | 是否匹配核心要求 | 匹配度判断 |
| 当前简历版本 | 表达是否可信、是否能经受面试追问 | 修改建议 |
| PDF / 截图 QA | 是否裁切、重叠、泄露本地路径 | 版面结论 |

审核专家身份会根据 JD 动态生成，例如：

| JD 方向 | 可能的专家身份 |
| --- | --- |
| 端到端自动驾驶 | 端到端自动驾驶算法负责人 |
| 多模态世界模型 | 多模态世界模型面试官 |
| SLAM / 定位 | SLAM / 定位算法负责人 |
| 机器人系统 | 机器人系统落地负责人 |

只有 `expert-review_vN.md` 中出现：

```text
PASS_FOR_HUMAN_REVIEW
```

才算可以交给人工审阅或投递。

如果结果是：

```text
BLOCKED_BY_EXPERT
```

需要写 `review-fix-plan_vN.md`，再生成下一版修复。

## 事实安全原则

| 原则 | 示例 |
| --- | --- |
| 不编造 | 不编造公司、岗位、时间、论文、奖项、指标或工具 |
| 不升级 | 不把“了解”升级成“精通” |
| 留占位 | 缺失事实使用 `[量化指标待补]`、`[项目规模待补]` |
| 链接真实 | 未公开论文不要伪造链接 |
| 保护隐私 | 私有项目不要泄露地图、数据、客户和内部实现细节 |
| 记录边界 | 论文作者排序、收录状态和链接要写入项目卡 |

## 适用场景

| 场景 | 说明 |
| --- | --- |
| 校招 / 秋招投递 | 为多个公司和岗位维护独立版本 |
| 自动驾驶 / 机器人 / SLAM / 感知岗位 | 根据 JD 调整项目排序和表达重点 |
| 中文技术简历 PDF 打磨 | 保持原简历风格，同时解决密度、裁切、层级问题 |
| 论文和项目较多的候选人 | 为不同岗位筛选最相关证据 |

## 不适合做什么

- 不适合伪造经历或夸大项目边界。
- 不适合把一份简历无脑套所有岗位。
- 不适合替代人工事实核对。
- 不适合公开上传含个人隐私的真实简历材料。
