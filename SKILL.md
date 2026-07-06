---
name: tailored-resume-generator
description: Build JD-specific resumes from a reusable personal experience library. Use when the user provides one or more job descriptions and wants Codex to initialize a resume-bank from an existing resume, create per-JD application packages, select relevant project cards, tailor resume content for ATS and human reviewers, or generate Markdown and HTML resume versions with change history and without fabricating experience.
---

# Tailored Resume Generator

## Purpose

Generate job-specific resumes from a reusable `resume-bank` of profile data and project cards. Use this skill as a JD-driven resume assembler: analyze the target role, score available experiences, ask for confirmation when needed, then produce Markdown and HTML resume drafts. When the user asks for a polished Chinese resume PDF or iterative layout refinement, use the finalization workflow in `references/chinese-technical-resume-finalization.md`. Before any JD-specific resume is treated as complete for human review, run the dynamic adversarial expert gate in `references/adversarial-resume-review.md`.

## Required Inputs

If missing, request only the information needed for the current task:

- Target JD text, company name, and role title.
- Existing `resume-bank` path, defaulting to `./resume-bank`.
- Existing resume file when initializing a new bank.
- Application package path when continuing an existing JD tailoring session.
- Output preference when not obvious: Markdown, HTML, or both.

## Workflows

### Initialize A Resume Bank

Use this when no project library exists or the user asks to build one from an existing resume.

1. Run or adapt `scripts/init_resume_bank.py` against the provided resume.
2. Create `base-profile.md`, `projects/*.md`, `outputs/`, and `applications/`.
3. Mark extracted cards as `status: needs_review`.
4. Tell the user that extracted cards are drafts and must be fact-checked.
5. Output a review checklist covering project names, dates, technologies, metrics, and claims.

For detailed card structure, read `references/project-card-template.md`.

### Create Or Use An Application Package

Use this before tailoring a resume for a specific JD.

1. Create or reuse `resume-bank/applications/<YYYYMMDD-company-role>/`.
2. Save the original JD as `jd.md`; do not overwrite it after creation.
3. Save JD analysis, selected project scoring, resume versions, notes, and change history inside that package.
4. Use `scripts/create_application_package.py` when the user provides a JD file or when a consistent package skeleton is useful.
5. Read `references/application-package.md` for the directory contract and version rules.

### Tailor A Resume For A JD

1. Analyze the JD and extract:
   - target role, seniority, domain, hard requirements, preferred qualifications, keywords, and language.
2. Create or identify the application package for this JD.
3. Save the analysis to `jd-analysis.md`.
4. Read `base-profile.md` and all cards under `projects/`.
5. Score cards using `references/role-fit-rubric.md`.
6. Save the top 4-6 cards and rationale to `selected-projects.md`.
7. Ask for confirmation before final assembly unless the user explicitly requests automatic generation.
8. Generate the next resume version according to `references/output-contract.md`.
9. Save files as `resume_vN.md` and `resume_vN.html` inside the package, then update `CHANGELOG.md`.
10. Run the dynamic adversarial expert review in `references/adversarial-resume-review.md`.
11. Treat the resume as complete only if `expert-review_vN.md` returns `PASS_FOR_HUMAN_REVIEW`; otherwise create a fix plan and another version.

### Finalize A Polished Chinese Technical Resume

Use this after a JD-specific resume draft exists and the user asks for PDF polish, visual refinement, original-resume style matching, photo/logo inclusion, single-column layout, or iterative fixes to sections such as internships, projects, and research papers.

1. Continue from the existing application package; do not create a parallel package or separate one-off skill.
2. Read `references/chinese-technical-resume-finalization.md`.
3. Create the next `resume_vN.md` / `resume_vN.html` version before editing.
4. Preserve the accepted page architecture and patch only the smallest affected section.
5. Export PDF, render page images, visually inspect both pages, check for resource leaks, and update `CHANGELOG.md`.
6. Run the dynamic adversarial expert review. Do not hand off the resume to the user as final unless the gate result is `PASS_FOR_HUMAN_REVIEW`.

### Run Dynamic Expert Adversarial Review

Use this before final handoff for every JD-specific resume version.

1. Read `references/adversarial-resume-review.md`.
2. Build the evidence packet from the original resume extraction, `base-profile.md`, relevant project cards, `jd.md`, `jd-analysis.md`, `selected-projects.md`, the current `resume_vN.md`, and any PDF/render QA artifacts.
3. Generate the expert identity from the resume and JD content rather than using a generic reviewer.
4. If sub-agent tooling is available and the user asked for an expert agent, spawn the expert as a no-edit reviewer. Otherwise run the same protocol locally.
5. Save the result as `expert-review_vN.md`.
6. If the result is `BLOCKED_BY_EXPERT`, create `review-fix-plan_vN.md`, produce `resume_vN+1`, and review again.
7. Only `PASS_FOR_HUMAN_REVIEW` permits final handoff. If the user explicitly stops the loop despite open blocking issues, record `BLOCKED_BY_EXPERT_USER_OVERRIDE` and do not describe the resume as expert-approved.

## Resume-Bank Layout

Use this default structure:

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
        ├── expert-review_v1.md
        ├── review-fix-plan_v1.md
        ├── CHANGELOG.md
        └── notes.md
```

Keep personal facts in the bank, not inside this skill. The skill must stay reusable.

## Truthfulness Rules

- Never invent companies, roles, dates, technologies, publications, awards, metrics, or certifications.
- Do not upgrade skill level, for example from "了解" to "精通", unless the source supports it.
- Use placeholders for missing facts: `[量化指标待补]`, `[项目规模待补]`, `[英文表述待确认]`.
- Preserve uncertainty from source materials and surface it in the review notes.
- Include `Do Not Claim` constraints from project cards when tailoring bullets.

## Output Defaults

- Follow the JD language: Chinese JD produces Chinese resume; English JD produces English resume.
- Default to Markdown plus HTML when the user asks for files.
- Keep early-career resumes to one page unless the user asks for a longer archive version.
- Put the most JD-relevant experience first within each section, while preserving truthful chronology inside role histories.

## Resource Guide

- `references/project-card-template.md`: project card format and initialization review checklist.
- `references/role-fit-rubric.md`: JD parsing and project scoring rules.
- `references/output-contract.md`: Markdown and HTML resume output requirements.
- `references/application-package.md`: per-JD folder, versioning, and changelog contract.
- `references/chinese-technical-resume-finalization.md`: final Chinese technical resume polish workflow, single-column A4 layout rules, research-section hierarchy, and PDF QA checklist.
- `references/adversarial-resume-review.md`: dynamic expert persona, adversarial review protocol, blocking severity rules, and pass/fail gate.
- `assets/resume-template.html`: self-contained HTML template.
- `scripts/init_resume_bank.py`: create a draft resume bank from an existing resume.
- `scripts/create_application_package.py`: create a per-JD application package.
- `scripts/generate_resume_html.py`: convert a Markdown resume draft to a styled HTML file.
