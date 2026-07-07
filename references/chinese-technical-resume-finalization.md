# Chinese Technical Resume Finalization

Use this reference after a JD-specific resume package already exists and the user is iterating on visual quality, section density, PDF layout, original-resume style matching, or Chinese technical-resume polish.

## Operating Principle

The resume's visual style must come from evidence, not from a fixed template. Analyze the original resume or latest accepted version first, preserve the accepted page architecture, then make bounded section patches. Do not redesign the whole resume unless the user explicitly rejects the current style.

## Version Workflow

1. Identify the application package:

```text
resume-bank/applications/YYYYMMDD-company-role/
```

2. Read:
   - `jd.md`
   - `jd-analysis.md`
   - `selected-projects.md`
   - original resume source or extraction notes when available
   - latest `resume_vN.md`
   - latest `resume_vN.html`
   - latest rendered PDF or screenshots when available
   - `CHANGELOG.md`

3. Create or update visual style evidence:

```text
visual-style_vN.md
```

Record the page structure, font choices, colors, section headers, divider rules, density, emphasis pattern, and any assets such as a headshot or school logo.

4. Create the next version:

```bash
cp resume_vOLD.md resume_vN.md
cp resume_vOLD.html resume_vN.html
```

5. Edit only the new version.
6. Regenerate `resume_vN.pdf`.
7. Render pages and inspect.
8. Run the adversarial expert gate in `adversarial-resume-review.md`.
9. Append `CHANGELOG.md`.

Never overwrite a reviewed or submitted version.

## Original Resume Style Inheritance

Use this precedence order for visual decisions:

1. User's explicit visual instruction.
2. Original resume PDF, DOCX, HTML, Markdown, or rendered screenshots.
3. Latest accepted `resume_vN.html/pdf` in the same application package.
4. A neutral, readable, ATS-friendly technical resume fallback when no style source exists.

Extract these style facts before editing:

- Page: paper size, page count, margins, header/footer, photo/logo placement.
- Structure: single-column or multi-column layout, section order, timeline pattern, left/right metadata treatment.
- Typography: Chinese and English font family, body size, heading size, line height, text alignment.
- Color: primary text color, accent colors, divider colors, link colors, background treatment.
- Section headers: ribbons, lines, numbered labels, plain headings, spacing before/after sections.
- Density: paragraph spacing, bullet spacing, amount of content per page, bottom margin.
- Emphasis: bold rhythm, metric highlighting, role/project title treatment, tag style.

Only inherit a specific visual rule when evidence supports it. Do not default every resume to white background with red accents, red section ribbons, Songti/SimSun typography, single-column layout, or any other fixed style unless the original resume or user instruction uses that style.

When no style source is available, ask for the original resume if visual matching matters. If the user asks to proceed without it, use a conservative fallback: print-friendly A4, clean headings, readable density, no decorative elements that reduce ATS or PDF reliability.

## Content Rules

- Expand internships and projects with: problem/context, method, implementation details, and measurable result.
- Lead with JD-relevant evidence, but keep chronology truthful inside each role.
- Use bold for section labels, role/project names, leading bullet keywords, and key metrics only.
- Do not bold every title and every result; the page needs a visual rhythm.
- Keep unsupported claims out of the resume. Do not claim full sensor-to-decision autonomous driving, world-model closed-loop deployment, independent 3DGS work, or accepted top-conference publications unless the resume bank proves them.
- Preserve truthful boundaries internally, but do not put prompt-like caveats such as "针对该岗位", "相邻能力表述", "能力边界", or "可迁移经验" into visible resume copy unless they are natural, candidate-facing wording.

## Research Section Pattern

Avoid formatting many papers as equal stacked headings. Use a primary/secondary hierarchy:

- Keep the strongest 1-2 papers as primary blocks.
- Put additional papers under `补充论文成果`.
- Use real paper titles, especially when a publication link is shown. Do not replace a real title with an acronym-only or informal shortened title. If the real title is too long, tighten the local layout first; only shorten after the user explicitly accepts a display-title abbreviation.
- If a paper has a public link, place a link row directly under the title. In HTML/PDF, use compact clickable text such as `IEEE Xplore`, `arXiv`, or `ICRA 2026 官方程序页` instead of a naked long URL. Keep the full URL in the Markdown/project card. For submitted/private papers without a public page, use a truthful status such as `论文链接：在投未公开`; do not fabricate a link.
- Keep the title, link, and contribution text in one content block. Avoid CSS layouts where multi-line metadata creates a large vertical gap between title and link.
- Match the original resume's metadata style when possible. If the original uses left-side venue/role/date tags, preserve that rhythm; if it uses inline metadata, keep papers inline and compact.

HTML pattern for a primary paper:

```html
<div class="paper paper-featured">
  <div class="paper-head">
    <strong>Primary Paper Title</strong>
    <span class="date">2025年12月 - 至今</span>
  </div>
  <p class="meta">第一作者 | T-RO 在投</p>
  <p class="paper-link">论文链接：在投未公开</p>
  <p class="content">Contribution and result sentence.</p>
  <p class="content">Second result sentence if this is a primary paper.</p>
</div>
```

HTML pattern for compact supplementary papers:

```html
<div class="paper-secondary-group">
  <p class="paper-secondary-title">补充论文成果</p>
  <div class="paper-mini">
    <p class="mini-meta">RA-L | 学生一作<br>2024.11 - 2025.05</p>
    <div class="mini-main">
      <p class="mini-title">Real Full Paper Title From The Publication Source</p>
      <p class="mini-link">论文链接：<a href="https://example.com">IEEE Xplore</a></p>
      <p class="mini-content">One dense contribution/result sentence.</p>
    </div>
  </div>
</div>
```

Adapt spacing, color, and grid widths to the recorded original style. The snippets above are structure examples, not a mandatory visual theme.

## Fixed-Layout Patch Rules

When the user dislikes one section:

1. Render before editing.
2. Identify the smallest affected section.
3. Patch only that section.
4. Preserve the original or accepted style evidence: header, photo/logo treatment, section labels, margins, page count, typography, and accent colors.
5. Re-render and inspect.
6. If the patch causes overflow, first tighten local spacing or restructure the affected section; do not globally shrink the whole resume.

## PDF Export and QA

Export:

```bash
google-chrome --headless --disable-gpu --no-sandbox --disable-crash-reporter --disable-crashpad \
  --print-to-pdf='APPLICATION_DIR/resume_vN.pdf' \
  'file:///ABSOLUTE_URL_ENCODED_PATH/resume_vN.html'
```

Check geometry:

```bash
pdfinfo 'APPLICATION_DIR/resume_vN.pdf'
```

Expected for this workflow:

- Page count matches the user's requirement or the latest accepted resume.
- Page size matches the original resume or explicit user instruction; use A4 only when no source indicates otherwise.

Render:

```bash
pdftoppm -png -f 1 -l 2 -r 150 'APPLICATION_DIR/resume_vN.pdf' /tmp/resume_vN_page
```

Adjust the page range when the resume is not two pages.

Inspect:

- `/tmp/resume_vN_page-1.png`
- `/tmp/resume_vN_page-2.png`

Check self-contained HTML:

```bash
rg -n "<script\\s+src|<link\\s|@import|cdn\\.jsdelivr|unpkg\\.com|html2canvas\\.hertzen\\.com/dist|figure\\.jpg|SEU\\.png|/media/|file://|resume_vOLD" 'APPLICATION_DIR/resume_vN.html'
```

No output is expected for external resources, local path leaks, or stale version names. Embedded inline assets as data URIs are acceptable.

## Visual QA Checklist

Style inheritance:

- `visual-style_vN.md` or equivalent notes identify the style source.
- Layout, typography, color, section headers, dividers, density, and emphasis match the original or latest accepted resume unless the user requested a change.
- No fixed theme was imposed without evidence.

Page-level checks:

- Headshot and logo are visible, proportionate, and placed according to the inherited style when assets are used.
- Header, education, internships, projects, papers, skills, and JD match sections do not clip.
- Bullets do not collide with section labels or page bottom.
- Last visible line stays above the page bottom with a clear margin.

Research checks:

- Research has clear primary/secondary hierarchy.
- Additional papers do not appear as three or more stacked full-weight headings unless the original style intentionally uses that pattern and it remains readable.
- Paper titles match the real publication titles when links are shown.
- Paper title, link, and contribution text are vertically compact; there is no blank gap caused by metadata layout.

Overall:

- No excessive whitespace.
- No text overlap.
- No unsupported decorative redesign.
- Bold emphasis creates hierarchy rather than noise.

## Adversarial Expert Gate

Before final handoff, read `adversarial-resume-review.md` and produce `expert-review_vN.md`.

- Generate the expert persona from this JD and this resume, such as an autonomous-driving world-model hiring manager for world-model/VLA/environment-perception roles.
- Give the expert the original resume/source extraction, style evidence, JD, JD analysis, selected projects, current resume version, and PDF QA evidence.
- Treat `CRITICAL` and unresolved `MAJOR` findings as blocking.
- If blocked, write `review-fix-plan_vN.md`, create the next resume version, re-export PDF, and re-review.
- Only `PASS_FOR_HUMAN_REVIEW` allows the final response to present the resume as ready for human review.

## Changelog Entry

Use:

```markdown
## YYYY-MM-DD HH:MM - vN

- Trigger: user revision | formatting pass | fact correction
- Inputs: `resume_vOLD.md`, `resume_vOLD.html`, `resume_vOLD.pdf`, style source
- Outputs: `resume_vN.md`, `resume_vN.html`, `resume_vN.pdf`, `visual-style_vN.md`
- Changes:
  - ...
- Verification:
  - Rendered vN as a PDF with expected page count and page size.
  - Visually checked page screenshots for clipping/overlap.
  - Checked visual style inheritance against `visual-style_vN.md`.
  - Checked HTML has no external resource links or local path leaks.
  - Expert review: PASS_FOR_HUMAN_REVIEW | BLOCKED_BY_EXPERT | BLOCKED_BY_EXPERT_USER_OVERRIDE.
  - Expert findings: CRITICAL 0, MAJOR 0, MINOR 0.
```

## Final Response

If `expert-review_vN.md` returns `PASS_FOR_HUMAN_REVIEW`, link `resume_vN.pdf`, `resume_vN.html`, `resume_vN.md`, and the style evidence file. Mention page count, visual QA, expert gate result, and any remaining fact-safety caveats.

If the expert gate blocks the version, link `expert-review_vN.md` and `review-fix-plan_vN.md` instead, then state that the resume is not ready for human review yet.
