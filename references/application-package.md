# Application Package Contract

Use an application package for every JD-specific resume tailoring session. The package preserves the original JD, decision trail, resume versions, and revision history.

## Default Location

```text
resume-bank/applications/YYYYMMDD-company-role/
```

Create the folder with `scripts/create_application_package.py` when possible.

## Required Files

- `jd.md`: original JD text. Create once and do not overwrite.
- `metadata.md`: company, role, date, source file, package slug, and status.
- `jd-analysis.md`: target role, hard requirements, preferred requirements, keywords, and gaps.
- `selected-projects.md`: scored project shortlist, selected cards, rejected cards, and reasons.
- `resume_vN.md`: Markdown resume snapshots, starting with `resume_v1.md`.
- `resume_vN.html`: HTML version matching the Markdown snapshot when HTML output is requested.
- `expert-review_vN.md`: adversarial expert gate result for the matching resume version before final handoff.
- `review-fix-plan_vN.md`: required when `expert-review_vN.md` returns blocking findings.
- `CHANGELOG.md`: chronological record of generation and edits.
- `notes.md`: open questions, interview hooks, cover letter ideas, and user feedback.

## Version Rules

- Never overwrite a submitted or reviewed resume version.
- Create the next version number by scanning existing `resume_v*.md` files and adding 1.
- Use `resume_vN.md` and `resume_vN.html` for matching versions.
- Match expert reviews to the same version number: `expert-review_vN.md` reviews `resume_vN`.
- If expert review blocks the version, write `review-fix-plan_vN.md`, then create `resume_vN+1`.
- Do not hand off a resume as final until `expert-review_vN.md` returns `PASS_FOR_HUMAN_REVIEW`.
- If a change only updates analysis or notes, update `CHANGELOG.md` without creating a resume version.

## Metadata Status Values

Use one of these statuses in `metadata.md`:

- `draft`: package exists but no resume version is ready.
- `under_expert_review`: a resume version has been generated and is being reviewed.
- `blocked_by_expert`: latest expert review has `CRITICAL` or unresolved `MAJOR` findings.
- `passed_for_human_review`: latest expert review returned `PASS_FOR_HUMAN_REVIEW`.
- `blocked_by_expert_user_override`: user explicitly stopped despite unresolved blocking findings.

## Changelog Format

Use this entry format:

```markdown
## YYYY-MM-DD HH:MM - vN

- Trigger: initial generation | JD change | user revision | fact correction | formatting pass
- Inputs: `jd.md`, selected project IDs, user notes
- Outputs: `resume_vN.md`, `resume_vN.html`
- Changes:
  - ...
- Open facts:
  - ...
- Verification:
  - Expert identity: ...
  - Expert gate: PASS_FOR_HUMAN_REVIEW | BLOCKED_BY_EXPERT | BLOCKED_BY_EXPERT_USER_OVERRIDE
  - Findings: CRITICAL 0, MAJOR 0, MINOR 0
```

## Safety Rules

- Keep raw JD text intact for traceability.
- Mark missing facts with placeholders instead of filling them from inference.
- Record user-confirmed project choices in `selected-projects.md`.
- Move rejected but plausible projects into a "Not used" section with short reasons.
