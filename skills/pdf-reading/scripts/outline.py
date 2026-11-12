"""Extract a PDF's outline (bookmarks) into markdown + JSON.

Usage: outline.py <pdf> <out.md> <out.json>

Companion to the pdf-reading skill. Stdlib + pypdf only.
"""
import json
import sys

from pypdf import PdfReader

pdf_path, out_md, out_json = sys.argv[1:4]
reader = PdfReader(pdf_path, strict=False)

items = []  # (depth, title, page_1based)


def walk(node, depth):
    for item in node:
        if isinstance(item, list):
            walk(item, depth + 1)
            continue
        title = getattr(item, "title", None)
        if title is None:
            continue
        title = " ".join(str(title).split())
        try:
            page = reader.get_destination_page_number(item) + 1
        except Exception:
            page = None
        items.append((depth, title, page))


try:
    walk(reader.outline, 0)
except Exception as exc:  # pragma: no cover
    print(f"outline failed: {exc}", file=sys.stderr)

lines = ["# Outline (PDF bookmarks)", ""]
for depth, title, page in items:
    indent = "  " * depth
    where = f"p.{page}" if page else "?"
    lines.append(f"{indent}- **{title}** — {where}")
lines.append("")

with open(out_md, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines))

with open(out_json, "w", encoding="utf-8") as fh:
    json.dump([{"depth": d, "title": t, "page": p} for d, t, p in items], fh, indent=1)

print(f"pages={len(reader.pages)} outline_items={len(items)}")
