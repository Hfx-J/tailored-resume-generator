# Project Card Template

Use one Markdown file per project, internship, work experience, research item, competition, or representative achievement. Keep cards factual and reusable across roles.

## Blank Card

```markdown
---
id: unique-project-id
title:
type: project|internship|work|research|competition
role:
period:
domain_tags: []
skill_tags: []
preferred_for: []
status: draft|needs_review|verified
confidentiality: private|redacted|public
---

## Context

What the project/system/work was, who it served, and what problem it solved.

## What I Did

- Action, responsibility, technical choice, or collaboration detail.

## Deliverables

- Concrete outputs: system, module, paper, dataset, report, dashboard, process, script, model, campaign, etc.

## Metrics / Evidence

- Numbers, rankings, performance changes, adoption, business impact, awards, or source evidence.
- Use `[量化指标待补]` when the metric is useful but missing.

## Publication Metadata

Use this block for published, accepted, submitted, or representative papers. Keep it factual and update it when the official index changes.

- Venue:
- Level:
- Authorship:
- Paper link:
- Upload note:
- Source:

## Interview Talking Points

- Details worth expanding in interviews: tradeoffs, decisions, failures, debugging, collaboration.

## Do Not Claim

- Claims that must not be made, such as tools not actually used, unverified metrics, confidential details, or overstated ownership.
```

## Initialization Review Checklist

After extracting cards from an existing resume, ask the user to verify:

- Project boundaries: one card should represent one coherent project or experience.
- Dates and roles: periods, titles, and ownership level must match the source.
- Skills: each `skill_tags` item must be supported by the card content.
- Metrics: copied metrics must exist in the resume; inferred metrics need placeholders.
- Confidentiality: sensitive company, dataset, client, or project details should be redacted.

## Publication Review Checklist

For paper cards, verify:

- Title: use the real paper title from the source; do not replace it with an informal acronym or internally shortened title.
- Authorship: record exact order, including "共同第一作者（排名第一/第二）" or "第二作者（学生一作）" when relevant.
- Link: keep the full canonical URL in the card. Use IEEE Xplore / ACM / arXiv / official conference program pages when available.
- Status: distinguish published, accepted, in press, submitted, and private/unpublished work.
- Upload note: record which PDF version should be uploaded, such as IEEE Xplore final version, camera-ready, or acceptance proof.
- Source: record whether the link/order/status came from user confirmation, original resume extraction, DBLP, IEEE Xplore, PaperCept, or another official source.
