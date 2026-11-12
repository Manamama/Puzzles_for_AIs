"""Annotation forensics for one PDF: where are the reader's comments?

Usage: annot_forensics.py <pdf>

Prints: page count, catalog keys, /PieceInfo content, and every annotation
(subtype, author, date, rect, contents). Companion to the pdf-reading skill.
Stdlib + pypdf only.
"""
import sys

from pypdf import PdfReader
from pypdf.generic import DictionaryObject

path = sys.argv[1]
r = PdfReader(path, strict=False)

print(f"file   : {path}")
print(f"pages  : {len(r.pages)}")
info = dict(r.metadata or {})
print(f"meta   : Producer={info.get('/Producer')!r} Creator={info.get('/Creator')!r} "
      f"ModDate={info.get('/ModDate')!r}")

root = r.trailer["/Root"]
print(f"catalog: {sorted(root.keys())}")

piece = root.get("/PieceInfo")
if piece:
    piece = piece.get_object()
    print("\n=== /PieceInfo (application-private data) ===")
    for name, val in piece.items():
        val = val.get_object() if hasattr(val, "get_object") else val
        print(f"  [{name}] -> {sorted(val.keys()) if isinstance(val, dict) else type(val)}")
        if isinstance(val, dict):
            for k, v in val.items():
                v = v.get_object() if hasattr(v, "get_object") else v
                print(f"      {k} = {str(v)[:400]}")
else:
    print("\n=== /PieceInfo: absent ===")

totals = {}
found = 0
for i, page in enumerate(r.pages, 1):
    annots = page.get("/Annots")
    if not annots:
        continue
    for a in annots.get_object():
        a = a.get_object()
        sub = str(a.get("/Subtype"))
        totals[sub] = totals.get(sub, 0) + 1
        found += 1
        print(f"\n--- page {i}  subtype={sub}")
        for k in ("/T", "/M", "/NM", "/Rect", "/Contents", "/Subject", "/Popup",
                  "/IRT", "/FS", "/DA", "/Q", "/F"):
            if k in a:
                v = a[k]
                if isinstance(a[k], DictionaryObject):
                    v = a[k].get_object()
                print(f"    {k} = {str(v)[:500]}")

print(f"\n=== totals: {totals if totals else 'NO ANNOTATIONS AT ALL'} (found={found})")
