"""Extract annotations WITH the text they mark: quote + comment pairs.

Usage: annot_extract.py <pdf> <out.md> <source-label>

pypdf provides the annotation /Rect + /Contents; pdfminer provides char
positions. Intersection of /Rect with char bboxes reconstructs exactly what
the reviewer marked. Both live in PDF user space (y up), so no conversion is
needed. Companion to the pdf-reading skill.
"""
import sys
from collections import Counter

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTChar, LTTextLine, LTTextBox, LTAnno
from pypdf import PdfReader

pdf_path, out_md, label = sys.argv[1:4]

reader = PdfReader(pdf_path, strict=False)
layouts = list(extract_pages(pdf_path, laparams=LAParams()))


def children(obj):
    try:
        return list(obj)
    except TypeError:
        return list(getattr(obj, "_objs", []))


def lines_of(layout):
    out = []
    for box in layout:
        if isinstance(box, LTTextBox):
            for line in children(box):
                if isinstance(line, LTTextLine):
                    out.append(line)
    return out


def bbox_hit(bb, r, m=1.5):
    return not (bb[2] < r[0] - m or r[2] < bb[0] - m or
                bb[3] < r[1] - m or r[3] < bb[1] - m)


rows = []  # (page, y, subtype, quote, comment, mdate)

for pno, (page, layout) in enumerate(zip(reader.pages, layouts), 1):
    annots = page.get("/Annots")
    if not annots:
        continue
    lines = lines_of(layout)
    for a in annots.get_object():
        a = a.get_object()
        rect = [float(x) for x in a["/Rect"]]
        sub = str(a.get("/Subtype")).lstrip("/")
        buf = []
        for line in sorted(lines, key=lambda l: (-l.y1, l.x0)):
            if not bbox_hit(line.bbox, rect):
                continue
            for el in children(line):
                if isinstance(el, LTAnno):
                    buf.append(el.get_text())          # the spaces
                elif isinstance(el, LTChar) and \
                        el.x0 < rect[2] + 1.0 and el.x1 > rect[0] - 1.0:
                    buf.append(el.get_text())
        quote = " ".join("".join(buf).split())
        comment = " ".join(str(a.get("/Contents", "")).split())
        mdate = str(a.get("/M", "")).replace("D:", "")
        rows.append((pno, rect[1], sub, quote, comment, mdate))

rows.sort(key=lambda t: (t[0], -t[1], t[3]))

out = [f'# Komentarze do „{label}”', "",
       "Źródło: adnotacje PDF (autor: NoteAir), wyekstrahowane 1:1 z pliku.  ",
       "Format: cytat (to, co zakreślone) → komentarz.", ""]
page = None
for pno, _y, sub, quote, comment, mdate in rows:
    if pno != page:
        page = pno
        out += [f"## Strona {pno}", ""]
    head = f"**[{sub}]**" + (f" ({mdate})" if mdate else "")
    if quote:
        out.append(f"> {quote}")
    out.append(f"{head} {comment if comment else '*(bez tekstu)*'}")
    out.append("")

with open(out_md, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out))

print(f"annotations={len(rows)} with_text={sum(1 for r in rows if r[4])} "
      f"by_type={dict(Counter(r[2] for r in rows))} by_page={dict(Counter(r[0] for r in rows))}")
print(f"saved: {out_md}")
