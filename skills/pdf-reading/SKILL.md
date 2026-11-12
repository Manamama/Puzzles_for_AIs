---
name: pdf-reading
description: >
  How an agent should read PDFs in OpenCode: built-in read() passes a PDF as
  media (max 20 MiB, needs a PDF-input model) and never returns text, so
  content questions are answered by converting once to page-anchored markdown
  (.md + .index.md + .outline.md) and consuming it with grep + read(offset).
  Includes the two-script pipeline and the object-graph route for annotation
  forensics ("where did my comments go?"). Use whenever a task involves
  reading, searching, or questioning the content or structure of a PDF.
---

# Reading PDFs the OpenCode-friendly way

Written 2026-10-30 after converting the 181-page BOOX NoteAir manual on
Termux/Android (aarch64). Proven end-to-end there; numbers below are measured,
not estimated.

## Rule zero

Never answer a **content** question by reading raw PDF bytes. Byte offsets
locate objects; they cannot tell you what a page says. Convert first, search
second. (Motivating diagnosis: three wasted rounds of grep-on-bytes before the
obvious convert → grep → read path was taken.)

## The three instruments — pick by question type

| Question type | Instrument | Why |
|---|---|---|
| "What does it *say* about X?" | text: convert → `grep` → `read(offset)` | content lives in text |
| "Where is my data *stored*?" (annotations, attachments, form fields) | object graph via `pypdf`: `/Annots`, `/FreeText`, `/Popup`, `/Ink`, `/Highlight`, `/PieceInfo`, `/Outlines` | invisible content is still objects |
| "What does page N *look* like?" | built-in `read` as media | only route that sees layout |

Conflating rows 1 and 2 wastes the most time: text extraction can never
reveal where invisible data is stored, and object spelunking can never tell
you what the prose says.

## Built-in read() on a PDF — the hard limits

- Passes the file through as **document media**, not extracted text.
- **20 MiB source cap.** Over it: `Media exceeds 20971520 byte ingestion
  limit`. A 21,666,622-byte file fails on size alone; that is the whole story.
- **Needs a PDF-input-capable model**, else OpenCode substitutes a one-line
  apology note instead of the document.
- Even when it works, page imagery costs far more tokens than converted text
  (70 KB of text vs 21 MB of media for the same manual).
- Text-mode `read`: 2,000 lines and 50 KiB per page; lines truncated after
  2,000 characters.

## The pipeline (convert once, cache forever)

Write artifacts next to the PDF if that directory is writable, else into a
cache dir. The scripts ship with this skill in `scripts/`.

```sh
# 0. cache check — if the .md is newer than the .pdf, stop here.

# 1. map: PDF outline -> chapter->page table  (~2 s, ~1 KB output)
python3 scripts/outline.py BOOK.pdf BOOK.outline.md outline.json

# 2. raw text (poppler is ~60x faster than pdfminer on big files)
pkg install -y poppler                     # once; provides pdftotext
pdftotext -layout BOOK.pdf raw.txt         # 1.4 s for 181 pages / 21 MB
# fallback without poppler:  pdf2txt.py -o raw.txt BOOK.pdf   (pdfminer, slow)

# 3. build artifacts  (~1 s)
python3 scripts/build_md.py raw.txt BOOK.md BOOK.index.md outline.json BOOK.pdf
```

Read the `.outline.md` **before** deciding what to extract: the PDF's own
bookmark tree usually answers "where is X documented" without any body text
(the manual's own Contents page and the outline agreed with each other).

## The output contract (what makes it AI-friendly)

1. `## p.N` before every page — N is the PDF's own page number, 1:1, so any
   grep hit yields a page you can jump to in a viewer or `-f/-l` flag.
2. `### headings` — from the PDF outline titles + numeric patterns
   (`^\d+(\.\d+)*[.)]?\s+`); 132 detected in the 181-page manual,
   zero false positives.
3. Paragraphs reflowed: joined across `-layout`'s blank gaps, de-hyphenated
   at line ends; a blank line only ends a paragraph at a sentence boundary.
4. **No baked-in line numbers.** `read()` numbers lines itself and `grep`
   returns them; duplicating them pollutes every preview and breaks
   copy-paste. (The user's "cat -n like" instinct is already satisfied by
   `read`.)
5. `BOOK.index.md`: table `Section | PDF page | Line`, where Line is directly
   usable as `read(path, offset=Line-1, limit=N)`.
6. `BOOK.outline.md`: the PDF's bookmark tree with page numbers — the ~1 KB
   map that beats re-reading 70 KB of body.

## Consumption recipes

| Need | Calls |
|---|---|
| "what does it say about embedding?" | `grep embed` → `read(offset=hit, limit≈40)` |
| chapter structure | `read BOOK.outline.md` (~1 KB) |
| jump to section S | index row → `read(offset=Line-1)` |
| everything about topic T | `grep -i T` → every hit shows its `## p.N` context |

## When NOT to use this

- Small PDF (<20 MiB), PDF-input model available, and the question is about
  layout/appearance → `read` it directly.
- Scanned/image-only PDF: both pdftotext and pdfminer return ~nothing; OCR
  first (tesseract), then re-enter at step 3 of the pipeline.

## Annotation forensics (verified 2026-10-30 on two same-day cases)

Symptom: "I made text comments in a reader; other PDF readers show none."

**Enumerate annotations with pypdf — never grep raw bytes for type names.**
A probe list that omits the subtype the writer actually used produces a
confident, wrong "no annotations" verdict (that mistake cost a session here).

- Markup annotations carry the typed text in their own `/Contents`:
  `/Squiggly`, `/Underline`, `/Highlight`, `/StrikeOut`, `/FreeText`,
  `/Text`+`/Popup`, `/Ink`, `/Stamp`, `/Square` under a page's `/Annots`.
- Verified ONYX/NeoReader behavior — same device, same day, two files:
  - `Noc Innowacji.pdf`: 53 markup annotations (`/Squiggly` 43, `/Underline` 7,
    `/Stamp` 3), author `/T`=`NoteAir`, comment text in `/Contents` —
    standard PDF, fully recoverable.
  - the 181-page BOOX manual: **zero** user annotations in-file (only the
    publisher's 17 `/Link`), yet comments had been made there → they live in
    ONYX's private store, keyed by the `/PieceInfo[/onyxtag]/Private`
    document id (`{"id", "commitId", "exported": false}`).
  So the same app writes markup-attached comments into the PDF but note-style
  comments may stay app-local. Don't generalize from one file — probe both.
- Why they look invisible elsewhere: squiggly/underline markup is the
  least-supported annotation class — many viewers render nothing for it and
  never surface `/Contents` without a comments pane; ONYX writes no `/Popup`
  and most annots lack `/M` dates.
- Extraction recipe (`scripts/annot_extract.py`): pypdf gives `/Rect` +
  `/Contents`; pdfminer gives char bboxes; intersecting them reconstructs
  exactly the marked span → quote → comment pairs, sorted per page.
- App-side sidecars to check when in-file is empty: `/sdcard/note`,
  `.noteCache/`, `.noteResource/`, reader app databases. Manual p.50-51:
  re-edited files "are identified as different files and will not import the
  embedded data" — doc identity is path+id based.
- GUI recovery alternatives: NeoReader TOC → Annotation → export .txt;
  Scribble Toolbar → Save as PDF.

## Pitfalls (all measured here)

- `/Size N` in the trailer is the **object count**, not the page count.
  849 objects ≠ 849 pages (the manual: 181 pages).
- `pdfminer`/`pdf2txt.py` is ~60× slower than poppler and shreds two-column
  regions into one word per line.
- `pdftotext -layout` inserts a blank line between every text line; reflow
  must look ahead across blanks (`build_md.py:reflow`), or every wrapped line
  becomes its own paragraph and line counts balloon (3,156 → 2,220 after the
  fix, with identical byte count).
- Heading detection from outline titles + numeric patterns only — conservative
  and false-positive-free. Do not get cleverer; prose masquerading as headings
  is worse than a few unmarked headings.

## Scripts

`outline.py` / `build_md.py` need `pypdf` (`pip install pypdf`) and, for
extraction, `pdftotext` from the `poppler` package. The forensic pair needs
`pypdf` plus `pdfminer.six` for `annot_extract.py`.

```sh
python3 scripts/outline.py BOOK.pdf BOOK.outline.md outline.json
python3 scripts/build_md.py raw.txt BOOK.md BOOK.index.md outline.json BOOK.pdf
python3 scripts/annot_forensics.py BOOK.pdf              # where are annotations?
python3 scripts/annot_extract.py BOOK.pdf OUT.md LABEL   # quote+comment pairs
```

`build_md.py` expects `raw.txt` to separate pages with form-feed (`\f`) — the
default for both `pdftotext` and `pdf2txt.py`.
