#!/usr/bin/env python3
"""Create a per-JD application package inside a resume-bank."""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path


def slugify(value: str, fallback: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value[:80] or fallback


def read_jd(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore").strip() + "\n"


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def copy_jd_if_missing(source: Path, destination: Path) -> bool:
    if destination.exists():
        return False
    text = read_jd(source)
    destination.write_text(text, encoding="utf-8")
    return True


def create_package(
    bank: Path,
    company: str,
    role: str,
    jd_file: Path,
    date_value: str | None,
    slug: str | None,
    force: bool,
) -> Path:
    if not jd_file.exists():
        raise SystemExit(f"JD file not found: {jd_file}")

    package_date = date_value or date.today().strftime("%Y%m%d")
    if not re.fullmatch(r"\d{8}", package_date):
        raise SystemExit("--date must use YYYYMMDD format")

    applications_dir = bank / "applications"
    applications_dir.mkdir(parents=True, exist_ok=True)

    package_slug = slugify(slug or f"{package_date}-{company}-{role}", "application")
    package_dir = applications_dir / package_slug

    if package_dir.exists() and any(package_dir.iterdir()) and not force:
        raise SystemExit(f"{package_dir} already exists. Use --force to fill missing files without overwriting.")
    package_dir.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    if copy_jd_if_missing(jd_file, package_dir / "jd.md"):
        created.append("jd.md")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    metadata = f"""# Application Metadata

- Company: {company}
- Role: {role}
- Package Date: {package_date}
- Package Slug: {package_slug}
- JD Source: {jd_file}
- Status: draft
- Created At: {timestamp}

"""
    if write_if_missing(package_dir / "metadata.md", metadata):
        created.append("metadata.md")

    jd_analysis = """# JD Analysis

## Role Target

## Priority 1 Requirements

## Priority 2 Requirements

## Bonus Requirements

## Keywords

## Gaps / Risks

"""
    if write_if_missing(package_dir / "jd-analysis.md", jd_analysis):
        created.append("jd-analysis.md")

    selected_projects = """# Selected Projects

## Recommended Cards

| Score | Project ID | Matched Requirements | Evidence | Risks |
| --- | --- | --- | --- | --- |

## Selected For Resume

## Not Used

"""
    if write_if_missing(package_dir / "selected-projects.md", selected_projects):
        created.append("selected-projects.md")

    changelog = f"""# Change Log

## {timestamp} - package created

- Trigger: application package initialization
- Inputs: `{jd_file}`
- Outputs: package skeleton
- Changes:
  - Created JD-specific workspace for {company} / {role}.
- Open facts:
  - JD analysis and selected projects pending.

"""
    if write_if_missing(package_dir / "CHANGELOG.md", changelog):
        created.append("CHANGELOG.md")

    notes = """# Notes

## Open Questions

## User Feedback

## Interview Talking Points

## Cover Letter Hooks

"""
    if write_if_missing(package_dir / "notes.md", notes):
        created.append("notes.md")

    print(f"Application package: {package_dir}")
    if created:
        print("Created: " + ", ".join(created))
    else:
        print("No files created; package already had all standard files.")
    return package_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a JD-specific application package under resume-bank/applications.")
    parser.add_argument("--bank", default=Path("resume-bank"), type=Path, help="Path to resume-bank")
    parser.add_argument("--company", required=True, help="Target company name")
    parser.add_argument("--role", required=True, help="Target role title")
    parser.add_argument("--jd-file", required=True, type=Path, help="Path to JD text/Markdown file")
    parser.add_argument("--date", help="Package date in YYYYMMDD format; defaults to today")
    parser.add_argument("--slug", help="Custom package folder name")
    parser.add_argument("--force", action="store_true", help="Fill missing files in an existing package without overwriting")
    args = parser.parse_args()

    create_package(
        bank=args.bank.expanduser().resolve(),
        company=args.company,
        role=args.role,
        jd_file=args.jd_file.expanduser().resolve(),
        date_value=args.date,
        slug=args.slug,
        force=args.force,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
