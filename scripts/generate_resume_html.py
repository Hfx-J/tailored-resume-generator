#!/usr/bin/env python3
"""Convert a simple Markdown resume into self-contained HTML."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


def inline_format(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    return escaped


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            output.append("</ul>")
            in_list = False

    for raw_line in lines:
        line = raw_line.rstrip()
        if not line.strip():
            close_list()
            continue
        if line.startswith("# "):
            close_list()
            output.append(f"<h1>{inline_format(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            close_list()
            output.append(f"<h2>{inline_format(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            close_list()
            output.append(f"<h3>{inline_format(line[4:].strip())}</h3>")
        elif re.match(r"^\s*[-*]\s+", line):
            if not in_list:
                output.append("<ul>")
                in_list = True
            item = re.sub(r"^\s*[-*]\s+", "", line)
            output.append(f"  <li>{inline_format(item)}</li>")
        else:
            close_list()
            output.append(f"<p>{inline_format(line.strip())}</p>")
    close_list()
    return "\n".join(output)


def render(markdown_path: Path, template_path: Path, output_path: Path, title: str | None) -> None:
    markdown = markdown_path.read_text(encoding="utf-8")
    template = template_path.read_text(encoding="utf-8")
    inferred_title = title or next((line[2:].strip() for line in markdown.splitlines() if line.startswith("# ")), "Resume")
    content = markdown_to_html(markdown)
    html_text = template.replace("{{TITLE}}", html.escape(inferred_title)).replace("{{CONTENT}}", content)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_text, encoding="utf-8")
    print(f"Wrote {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate HTML from a Markdown resume.")
    parser.add_argument("--markdown", required=True, type=Path, help="Input Markdown resume")
    parser.add_argument("--template", required=True, type=Path, help="HTML template with {{TITLE}} and {{CONTENT}}")
    parser.add_argument("--output", required=True, type=Path, help="Output HTML file")
    parser.add_argument("--title", help="Optional HTML title")
    args = parser.parse_args()
    render(args.markdown, args.template, args.output, args.title)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
