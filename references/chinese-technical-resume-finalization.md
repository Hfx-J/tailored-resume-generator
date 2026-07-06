# Chinese Technical Resume Finalization

Use this reference after a JD-specific resume package already exists and the user is iterating on visual quality, section density, PDF layout, or Chinese technical-resume polish.

## Operating Principle

Treat the latest accepted resume version as the layout source of truth. Do not redesign the whole resume unless the user explicitly rejects the template. Make bounded section patches, create a new `resume_vN`, export PDF, render screenshots, inspect visually, and record the change.

## Version Workflow

1. Identify the application package:

```text
resume-bank/applications/YYYYMMDD-company-role/
```

2. Read:
   - `jd.md`
   - `jd-analysis.md`
   - `selected-projects.md`
   - latest `resume_vN.md`
   - latest `resume_vN.html`
   - `CHANGELOG.md`

3. Create the next version:

```bash
cp resume_vOLD.md resume_vN.md
cp resume_vOLD.html resume_vN.html
```

4. Edit only the new version.
5. Regenerate `resume_vN.pdf`.
6. Render pages and inspect.
7. Run the adversarial expert gate in `adversarial-resume-review.md`.
8. Append `CHANGELOG.md`.

Never overwrite a reviewed or submitted version.

## Accepted Chinese Technical Resume Style

Default to this style for conservative engineering/algorithm resumes unless the user asks otherwise:

- A4, two pages when necessary.
- Single-column layout.
- White background with restrained red accents.
- Original-style red section ribbons and full-width divider lines.
- Header with headshot, name/contact/target, and school logo when assets are provided.
- Songti/SimSun-style Chinese body text.
- Dense but readable layout; avoid first-page whitespace and bottom clipping.
- No flashy cards, double-column sidebars, gradients, decorative blobs, or marketing-like hero layout.

Use body size based on rendered fit. If 12pt breaks the page, reduce proportionally while preserving Songti/SimSun.

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
- Use left-side venue/role/date tags and right-side title/contribution text.
- Use real paper titles, especially when a publication link is shown. Do not replace a real title with an acronym-only or informal shortened title. If the real title is too long, tighten the local layout first; only shorten after the user explicitly accepts a display-title abbreviation.
- If a paper has a public link, place a link row directly under the title. In HTML/PDF, use compact clickable text such as `IEEE Xplore`, `arXiv`, or `ICRA 2026 官方程序页` instead of a naked long URL. Keep the full URL in the Markdown/project card. For submitted/private papers without a public page, use a truthful status such as `论文链接：在投未公开`; do not fabricate a link.
- Keep the title, link, and contribution text in one right-side content block. Avoid CSS layouts where a multi-line left meta tag creates a large vertical gap between title and link.

HTML pattern:

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

CSS pattern:

```css
.paper-secondary-group {
  margin-top: 1.2mm;
  padding-top: .9mm;
  border-top: 1px solid #ead8d6;
}
.paper-secondary-title {
  color: var(--accent);
  font-size: 9.8pt;
  font-weight: 800;
}
.paper-mini {
  display: grid;
  grid-template-columns: 31mm minmax(0, 1fr);
  column-gap: 3.2mm;
  margin-top: .55mm;
  align-items: start;
}
.paper-mini .mini-meta {
  color: var(--quiet);
  font-size: 9.35pt;
  line-height: 1.16;
  white-space: nowrap;
}
.paper-mini .mini-main {
  min-width: 0;
}
.paper-mini .mini-title {
  font-size: 9.35pt;
  line-height: 1.08;
  font-weight: 700;
}
.paper-mini .mini-link {
  margin: .08mm 0 0;
  color: var(--quiet);
  font-size: 8.35pt;
  line-height: 1.06;
}
.paper-mini .mini-content {
  margin-top: .08mm;
  font-size: 9.65pt;
  line-height: 1.11;
  text-align: justify;
}
```

## Fixed-Layout Patch Rules

When the user dislikes one section:

1. Render before editing.
2. Identify the smallest affected section.
3. Patch only that section.
4. Preserve header, photo, logo, section labels, margins, and page count.
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

- `Pages: 2` unless the user approved another count.
- `Page size: 594.96 x 841.92 pts (A4)`.

Render:

```bash
pdftoppm -png -f 1 -l 2 -r 150 'APPLICATION_DIR/resume_vN.pdf' /tmp/resume_vN_page
```

Inspect:

- `/tmp/resume_vN_page-1.png`
- `/tmp/resume_vN_page-2.png`

Check self-contained HTML:

```bash
rg -n "<script\\s+src|<link\\s|@import|cdn\\.jsdelivr|unpkg\\.com|html2canvas\\.hertzen\\.com/dist|figure\\.jpg|SEU\\.png|/media/|file://|resume_vOLD" 'APPLICATION_DIR/resume_vN.html'
```

No output is expected for external resources, local path leaks, or stale version names. Embedded inline assets as data URIs are acceptable.

## Visual QA Checklist

Page 1:

- Headshot is visible and not stretched.
- School logo is visible and not oversized.
- Header, education, internships, and first project do not clip.
- Bullets do not collide with section labels or page bottom.

Page 2:

- Research has clear primary/secondary hierarchy.
- Additional papers do not appear as three or more stacked full-weight headings.
- Paper titles match the real publication titles when links are shown.
- Paper title, link, and contribution text are vertically compact; there is no blank gap caused by left-side venue/role/date tags.
- Skills and JD match sections are fully visible.
- Last bullet stays above the page bottom with visible margin.

Overall:

- No excessive whitespace.
- No text overlap.
- No flashy template choices.
- Bold emphasis creates hierarchy rather than noise.

## Adversarial Expert Gate

Before final handoff, read `adversarial-resume-review.md` and produce `expert-review_vN.md`.

- Generate the expert persona from this JD and this resume, such as an autonomous-driving world-model hiring manager for world-model/VLA/environment-perception roles.
- Give the expert the original resume/source extraction, JD, JD analysis, selected projects, current resume version, and PDF QA evidence.
- Treat `CRITICAL` and unresolved `MAJOR` findings as blocking.
- If blocked, write `review-fix-plan_vN.md`, create the next resume version, re-export PDF, and re-review.
- Only `PASS_FOR_HUMAN_REVIEW` allows the final response to present the resume as ready for human review.

## Changelog Entry

Use:

```markdown
## YYYY-MM-DD HH:MM - vN

- Trigger: user revision | formatting pass | fact correction
- Inputs: `resume_vOLD.md`, `resume_vOLD.html`, `resume_vOLD.pdf`
- Outputs: `resume_vN.md`, `resume_vN.html`, `resume_vN.pdf`
- Changes:
  - ...
- Verification:
  - Rendered vN as a 2-page A4 PDF.
  - Visually checked page screenshots for clipping/overlap.
  - Checked HTML has no external resource links or local path leaks.
  - Expert review: PASS_FOR_HUMAN_REVIEW | BLOCKED_BY_EXPERT | BLOCKED_BY_EXPERT_USER_OVERRIDE.
  - Expert findings: CRITICAL 0, MAJOR 0, MINOR 0.
```

## Final Response

If `expert-review_vN.md` returns `PASS_FOR_HUMAN_REVIEW`, link `resume_vN.pdf`, `resume_vN.html`, and `resume_vN.md`. Mention page count, visual QA, expert gate result, and any remaining fact-safety caveats.

If the expert gate blocks the version, link `expert-review_vN.md` and `review-fix-plan_vN.md` instead, then state that the resume is not ready for human review yet.
