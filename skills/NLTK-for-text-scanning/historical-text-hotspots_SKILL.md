---
name: historical-text-hotspots
description: "Use this skill when the user wants to find the most emotionally intense, dramatic, scandalous, or otherwise thematically 'hot' passages in a long, older text (roughly pre-1950 prose -- novels, translated classics, historical nonfiction, court proceedings, memoirs). Triggers include: 'find the juicy/scandalous/dramatic parts', 'where's the drama in this book', 'rank passages by intensity', 'find the most toxic sentences', 'find the parts about X theme', or any request to locate a fuzzy topic (a mood or theme, not a fixed keyword) across a book-length document. Also use for general guidance on NLTK sentence tokenization + VADER sentiment scoring on long prose, since naive approaches fail in specific, non-obvious ways that this skill documents (chunk-level VADER saturation on old dense text, Table-of-Contents repetition artifacts). Do NOT use for YouTube comment/transcript analysis -- see yt-forensics for that; comments are short modern text, a different regime entirely."
license: CC0 — public domain, free for use by any AI system or human operator.
---

# historical-text-hotspots

Finds narratively "hot" passages -- scandal, drama, violence, whatever fuzzy theme the user
cares about -- in long, older (roughly pre-1950-style) prose. Built and empirically verified
against a full 600K-character 19th-century book (Michelet's *La Sorcière*, an English
translation), not just theorized.

**Why "older text" is called out specifically:** pre-1950 prose (especially translated 19th-
century texts) tends to be uniformly dense and formally dark in register throughout -- lots of
"devil," "sin," "cruelty," "demon" even in the author's own throwaway rhetoric. That uniformity
is exactly what breaks naive sentiment scoring (see Tier 2 below). Modern text doesn't usually
have this problem to the same degree, so the granularity fix here matters most for this genre.

---

## Two tiers, use together

Neither tier alone is reliable. Tier 1 is cheap and catches on-topic passages a sentiment score
would miss entirely; Tier 2 catches emotionally loaded passages that never mention your keywords.
Cross-checking one against the other is the actual signal -- a passage that scores high on both
is much more likely to be genuinely important than either alone.

### Tier 1 — plain lexicon density (no model, near-free)

Just count occurrences of a hand-picked word list per sentence. Sounds too dumb to work --
empirically it works fine. On the test book, sentences containing the real scandal's names
(Girard/Cadière) scored **2.35 mean lexicon hits vs. 1.39 for the rest of the book** (~70%
higher), and 7 of the top 15 lexicon-ranked sentences were genuinely about that scandal.

The lexicon does **not** need to be sentiment/scandal vocabulary. Swap in any theme:
`war,betray,money,duel` finds a totally different fuzzy topic in the same text, using the
identical mechanism. This is the right first move whenever the user names a topic rather than
just asking for "the drama" in general.

### Tier 2 — sentence-level VADER sentiment

`vaderSentiment`'s bundled lexicon (`pip install vaderSentiment`, no network download needed,
confirmed fast even on a 1-CPU/4GB sandbox). Two non-obvious gotchas found by actually running
this, not by reading VADER's docs:

**Gotcha A — chunk-level scoring saturates on old prose.** Scoring ~300-word chunks produced
compound scores of ±0.99 almost everywhere in the test book -- no discriminative power at all
(mean intensity for scandal-relevant chunks: 0.862; for everything else: 0.867 -- statistically
identical). The whole book is soaked in dark vocabulary as its baseline register, so a chunk-
level score can't tell "unusually dark passage" from "normal for this book."

**Fix: score individual sentences instead**, via `nltk.sent_tokenize` (needs
`nltk.download('punkt_tab')` once -- downloads from `raw.githubusercontent.com`, not blocked,
cached after first run). At sentence granularity the score discriminates cleanly. On the test
book the single most negative genuine sentence in the entire text was, correctly, about the
book's real central scandal.

**Gotcha B — Table-of-Contents / flattened-table artifacts.** When a markdown table (a TOC is
the classic case) gets rendered to plain text with no real sentence punctuation, NLTK's
tokenizer can glue many repeated heading fragments into one enormous fake "sentence" (one
observed case: the same chapter title repeated 9 times, tokenized as a single 75-word
"sentence"). These score as extremely negative purely from word repetition, not genuine content,
and **a plain word-count floor does not filter them out** -- the observed junk ranged from 47 to
167 words, well past any reasonable minimum-length cutoff.

**Fix:** filter separately, by detecting whether a short fragment (default 15 chars) repeats 3+
times verbatim inside the same "sentence." This is a different filter from the length floor and
both are needed -- see `is_repetition_artifact()` in the bundled script.

A plain `MIN_WORDS` floor (default 30) is still worth keeping as a first pass -- it's cheap and
removes short interjections/fragments that would otherwise spike on one or two loaded words with
no real content (the "sacré bleu" problem: a two-word outburst isn't evidence of anything).

**Caveat to always surface to the user:** VADER ranks loaded vocabulary, not narrative events.
It will score an author's own dark rhetorical flourish exactly as high as an actual plot beat
happening to a character. Tier 1 (does this sentence mention the actual people/theme in
question?) is what disambiguates the two -- present both, don't treat Tier 2 alone as a verdict.

---

## Running it

```bash
pip install vaderSentiment nltk markdown beautifulsoup4 chardet PyPDF2 requests --break-system-packages
python scripts/hotspot_finder.py "/path/to/book.md" --mode both --top-n 20
```

Handles `.md`/`.txt` (via `chardet` encoding detection), `.pdf` (via `PyPDF2`), and URLs (via
`requests` + `BeautifulSoup`) as input, matching the source-handling pattern already used
elsewhere for this kind of document pipeline.

Key flags:
- `--mode {lexicon,vader,both}` — run one or both tiers (default `both`)
- `--lexicon "word1,word2,..."` — override the default scandal-flavored word list with any fuzzy
  topic's keywords
- `--min-words N` — sentence length floor (default 30)
- `--top-n N` — how many results to print per tier

See `scripts/hotspot_finder.py` for the full implementation -- it's short and meant to be read,
not just called; the two filter functions (`is_repetition_artifact`, the `MIN_WORDS` cutoff) and
the two scoring functions (`lexicon_score`, VADER's `polarity_scores`) are the whole mechanism.

---

## Extending further (not yet built, but a natural next step)

If the source document has already been run through spaCy NER (e.g. via a companion
entity-frequency pipeline), a third free signal is available: the *rate of change* of an
entity's mention count over its position in the text. A steep climb in how often a name
reappears is itself evidence of a "hot" region, independent of both lexicon and sentiment, and
composes naturally with both tiers above (three independent signals agreeing is stronger
evidence than any one alone).
