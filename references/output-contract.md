# Output Contract

Use this contract for generated resumes and related strategy notes.

## Required Response Before Final Resume

Before assembling the final resume, provide:

- JD priority analysis.
- Candidate fit summary.
- Project shortlist with scores.
- Gaps and missing facts.
- Confirmation request unless the user asked for automatic generation.

## Markdown Resume

Use standard headings:

```markdown
# Name

Contact line

## Professional Summary

## Skills

## Experience / Projects

## Education

## Awards / Certifications
```

Rules:

- Keep bullets concise and evidence-based.
- Use action + scope + method + result.
- Include JD keywords only when supported by the bank.
- Use placeholders for missing facts instead of inventing.
- Omit irrelevant cards even if they are impressive.

## HTML Resume

Use `assets/resume-template.html` or `scripts/generate_resume_html.py`.

Requirements:

- Self-contained HTML with embedded CSS.
- Print-friendly A4 layout.
- No external fonts, scripts, tracking, or images by default.
- Preserve simple headings, bullets, and contact information.

For polished Chinese technical resume PDFs, read `chinese-technical-resume-finalization.md` and follow its single-column layout, research-section hierarchy, PDF export, screenshot inspection, and HTML self-containment checks.

Before final handoff for any JD-specific resume, read `adversarial-resume-review.md` and produce `expert-review_vN.md`. Do not call the resume final unless the expert gate returns `PASS_FOR_HUMAN_REVIEW`.

## Final Notes

After the resume, include short notes:

- strongest positioning for this JD
- remaining facts to verify
- 2-3 interview talking points
- optional cover letter hooks when useful
