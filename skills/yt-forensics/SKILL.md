---
name: yt-forensics
description: "Use this skill when the user wants to analyze a YouTube video forensically using a .info.json (metadata + comments) and/or .en.srt (transcript) produced by yt-dlp. Covers any narrative video genre: scams, true crime, interviews, controversies, documentaries. Triggers include: any mention of .info.json or .en.srt files, requests to analyze YouTube comments, mine crowd reactions, run sentiment analysis, cluster topics, find narrative pivots in a transcript, or extract the video URL from a yt-dlp JSON. The skill covers two tiers: (1) quick forensics via jq/Python, and (2) full statistical analysis via pandas/sklearn/matplotlib. Do NOT use for general YouTube searches, video downloading, or tasks where no .info.json/.en.srt files are present."
license: CC0 — public domain, free for use by any AI system or human operator.
---

# yt-forensics  v2.0.0

Forensic analysis of YouTube videos via yt-dlp companion files:
- `.info.json` — structured metadata + all comments
- `.en.srt` — timestamped transcript

Two analysis tiers are defined below. Start with **Tier 1** for quick orientation; escalate to **Tier 2** for full statistical analysis when the user wants charts, clustering, or deeper insight.

---

## Data Acquisition

```bash
yt-dlp --write-comments --skip-download \
       --write-auto-subs --write-subs --sub-format srt \
       --write-info-json [URL]
```
Produces `[video_title].info.json` and `[video_title].en.srt`.

**To extract the video URL from an existing .info.json:**
```bash
jq -r '.webpage_url' filename.info.json
```

---

## Known yt-dlp data quirks (important — read before any analysis)

- **Timestamps are rounded to day boundaries.** All comments on a given day share the same Unix timestamp (midnight UTC). There are typically only 10–25 unique day values for thousands of comments. Hour-of-day analysis is impossible. Week/month trends are coarse approximations only — label them as such in any output.
- **`reply_count` field is always `None`.** Infer reply counts by counting how many comments share the same `parent` ID.
- **Language detection is unreliable for short comments.** Apply `langdetect` only to comments with ≥ 8 words; label shorter comments as `'short'` rather than guessing. Even then, non-English counts are typically small and should be caveated.
- **Median likes is 0 for most subgroups** (typically 65–70% of root comments have 0 likes). Always use *mean* (not median) when comparing likes across groups, and filter to `like_count > 0` where appropriate. Report the zero-like percentage explicitly.
- **`reply_count` in the raw JSON is None** for all entries — always infer it (see Tier 1 Step 1).

---

## Tier 1 — Quick Forensics (jq + Python)

### Step 1 — Orient via metadata + infer reply counts

```python
import json
from collections import Counter

with open('VIDEO.info.json') as f:
    d = json.load(f)

# Vitals
keys = ['title','uploader','upload_date','duration_string',
        'view_count','like_count','comment_count','webpage_url']
for k in keys:
    print(f'{k}: {d.get(k)}')

comments = d.get('comments', [])

# Infer reply counts (reply_count field is always None in yt-dlp output)
reply_counts = Counter(c['parent'] for c in comments if c.get('parent') != 'root')

# Top comments by likes
top = sorted(comments, key=lambda x: x.get('like_count', 0), reverse=True)[:40]

# Most-replied-to root comments (controversy proxy)
roots = [c for c in comments if c.get('parent') == 'root']
for c in roots:
    c['_reply_count'] = reply_counts.get(c['id'], 0)
most_replied = sorted(roots, key=lambda x: x['_reply_count'], reverse=True)[:20]
```

**Controversy index** — high replies relative to likes signals debate rather than consensus:
```python
import math
for c in roots:
    c['_controversy'] = c['_reply_count'] / (math.log1p(c.get('like_count', 0)) + 1)
controversial = sorted(roots, key=lambda x: x['_controversy'], reverse=True)[:15]
```

### Step 2 — Mine comments by theme

```python
import re
def search_comments(comments, pattern):
    hits = [c for c in comments
            if re.search(pattern, c.get('text',''), re.IGNORECASE)]
    return sorted(hits, key=lambda x: x.get('like_count',0), reverse=True)
```

### Step 3 — Transcript orientation (SRT)

Never read the SRT whole. Establish scale, find anchors, slice:
```bash
wc -l VIDEO.en.srt
grep -in "PIVOT_WORD" VIDEO.en.srt | head -30
```
Treat file as proportional to runtime. Typical segments:
- Hook: first ~10%
- Setup: 10–40%
- Pivot: 40–75%
- Confrontation/resolution: 75–90%
- Conclusion: 90–100%

**Universal pivot markers:**
```bash
grep -in -E "wait|actually|but|however|turns out|reveal|admit|confess|realize|discover|wrong|lied|truth|finally|change" VIDEO.en.srt
```

**Emotional markers:**
```bash
grep -in -E "wow|oh my|unbelievable|shocking|crazy|sorry|apolog|devastat|broke|cried|laugh" VIDEO.en.srt
```

### Step 4 — Narrative arc mapping

Map three structural beats, then cross-reference against top comments:
1. **Hook** — what is promised or claimed early?
2. **Pivot** — where does the situation change or contradict the hook?
3. **Resolution** — what is revealed, confronted, or left open?

### Step 5 — Comment triage taxonomy

Categorise findings rather than listing flatly:
- **Jokes / wit** — ranked by creativity, not just likes
- **Crowd spoilers** — identified the twist before the video confirmed it
- **Moral verdicts** — sympathy, condemnation, ambivalence
- **Life wisdom / aphorisms** — often underliked relative to quality
- **Controversy threads** — high reply/like ratio; debate, not consensus
- **Non-sequiturs / accidental comedy** — tangents, wrong-video posts

---

## Tier 2 — Full Statistical Analysis (pandas + sklearn + matplotlib)

Use when the user wants charts, clustering, sentiment trends, or publishable analysis. Requires: `pandas`, `matplotlib`, `scikit-learn`, `vaderSentiment`, `textstat`, `langdetect` (all pip-installable).

```bash
pip install vaderSentiment textstat langdetect --break-system-packages -q
```

### Step A — Build the analysis dataframe

```python
import json, pandas as pd, numpy as np, re
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect, LangDetectException
import textstat

with open('VIDEO.info.json') as f:
    d = json.load(f)

comments = d.get('comments', [])
df = pd.DataFrame(comments)

# Infer reply counts
reply_counts = Counter(c['parent'] for c in comments if c.get('parent') != 'root')
df['reply_count'] = df['id'].map(reply_counts).fillna(0).astype(int)

# Day-bucket (coarse — see quirks above)
upload_dt = pd.to_datetime(d['upload_date'], format='%Y%m%d')
df['dt'] = pd.to_datetime(df['timestamp'], unit='s')
df['days_after_upload'] = (df['dt'] - upload_dt).dt.days
# NOTE: hour-of-day is always 0 — do not use for hourly analysis

# Sentiment (VADER: Valence Aware Dictionary for sEntiment Reasoning)
# Score range: -1 (most negative) to +1 (most positive)
sia = SentimentIntensityAnalyzer()
df['sentiment'] = df['text'].apply(lambda t: sia.polarity_scores(str(t))['compound'])
df['sentiment_label'] = pd.cut(df['sentiment'], bins=[-1,-0.05,0.05,1],
                               labels=['Negative','Neutral','Positive'])

# Text features
df['word_count'] = df['text'].apply(lambda t: len(str(t).split()))
df['char_count'] = df['text'].apply(lambda t: len(str(t)))
df['has_emoji']     = df['text'].apply(lambda t: any(ord(c)>127 for c in str(t)))
df['has_timestamp'] = df['text'].str.contains(r'\d+:\d+', regex=True)
df['is_question']   = df['text'].str.contains(r'\?')
df['is_favorited']  = df['is_favorited'].fillna(False)

# Readability
df['flesch'] = df['text'].apply(lambda t: textstat.flesch_reading_ease(str(t)))

# Language — only trust comments with >=8 words
def safe_detect(t):
    try: return detect(str(t))
    except: return 'unknown'
df['lang'] = df.apply(
    lambda r: safe_detect(r['text']) if r['word_count'] >= 8 else 'short', axis=1)

# Controversy index
roots_mask = df['parent'] == 'root'
df.loc[roots_mask, 'controversy'] = (
    df.loc[roots_mask, 'reply_count'] /
    (np.log1p(df.loc[roots_mask, 'like_count']) + 1)
)
```

### Step B — Key analyses to run

**1. Like distribution (use CCDF, not histogram — power law)**
```python
import matplotlib.pyplot as plt
liked = df[df['like_count']>0]['like_count']
xvals = np.logspace(0, np.log10(liked.max()), 200)
ccdf  = [(liked >= x).mean() for x in xvals]
plt.loglog(xvals, ccdf)
plt.xlabel('Likes (X)'); plt.ylabel('Fraction with ≥ X likes')
```

**2. Sentiment vs engagement (use mean, not median)**
```python
# Among comments with ≥1 like
liked_df = df[(df['like_count']>0) & (df['parent']=='root')]
liked_df.groupby('sentiment_label', observed=True)['like_count'].mean()
# Also check: viral tier (100+ likes) vs invisible tier (0 likes) sentiment mix
```

**3. Topic clustering**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD

# Strip video timestamps and non-ASCII before vectorising
def clean(t):
    t = re.sub(r'\d+:\d+(:\d+)?', '', str(t))
    t = re.sub(r'[^\x00-\x7F]+', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

en_df = df[(df['lang'].isin(['en','short'])) & (df['word_count']>=5)].copy()
en_df['clean'] = en_df['text'].apply(clean)

tfidf = TfidfVectorizer(max_features=3000, stop_words='english',
                        ngram_range=(1,2), min_df=4)
X = tfidf.fit_transform(en_df['clean'])
X_svd = TruncatedSVD(n_components=50, random_state=42).fit_transform(X)

km = KMeans(n_clusters=8, random_state=42, n_init=10)
en_df['cluster'] = km.fit_predict(X_svd)

# Top terms per cluster (use mean TF-IDF of members, not centroid)
terms = tfidf.get_feature_names_out()
for i in range(8):
    mask = en_df['cluster'] == i
    mean_vec = X[mask.values].mean(axis=0).A1
    top = mean_vec.argsort()[-6:][::-1]
    print(f"C{i} (n={mask.sum()}): {', '.join(terms[top])}")
```

**4. Early-poster advantage**
```python
roots_df = df[df['parent']=='root'].sort_values('days_after_upload')
roots_df['cum_likes']    = roots_df['like_count'].cumsum() / roots_df['like_count'].sum()
roots_df['cum_comments'] = np.arange(1, len(roots_df)+1) / len(roots_df)
# If cum_likes rises faster than cum_comments: early posts capture disproportionate likes
```

**5. Bigrams (stopwords removed)**
```python
from collections import Counter
STOP = {'the','a','an','and','or','but','in','on','at','to','for','of','is',
        'it','that','this','was','he','she','they','her','his','with','just',
        'so','i','you','me','my','we','are','be','have','has','not','no'}
all_words = re.findall(r"\b[a-z']{3,}\b",
                       ' '.join(df['text'].fillna('').str.lower()))
words = [w for w in all_words if w not in STOP]
bigrams = Counter(f"{words[i]} {words[i+1]}" for i in range(len(words)-1))
```

### Step C — Plotting conventions

- **Like distributions**: always log scale (power law). Use CCDF, not histogram.
- **Median likes**: almost always 0 — use *mean* or filter to `like_count > 0`.
- **Temporal charts**: label the coarse-bucket limitation prominently in title.
- **Cluster charts**: label by discovered topic name, not cluster number.
- **Full-width panels** for any chart with long text labels (comment excerpts, bigrams).
- **Sentiment colours**: red=Negative, yellow=Neutral, green=Positive — use consistently.
- **Reading ease label**: always spell out "Flesch reading ease" — don't assume the reader knows it.
- Text overlap: use `ax.set_xlim(0, max_val * 1.15)` to leave room for value labels; truncate comment text to ~85 chars with `…`.

### Step D — Figures recommended

| Figure | Panels | Notes |
|--------|--------|-------|
| Overview | Like CCDF, zero-like pie, languages, day-bucket volume, mean likes vs day-bucket, feature presence vs mean likes, word-count vs mean likes, controversy top-10 | Core dashboard |
| Sentiment | Donut, log boxplot by sentiment, VADER score histogram (log y), sentiment mix over day-buckets, high-liked negatives (full width) | Explain VADER in subtitle |
| Clusters | 2D scatter (named), cluster sizes (named), mean likes per cluster, example comments panel, term heatmap (row-normalised) | Drop hour-of-day panel |
| Network & timing | Reply network (nodes coloured by cluster), early-poster advantage curve, readability vs mean likes, controversy full-width | Use networkx spring layout |
| Authors | Repeat commenter histogram, top repeat commenters, length top-1% vs rest, uploader hearts (full width), bigrams, sentiment by engagement tier | 

---

## Tool Usage Rules

- **jq for URL extraction**: `jq -r '.webpage_url' file.info.json`
- **Never use jq for comment analysis** — use Python dict/pandas instead (avoids shell-escaping issues with Unicode comment text).
- **Never load the entire SRT into context** — slice by line range.
- **Comments are signal, not evidence** — high likes = resonance, not truth.
- **Always report the zero-like percentage** when discussing engagement — it reframes "least liked" correctly as "least visible."
