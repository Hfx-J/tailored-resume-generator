#!/usr/bin/env python3
"""Initialize a resume-bank workspace from an existing resume."""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree


SECTION_ALIASES = {
    "education": ["教育经历", "教育背景", "education"],
    "skills": ["技能", "专业技能", "技术栈", "skills", "technical skills"],
    "experience": ["项目经历", "实习经历", "工作经历", "科研经历", "竞赛经历", "professional experience", "experience", "projects"],
    "awards": ["荣誉", "奖项", "获奖", "awards", "honors"],
}


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix in {".html", ".htm"}:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
        raw = re.sub(r"(?is)<br\s*/?>", "\n", raw)
        raw = re.sub(r"(?is)</(p|div|section|li|h[1-6])>", "\n", raw)
        return html.unescape(re.sub(r"(?is)<[^>]+>", " ", raw))
    if suffix == ".docx":
        return read_docx(path)
    if suffix == ".pdf":
        return read_pdf(path)
    raise SystemExit(f"Unsupported resume format: {path.suffix}")


def read_docx(path: Path) -> str:
    try:
        with ZipFile(path) as archive:
            xml_bytes = archive.read("word/document.xml")
    except Exception as exc:  # pragma: no cover - defensive extraction
        raise SystemExit(f"Failed to read DOCX: {exc}") from exc

    root = ElementTree.fromstring(xml_bytes)
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragraphs = []
    for paragraph in root.iter(f"{namespace}p"):
        parts = [node.text or "" for node in paragraph.iter(f"{namespace}t")]
        text = "".join(parts).strip()
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs)


def read_pdf(path: Path) -> str:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise SystemExit("PDF extraction requires pdftotext. Convert the PDF to text, DOCX, Markdown, or HTML and retry.")
    result = subprocess.run([pdftotext, str(path), "-"], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "pdftotext failed")
    return result.stdout


def clean_lines(text: str) -> list[str]:
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return [line for line in lines if line]


def find_name(lines: list[str]) -> str:
    for line in lines[:8]:
        if len(line) <= 20 and not re.search(r"@|\d{5,}|电话|邮箱|email|phone", line, re.I):
            return line
    return "[姓名待补]"


def extract_contact(lines: list[str]) -> list[str]:
    contact = []
    for line in lines[:20]:
        if re.search(r"@|\b1[3-9]\d{9}\b|\+?\d[\d\s\-]{7,}|github|linkedin", line, re.I):
            contact.append(line)
    return contact or ["[联系方式待补]"]


def detect_sections(lines: list[str]) -> dict[str, list[str]]:
    markers: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        normalized = line.strip().lower().strip(":：")
        for key, aliases in SECTION_ALIASES.items():
            if any(alias.lower() == normalized or alias.lower() in normalized for alias in aliases):
                markers.append((index, key))
                break

    sections = {key: [] for key in SECTION_ALIASES}
    if not markers:
        sections["experience"] = lines
        return sections

    markers = sorted(markers)
    for marker_index, (start, key) in enumerate(markers):
        end = markers[marker_index + 1][0] if marker_index + 1 < len(markers) else len(lines)
        sections[key].extend(lines[start + 1 : end])
    return sections


def split_experience_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    heading_pattern = re.compile(r"(\d{4}[./-]\d{1,2}|\d{4}|项目|实习|公司|课题|竞赛|Research|Project|Intern|Engineer)", re.I)

    for line in lines:
        is_heading = bool(heading_pattern.search(line)) and len(line) <= 90 and not line.startswith(("-", "•", "*"))
        if is_heading and current:
            blocks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append(current)
    return [block for block in blocks if any(len(line) > 6 for line in block)]


def slugify(value: str, fallback: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value[:48] or fallback


def frontmatter_list(items: list[str]) -> str:
    return "[" + ", ".join(items) + "]"


def make_base_profile(lines: list[str], sections: dict[str, list[str]]) -> str:
    name = find_name(lines)
    contact = extract_contact(lines)
    skills = sections.get("skills") or ["[技能待整理]"]
    education = sections.get("education") or ["[教育经历待整理]"]
    awards = sections.get("awards") or []
    return "\n".join(
        [
            "# Base Profile",
            "",
            "## Identity",
            f"- Name: {name}",
            *[f"- Contact: {item}" for item in contact],
            "",
            "## Target Directions",
            "- [目标岗位方向待补]",
            "",
            "## Education",
            *[f"- {item}" for item in education],
            "",
            "## Global Skills",
            *[f"- {item}" for item in skills],
            "",
            "## Awards / Certifications",
            *([f"- {item}" for item in awards] if awards else ["- [奖项或证书待补]"]),
            "",
            "## Constraints",
            "- Do not invent metrics, titles, tools, or project ownership beyond source materials.",
            "- Cards generated during initialization require manual review before final use.",
            "",
        ]
    )


def make_project_card(block: list[str], index: int) -> tuple[str, str]:
    title = block[0][:80] if block else f"Extracted Experience {index}"
    project_id = slugify(title, f"experience-{index:02d}")
    body_lines = block[1:] if len(block) > 1 else ["[项目内容待补]"]
    content = "\n".join(
        [
            "---",
            f"id: {project_id}",
            f"title: {title}",
            "type: project",
            "role: [角色待确认]",
            "period: [时间待确认]",
            "domain_tags: []",
            "skill_tags: []",
            "preferred_for: []",
            "status: needs_review",
            "confidentiality: private",
            "---",
            "",
            "## Context",
            "[项目背景待补：说明项目服务对象、业务/研究问题、系统定位]",
            "",
            "## What I Did",
            *[f"- {line.lstrip('-•* ')}" for line in body_lines],
            "",
            "## Deliverables",
            "- [交付产物待补]",
            "",
            "## Metrics / Evidence",
            "- [量化指标待补]",
            "",
            "## Interview Talking Points",
            "- [可展开细节待补]",
            "",
            "## Do Not Claim",
            "- Do not claim facts not present in the source resume or later user confirmation.",
            "",
        ]
    )
    return project_id, content


def write_bank(resume: Path, output: Path, force: bool) -> None:
    if output.exists() and any(output.iterdir()) and not force:
        raise SystemExit(f"{output} already exists and is not empty. Use --force to overwrite generated files.")

    text = read_text(resume)
    lines = clean_lines(text)
    sections = detect_sections(lines)
    projects_dir = output / "projects"
    outputs_dir = output / "outputs"
    applications_dir = output / "applications"
    projects_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)
    applications_dir.mkdir(parents=True, exist_ok=True)

    (output / "base-profile.md").write_text(make_base_profile(lines, sections), encoding="utf-8")

    blocks = split_experience_blocks(sections.get("experience") or lines)
    if not blocks:
        blocks = [lines]
    for index, block in enumerate(blocks, 1):
        project_id, card = make_project_card(block, index)
        (projects_dir / f"{project_id}.md").write_text(card, encoding="utf-8")

    review = textwrap.dedent(
        f"""\
        # Resume Bank Initialization Review

        Source resume: `{resume}`

        Generated files:
        - `base-profile.md`
        - `projects/*.md`
        - `outputs/`
        - `applications/`

        Review before using for applications:
        - Confirm each card represents one real project or experience.
        - Fill role, period, domain_tags, skill_tags, and preferred_for.
        - Replace `[量化指标待补]` with verified metrics only.
        - Move unsupported claims into `Do Not Claim`.
        - Change `status` from `needs_review` to `verified` only after fact-checking.
        - Create one `applications/<date-company-role>/` package for each JD-specific resume.
        """
    )
    (output / "INIT_REVIEW.md").write_text(review, encoding="utf-8")
    print(f"Initialized resume bank at {output}")
    print(f"Generated {len(blocks)} project card(s). Review INIT_REVIEW.md before use.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a resume-bank from an existing resume.")
    parser.add_argument("--resume", required=True, type=Path, help="Path to .md, .txt, .html, .docx, or .pdf resume")
    parser.add_argument("--output", default=Path("resume-bank"), type=Path, help="Output resume-bank directory")
    parser.add_argument("--force", action="store_true", help="Allow writing into an existing non-empty output directory")
    args = parser.parse_args()

    write_bank(args.resume.expanduser().resolve(), args.output.expanduser().resolve(), args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
