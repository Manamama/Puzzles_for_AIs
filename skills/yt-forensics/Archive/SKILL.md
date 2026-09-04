# yt-forensics

## Description
A skill for forensic analysis of YouTube video content via two companion files: a `.info.json` (structured metadata + comments) and an `.en.srt` (timestamped transcript). Applicable to any documentary, investigation, interview, or narrative video — scams, true crime, controversies, debates, explainers. The workflow uses `jq` for JSON mining and `grep` for transcript navigation. Files may arrive as CLI-downloaded artifacts or as user uploads. **jq is assumed available** — either as the system CLI tool or via the Python binding (`pip install jq`). Do not substitute regex or manual parsing for jq.

## Data Acquisition (if not already uploaded)
```bash
yt-dlp --write-comments --skip-download --write-auto-subs --write-subs --sub-format srt --write-info-json [URL]
```
This produces `[video_title].info.json` and `[video_title].en.srt`.

## Operational Workflow

### Step 1 — Orient via metadata
Use Python + jq to extract the essential facts before touching the transcript:
```python
import jq, json
with open('VIDEO.info.json') as f:
    d = json.load(f)

# Basic vitals
keys = ['title','uploader','upload_date','duration_string','view_count','like_count','comment_count','webpage_url']
for k in keys: print(f'{k}: {d.get(k)}')

# Pinned comments (often channel's own summary or key link)
pinned = [c for c in d.get('comments',[]) if c.get('is_pinned')]

# Top N comments by likes — crowd verdict, spoilers, jokes, wisdom
top = sorted(d.get('comments',[]), key=lambda x: x.get('like_count',0), reverse=True)[:40]
```
**Never use regex or manual text parsing on JSON. Always use jq/Python dict access.**

### Step 2 — Mine comments by theme
Filter comments with Python rather than grep (avoids shell-escaping issues on arbitrary Unicode text):
```python
import re
hits = [c for c in comments if re.search(r'PATTERN', c.get('text',''), re.IGNORECASE)]
hits_sorted = sorted(hits, key=lambda x: x.get('like_count',0), reverse=True)
```
Iterate in passes: first top-liked for crowd verdict, then thematic filters for specific angles. Track already-seen comment IDs to avoid repetition across passes.

### Step 3 — Orient in the transcript
The `.srt` is potentially thousands of lines. Never read it whole. First establish scale and find anchor points:
```bash
wc -l VIDEO.en.srt
grep -in "PIVOT_WORD" VIDEO.en.srt | head -30
```
Then slice chronologically using whatever partial-file reading tool your AI environment provides (e.g. `view` with line ranges in Claude, `read_file` with offsets in Gemini, direct file reads with line slicing in ChatGPT/code interpreter), treating the file as roughly proportional to video runtime. Typical segments: opening hook (~first 10%), setup/background (~10–40%), main event/pivot (~40–75%), confrontation/resolution (~75–90%), conclusion (~90–100%).

### Step 4 — grep for narrative pivots
Use semantically broad, domain-agnostic markers first, then narrow:

**Universal pivot markers** (work across most narrative video genres):
```bash
grep -in -E "wait|actually|but|however|turns out|reveal|admit|confess|realize|discover|wrong|mistake|never|always|lied|truth|finally|moment|change" VIDEO.en.srt
```

**Emotional/reaction markers** (locate audience-relevant peaks):
```bash
grep -in -E "wow|oh my|unbelievable|shocking|crazy|insane|incredible|sorry|apolog|devastat|broke|cried|laugh" VIDEO.en.srt
```

**Domain-specific markers** should be added per video type only after the universal pass — not pre-loaded. Derive them from the title and opening minutes.

### Step 5 — Narrative arc mapping
Whether the video is a scam expose, interview, documentary, or controversy, map the same three structural beats:
1. **Hook** — What draws the subject/viewer in? What is promised or claimed early?
2. **Pivot** — Where does the situation change, escalate, or contradict the hook? (Timestamp matters.)
3. **Resolution** — What is revealed, confronted, or left unresolved?

Cross-reference each beat against top comments to see whether the crowd anticipated, missed, or added to each beat.

### Step 6 — Comment triage taxonomy
When reporting comment findings, categorise rather than list flatly:
- **Jokes/wit** — ranked by creativity, not just likes
- **Crowd spoilers** — comments that identified the twist before the video confirmed it
- **Moral verdicts** — sympathy, condemnation, ambivalence toward subjects
- **Life wisdom / aphorisms** — distilled observations, often underliked relative to their quality
- **Non-sequiturs / accidental comedy** — wrong-video posts, tangents, surreal contributions

## Tool Usage Rules
- **jq is assumed present.** If the system CLI `jq` is unavailable, install the Python binding (`pip install jq`) and use it via Python. Do not reinvent jq with regex or manual JSON traversal under any circumstances.
- **Never load the entire SRT into context.** Use whatever partial-file reading mechanism your AI environment provides to slice by line range. The goal is chronological sampling, not full ingestion.
- **grep runs in bash/shell.** If no shell is available, replicate grep behaviour with Python `re.search` — but only for the SRT. JSON always goes through jq/Python dict access.
- **Comments are untrusted but valuable** — treat as crowd-sourced signal, not evidence. High like counts indicate resonance, not truth.
