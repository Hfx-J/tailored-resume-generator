# tailored-resume-generator

面向求职投递的 Codex Skill：从一份基础简历和可复用项目库出发，为不同 JD 生成定制简历、HTML/PDF 版本、项目筛选记录、修改历史和专家审阅结果。

这个 skill 的目标不是“花式改写”，而是建立一套可复现的投递流程：

- 把个人经历沉淀成 `resume-bank`
- 针对 JD 分析岗位优先级和关键词
- 从项目库中筛选最相关经历
- 生成 Markdown / HTML / PDF 简历
- 做版面检查、事实边界检查和专家式对抗审核
- 只有审核通过后才交给人工投递

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

## 快速安装

克隆到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Hfx-J/tailored-resume-generator.git \
  ~/.codex/skills/tailored-resume-generator
```

如果你已经有同名目录，可以更新：

```bash
cd ~/.codex/skills/tailored-resume-generator
git pull
```

## 快速上手

### 1. 准备基础简历

建议先准备一份已有简历，例如：

```text
/path/to/my_resume.pdf
```

然后对 Codex 说：

```text
请用 tailored-resume-generator，根据我的简历 /path/to/my_resume.pdf 初始化 resume-bank，
工作目录放在 /path/to/job-plan
```

生成后的结构通常是：

```text
resume-bank/
├── base-profile.md
├── projects/
├── outputs/
└── applications/
```

初始化后的项目卡默认需要人工核对，尤其是日期、指标、作者排序、项目边界和保密信息。

### 2. 提供 JD 生成投递包

把目标 JD 发给 Codex，例如：

```text
请基于这个 JD 生成一版简历：
【公司】...
【岗位】...
【岗位职责】...
【任职要求】...
```

skill 会创建：

```text
resume-bank/applications/YYYYMMDD-company-role/
├── jd.md
├── metadata.md
├── jd-analysis.md
├── selected-projects.md
├── resume_v1.md
├── resume_v1.html
├── resume_v1.pdf
├── expert-review_v1.md
├── CHANGELOG.md
└── notes.md
```

### 3. 迭代修改

你可以继续给具体反馈：

```text
研究经历太短了，把论文和项目展开一点
```

```text
第一页太空，保持单栏格式但提高密度
```

```text
论文标题下面加论文链接
```

每次修改都应该生成新的版本，例如 `resume_v2.md/html/pdf`，不要覆盖已经审核过的版本。

## 中文技术简历规则

针对中文算法/工程简历，默认采用保守技术风格：

- A4，必要时两页
- 单栏布局
- 白底、克制红色强调
- 宋体 / SimSun 风格正文
- 有照片和学校 Logo 时放在页眉
- 不使用花哨卡片、渐变、双栏侧边栏或营销风 hero
- 密度要足，但不能裁切、重叠或底部贴边

论文区遵循主次层级：

- 最相关的 1-2 篇作为主论文
- 其他论文放入 `补充论文成果`
- 论文标题必须使用真实标题
- 有公开链接时，标题下方放紧凑链接行，如 `IEEE Xplore`
- 项目库中保留完整 URL 和上传说明

## 专家门禁

每个 JD 定制版本在交付前都要通过对抗性专家审核。

审核专家身份会根据 JD 动态生成，例如：

- 端到端自动驾驶算法负责人
- 多模态世界模型面试官
- SLAM / 定位算法负责人
- 机器人系统落地负责人

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

## 常用脚本

初始化项目库：

```bash
python scripts/init_resume_bank.py /path/to/resume.pdf /path/to/resume-bank
```

创建投递包：

```bash
python scripts/create_application_package.py \
  --bank /path/to/resume-bank \
  --company 公司名 \
  --role 岗位名 \
  --jd /path/to/jd.md
```

从 Markdown 生成 HTML：

```bash
python scripts/generate_resume_html.py \
  /path/to/resume_v1.md \
  /path/to/resume_v1.html
```

具体参数以脚本实现为准；实际使用时更推荐让 Codex 根据当前目录和文件自动调用。

## 事实安全原则

- 不编造公司、岗位、时间、论文、奖项、指标或工具
- 不把“了解”升级成“精通”
- 缺失事实用占位符，例如 `[量化指标待补]`
- 未公开论文不要伪造链接
- 私有项目不要泄露地图、数据、客户和内部实现细节
- 论文作者排序、收录状态和链接要写入项目卡

## 推荐工作流

1. 初始化 `resume-bank`
2. 人工核对 `base-profile.md` 和 `projects/*.md`
3. 为每个 JD 创建独立 application package
4. 写入原始 `jd.md`
5. 生成 `jd-analysis.md` 和 `selected-projects.md`
6. 生成 `resume_vN.md/html/pdf`
7. 渲染 PDF 截图检查版面
8. 运行专家门禁
9. 通过后投递，不通过则修复并生成下一版

## 适用场景

- 2027 秋招 / 校招投递
- 自动驾驶、机器人、SLAM、感知、端到端算法岗位
- 多 JD 批量定制简历
- 中文技术简历 PDF 打磨
- 论文/项目经历较多，需要为不同岗位重排重点的候选人

## 不适合做什么

- 不适合伪造经历或夸大项目边界
- 不适合把一份简历无脑套所有岗位
- 不适合替代人工事实核对
- 不适合公开上传含个人隐私的真实简历材料
