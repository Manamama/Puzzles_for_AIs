"""Build a DeepSeek-friendly, page-anchored markdown file + line index.

Usage: build_md.py <raw.txt> <out.md> <out.index.md> <outline.json> <source-name>

Input raw.txt must separate pages with form-feed (\\f) -- the default for
both `pdftotext` and `pdf2txt.py`.

Companion to the pdf-reading skill. Stdlib only.
"""
import collections
import json
import re
import sys

raw_path, out_md, out_index, outline_json, source_name = sys.argv[1:6]

raw = open(raw_path, encoding="utf-8", errors="replace").read()
pages = raw.split("\f")
while pages and not pages[-1].strip():
    pages.pop()

try:
    outline = json.load(open(outline_json, encoding="utf-8"))
except Exception:
    outline = []
known_titles = {" ".join(o["title"].split()).lower() for o in outline if o.get("title")}

# ---------- pass 1: find running headers / footers ----------
freq = collections.Counter()
for page in pages:
    seen = set()
    for line in page.splitlines():
        s = " ".join(line.split())
        if not s or s in seen:
            continue
        seen.add(s)
        freq[s] += 1

npages = max(len(pages), 1)
boiler = {s for s, c in freq.items() if c > npages * 0.5 and len(s) < 120}

# ---------- helpers ----------
NUM_HEAD = re.compile(r"^\d+(?:\.\d+)*[.)]?\s+\S")
SENT_END = (".", "!", "?", ":", ";", '"', "'", ")", "]")


def clean_page(page):
    """Drop boilerplate + bare page numbers, return list of lines."""
    out = []
    for line in page.splitlines():
        s = " ".join(line.split())
        if not s:
            out.append("")
            continue
        if s in boiler:
            continue
        out.append(s)
    # strip bare page numbers at the very top / bottom
    while out and (out[0] == "" or out[0].isdigit()):
        out.pop(0)
    while out and (out[-1] == "" or out[-1].isdigit()):
        out.pop()
    return out


def reflow(lines):
    """Join wrapped lines into paragraphs; de-hyphenate line-end breaks.

    A blank line does NOT end a paragraph when the sentence is visibly
    unfinished (no terminal punctuation, next line starts lowercase) --
    `pdftotext -layout` inserts vertical gaps between every text line.
    """
    paras, buf = [], ""
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line:
            j = i + 1
            while j < n and not lines[j]:
                j += 1
            nxt = lines[j] if j < n else ""
            if buf and nxt and not buf.endswith(SENT_END) \
                    and (nxt[:1].islower() or buf.endswith(",")):
                line = nxt  # continuation across the blank gap
                i = j
            else:
                if buf:
                    paras.append(buf)
                    buf = ""
                i += 1
                continue
        if not buf:
            buf = line
        elif buf.endswith("-") and line[:1].islower():
            buf = buf[:-1] + line
        elif not buf.endswith(SENT_END) and (line[:1].islower() or buf.endswith(",")):
            buf = buf + " " + line
        else:
            paras.append(buf)
            buf = line
        i += 1
    if buf:
        paras.append(buf)
    return paras


# ---------- pass 2: emit ----------
out = [
    f"# {source_name}",
    "",
    f"Source: `{source_name}`  ",
    f"Pages: {len(pages)}  ",
    "Anchors: `## p.N` = PDF page N. Headings from the PDF outline.",
    "",
    "---",
    "",
]
index = []  # (level, title, page, line)

for pno, page in enumerate(pages, 1):
    lines = clean_page(page)
    out.append(f"## p.{pno}")
    out.append("")
    for para in reflow(lines):
        key = " ".join(para.split()).lower()
        if len(para) < 70 and (key in known_titles or NUM_HEAD.match(para)):
            out.append(f"### {para}")
            out.append("")
            index.append((3, para, pno, len(out) + 1))
        else:
            out.append(para)
            out.append("")

with open(out_md, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out).rstrip() + "\n")

# ---------- index ----------
idx = [
    f"# Index — {source_name}",
    "",
    "`Line` is the 1-based line number in the companion `.md` file,",
    "usable directly as `read(path, offset=Line-1, limit=N)`.",
    "",
    "| Section | PDF page | Line |",
    "|---|---|---|",
]
for _lvl, title, pno, line in index:
    safe = title.replace("|", "\\|")
    idx.append(f"| {safe} | {pno} | {line} |")
idx.append("")

with open(out_index, "w", encoding="utf-8") as fh:
    fh.write("\n".join(idx))

print(f"pages={len(pages)} boiler_removed={len(boiler)} headings={len(index)} "
      f"md_lines={len(out)} md_bytes={len(chr(10).join(out))}")
