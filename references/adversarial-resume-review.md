# Adversarial Resume Review

Use this protocol before treating any JD-specific resume as ready for human review. The review is intentionally adversarial: the expert should find weak claims, evidence gaps, poor JD alignment, and layout issues that would reduce interview probability.

## Completion Gate

A resume version is not complete until `expert-review_vN.md` returns:

```text
PASS_FOR_HUMAN_REVIEW
```

PDF export, visual QA, or user satisfaction with appearance is not enough. If the result is `BLOCKED_BY_EXPERT`, produce a new version and review again.

## Evidence Packet

Give the reviewer only evidence-backed materials:

- Original resume file or extracted source text when available.
- `base-profile.md`.
- Relevant `projects/*.md` cards, including `Do Not Claim` constraints.
- `jd.md`.
- `jd-analysis.md`.
- `selected-projects.md`.
- Current `resume_vN.md`.
- Current `resume_vN.html` and `resume_vN.pdf` when layout is in scope.
- Rendered page images or visual QA notes when PDF quality is in scope.
- `CHANGELOG.md`.

If the original resume source is unavailable, mark `ORIGINAL_RESUME_MISSING`. If project cards and base profile still support the claims, this is usually `MAJOR`; if no source evidence supports key claims, it is `CRITICAL`.

## Dynamic Expert Persona

Generate the expert identity from the JD and resume. Do not use a generic "resume expert".

Construct the persona with these lenses:

- Target-domain hiring manager: derived from the role title, company domain, and the top JD requirements.
- Technical interviewer: derived from the most important methods in the JD, such as world models, VLA, multimodal perception, SLAM, 3D reconstruction, deployment, or training efficiency.
- Production reviewer: include this when the JD mentions deployment, mass production, edge/cloud runtime, data pipeline, closed-loop simulation, or business value.
- Truthfulness reviewer: include this when the resume has publications, internships, metrics, confidential systems, or claims adjacent to but not directly proven by the source.

Persona template:

```text
你是<目标领域>的一线 Hiring Manager / 技术面试官，正在筛选<届别/岗位>候选人。你熟悉<JD核心技术关键词>，也会严厉追问候选人简历中关于<候选人核心经历关键词>的真实性、深度、边界和可落地性。
```

Examples:

- World model / VLA / environment perception JD: autonomous-driving multimodal world-model hiring manager with vehicle/cloud deployment and training-efficiency review lenses.
- SLAM / localization JD: robotics localization and mapping algorithm lead with geometric consistency, real-time, and sensor-fusion review lenses.
- End-to-end unmanned delivery JD: autonomous delivery end-to-end driving lead with perception-planning integration, simulation, and safety review lenses.

## Review Dimensions

Review every version across these dimensions:

1. Truthfulness and evidence consistency: every company, date, role, metric, publication status, method, and claim must be supported.
2. JD priority fit: the first half of the resume must surface evidence for the JD's highest-priority requirements.
3. Recruiter first-screen effectiveness: structure, section order, keywords, and summary must make the candidate's fit obvious without reading every bullet.
4. Technical credibility: bullets must survive interview follow-up, with clear method, responsibility boundary, implementation detail, and result.
5. Prompt/meta contamination: visible resume copy must not contain internal instructions, placeholders that should have been resolved, or wording such as "针对该岗位", "能力边界", "相邻能力表述", "可迁移经验" when it reads like prompt residue.
6. Layout and PDF quality: check density, hierarchy, alignment, clipping, page balance, photo/logo quality, and whether the format is appropriate for a conservative technical resume.
7. Confidentiality and risk: do not expose private contact artifacts, local file paths, internal links, NDA-sensitive details, or exaggerated unpublished results.

## Severity Taxonomy

Use `CRITICAL`, `MAJOR`, and `MINOR`.

`CRITICAL` blocks completion. Examples:

- Fabricated or source-unsupported company, role, date, degree, publication, award, metric, deployment, or ownership claim.
- A claim contradicts the original resume, project cards, or JD analysis.
- Prompt-like text, internal reviewer notes, or editing instructions appear in visible resume copy.
- PDF has clipping, overlapping text, missing pages, missing key assets, unreadable text, or wrong candidate identity.
- The resume implies accepted publication or production deployment when the source only proves submission, experiment, prototype, or participation.

`MAJOR` blocks completion by default. Examples:

- The first page does not clearly answer the JD's core requirements.
- Important internships, research, or projects are too compressed to show technical depth.
- Keyword stuffing weakens credibility.
- Claims use unsupported intensity such as "精通", "主导", "量产", "闭环", "端到端", or "世界模型" without enough evidence.
- The layout is readable but has poor hierarchy, excessive whitespace, chaotic emphasis, or misplaced section order.

`MINOR` does not block completion when no `CRITICAL` or unresolved `MAJOR` remains. Examples:

- Slight wording polish.
- Small alignment or spacing improvements.
- Optional interview hook additions.

## Pass Criteria

Return exactly one gate result:

- `PASS_FOR_HUMAN_REVIEW`: zero `CRITICAL` and zero unresolved `MAJOR`.
- `BLOCKED_BY_EXPERT`: at least one `CRITICAL` or unresolved `MAJOR`.
- `BLOCKED_BY_EXPERT_USER_OVERRIDE`: the user explicitly stops the repair loop despite unresolved blocking findings.

Do not call a resume "final", "complete", or "expert-approved" unless the gate result is `PASS_FOR_HUMAN_REVIEW`.

## Expert Agent Execution

If sub-agent tooling is available and the user asked for an expert agent, spawn a no-edit reviewer. The expert receives the evidence packet and this protocol, then returns only the review. The expert must not rewrite the resume directly.

If sub-agent tooling is unavailable, the main agent runs the same protocol locally and still writes `expert-review_vN.md`.

The expert must cite exact resume text or evidence gaps. The expert must not invent achievements, metrics, technologies, or publications while proposing fixes.

## Output Format

Save the review as `expert-review_vN.md`:

```markdown
# Expert Review - resume_vN

## Expert Identity

- Persona: ...
- JD-derived lenses: ...
- Resume evidence under review: ...

## Gate Result

- Result: PASS_FOR_HUMAN_REVIEW | BLOCKED_BY_EXPERT | BLOCKED_BY_EXPERT_USER_OVERRIDE
- Severity counts: CRITICAL 0, MAJOR 0, MINOR 0
- Overall score: N/10

## Blocking Findings

| # | Severity | Resume text / evidence gap | Why it matters | Required fix |
|---|---|---|---|---|

## Truthfulness Audit

| Claim type | Status | Evidence | Notes |
|---|---|---|---|

## JD Fit Audit

| JD priority | Resume evidence | Verdict | Required change |
|---|---|---|---|

## Layout And PDF Audit

| Area | Verdict | Notes |
|---|---|---|

## Human Polish Queue

- Minor items that can wait until after pass.

## Re-review Requirement

- State whether `review-fix-plan_vN.md` and `resume_vN+1` are required.
```

## Repair Loop

When the gate result is `BLOCKED_BY_EXPERT`:

1. Create `review-fix-plan_vN.md`.
2. List each `CRITICAL` and `MAJOR` finding, the evidence source to use, and the exact resume area to patch.
3. Create `resume_vN+1.md` and matching exports.
4. Re-run PDF/render QA if layout is affected.
5. Re-run this expert review on the new version.

Do not resolve a finding by adding a stronger claim unless the evidence packet supports it.
