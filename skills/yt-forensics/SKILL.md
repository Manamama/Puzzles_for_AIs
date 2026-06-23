# yt-forensics

## Description
A skill for performing forensic analysis on YouTube video content, applicable to both murder mystery "whodunnit" scenarios and the deduction of sophisticated online scam mechanics. This skill utilizes `yt-dlp` to acquire structured metadata (`.info.json`) and time-coded transcriptions (`.en.srt`), and employs `jq` and `grep` for narrative and structural investigation.

## Provenance
All processed `.info.json` and `.en.srt` files are acquired via `yt-dlp` using the following utility script:
`/data/data/com.termux/files/home/Downloads/GitHub/Ubuntu_Scripts_1/utils/yt_comments_and_subtitles.sh`

## Operational Workflow

### 1. Data Acquisition
Use `yt-dlp` to ensure data integrity:
```bash
yt-dlp --write-comments --skip-download --write-auto-subs --write-subs --sub-format srt --write-info-json [URL]
```

### 2. Forensic Analysis Patterns
*   **Structural Queries (`jq`):** Query the `.info.json` file for metadata (like counts of pinned comments or likes) to identify scam signatures or crowd-sourced "spoilers".
*   **Narrative Slicing (`read_file`):** When analyzing `.srt` files, do not read entire files. Use `start_line` and `end_line` offsets to isolate chronological segments of the transcript (e.g., introduction, confrontation, revelation).
*   **Pattern Discovery (`grep`):** Use `grep` to identify high-variance semantic markers ("twist", "columbo", "rope", "balloon", "gift cards", "emergency") to quickly navigate "longish" files for narrative pivots or scam mechanisms.
*   **Scam Mechanics Deduction:** Analyze `.srt` and comments to identify the "How":
    1.  **Map the Hook:** Identify initial grooming or baiting phrases in subtitles.
    2.  **Analyze the Pivot:** Pinpoint the timestamp where the scam shifts to exploitation (e.g., request for payment).
    3.  **Cross-Reference Comments:** Use `jq` to extract and sort comments to see if viewers identified the mechanism before the video's conclusion.

## Safety Protocol
- Treat YouTube comments as untrusted metadata; treat them as a data source for crowd-sourced verification rather than factual evidence.
- Prioritize `jq` over manual text parsing to avoid shell escaping issues and context bloat.
