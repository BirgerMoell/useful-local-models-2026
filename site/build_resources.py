from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "resources"

DOCS = {
    "student-project-brief": ROOT / "student-project-brief.md",
    "examples": ROOT / "examples" / "README.md",
    "course-code": ROOT / "course-code" / "README.md",
    "local-deployment-guide": ROOT / "local-deployment-guide.md",
    "project-tracks": ROOT / "project-tracks.md",
    "teacher-overview": ROOT / "teacher-overview.md",
    "teacher-start-checklist": ROOT / "teacher-start-checklist.md",
    "milestones-and-schedule": ROOT / "milestones-and-schedule.md",
    "rubric": ROOT / "rubric.md",
    "project-format": ROOT / "project-format.md",
    "modern-tooling-map": ROOT / "modern-tooling-map.md",
    "project-ideas": ROOT / "project-ideas.md",
    "project-intake-form": ROOT / "templates" / "project-intake-form.md",
    "training-pipeline-spec": ROOT / "training-pipeline-spec.md",
    "advanced-techniques-guide": ROOT / "advanced-techniques-guide.md",
    "worked-systems": ROOT / "nanochat-autoresearch-integration.md",
    "studium-theme-description": ROOT / "assignment-pages" / "studium-theme-description.md",
    "studium-proposal-assignment": ROOT / "assignment-pages" / "studium-proposal-assignment.md",
    "studium-progress-seminars": ROOT / "assignment-pages" / "studium-progress-seminars.md",
    "studium-final-report": ROOT / "assignment-pages" / "studium-final-report.md",
}


def slugify(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    def link(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.escape(match.group(2), quote=True)
        return f'<a href="{href}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    return text


def render_markdown(markdown: str) -> tuple[str, str]:
    lines = markdown.splitlines()
    out: list[str] = []
    title = "Course Resource"
    in_code = False
    in_list = False
    in_table = False
    table_rows: list[list[str]] = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not in_table:
            return
        out.append("<table>")
        for i, row in enumerate(table_rows):
            if i == 1 and all(re.fullmatch(r"\s*:?-{3,}:?\s*", cell) for cell in row):
                continue
            tag = "th" if i == 0 else "td"
            cells = "".join(f"<{tag}>{inline(cell.strip())}</{tag}>" for cell in row)
            out.append(f"<tr>{cells}</tr>")
        out.append("</table>")
        in_table = False
        table_rows = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_table()
            close_list()
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            continue

        if in_code:
            out.append(html.escape(line))
            continue

        if not stripped:
            flush_table()
            close_list()
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            close_list()
            in_table = True
            table_rows.append([cell for cell in stripped.strip("|").split("|")])
            continue
        flush_table()

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            close_list()
            level = len(heading.group(1))
            text = heading.group(2)
            if level == 1:
                title = re.sub(r"`", "", text)
            out.append(f'<h{level} id="{slugify(text)}">{inline(text)}</h{level}>')
            continue

        if stripped.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(stripped[2:])}</li>")
            continue

        close_list()
        out.append(f"<p>{inline(stripped)}</p>")

    flush_table()
    close_list()
    if in_code:
        out.append("</code></pre>")
    return title, "\n".join(out)


def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)} - Useful Local Models</title>
    <link rel="stylesheet" href="resource.css">
  </head>
  <body>
    <header>
      <a href="../index.html">Useful Local Models</a>
    </header>
    <main>
      {body}
    </main>
  </body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, source in DOCS.items():
        title, body = render_markdown(source.read_text(encoding="utf-8"))
        (OUT / f"{name}.html").write_text(page(title, body), encoding="utf-8")
    print(f"Wrote {len(DOCS)} resource pages to {OUT}")


if __name__ == "__main__":
    main()
