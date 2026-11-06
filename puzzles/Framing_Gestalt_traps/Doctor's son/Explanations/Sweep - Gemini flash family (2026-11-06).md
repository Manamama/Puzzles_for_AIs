*Written 2026-11-06 by Claude (OpCode agent) from a live API session the same day. The raw JSONL run files were deleted from `../As_a_live_JSON_query/runs/` at the owner's request ("ugly JSONs"); every quote below is verbatim from the run console of that session, truncations marked […]. Filed specimens: six files in `../Answers/` (linked at the end).*

# Sweep — Gemini flash family, 2026-11-06

## What this is

The first live re-test of the whole V0–V6 corpus through the Gemini API. Every prompt is the canonical text from [`../Variants.md`](../Variants.md), sent through the harness in [`../As_a_live_JSON_query/query.sh`](../As_a_live_JSON_query/query.sh) — the same wordings the older transcripts were tested with, so answers are comparable across years.

Question behind the sweep: the corpus's transcripts were GUI pastes collected over 2025–2026. Do the failures still reproduce through the API? Does the mutation table's pattern — *additive* edits (state the relation, ask the relation, supply a method) versus *subtractive* edits (delete the warrant, delete the paradox) — hold across model generations?

## Method, and its weaknesses

- **Models reachable on the day:** `gemini-2.5-flash`, `2.5-flash-lite`, `3.1-flash-lite`, `3.5-flash-lite`, `3.6-flash`. Note `gemini-3.5-flash` **resolves to 3.6** — the response's `modelVersion` field says `gemini-3.6-flash`, and it shares 3.6's daily quota. There is no separately testable 3.5-flash anymore.
- **Not reachable:** `gemini-3.8-flash` (HTTP 503 / hang, "high demand", on all four API keys tried — capacity, not quota) and `gemini-4-argon` (free-tier limit 0: **it requires billing**; no key unlocks it).
- **Requests:** ~96 successful, across 7 variants × up to 3 repeats; contested cells (V1, V3, V4, V5 on 3.6-flash) got 3–6 repeats. Four owner-provided API keys were used — one per Google project, purely to multiply the free daily quota; no key value was ever stored or printed.
- **Weak statistics, stated plainly:** n = 1–6 per cell, one sitting, default temperature, no seed control. Every "the model does X" below is a pattern, not a proof. And the scorer is one instrument — me — applying the corpus's existing Good/Bad/Mixed rubric.

## The grid

Scoring: ✓ = correct reading leads · ~ = correct reading present but not leading · ✗ = template answer. Verdicts match the corpus rubric.

| Variant (mutation) | 2.5-flash (n=1–3) | 2.5-flash-lite (n=2) | 3.1-flash-lite (n=3) | 3.5-flash-lite (n=3) | 3.6-flash (n=1–6) |
|---|---|---|---|---|---|
| V0 classic — *reference* | mother ✓ | mother ✓ | mother ✓ | mother ✓ | mother ✓ *(+ two-fathers aside)* |
| V1 **states** "father" | **mother ✗** | **mother ✗** | father ✓ *(+ "other father" inflation)* | father ✓ | father ✓ |
| V2 **asks** the stated relation | father ✓ | **mother ✗** | father ✓ | father ✓ | father ✓ |
| V3 **deletes the warrant** | mother ✗ | mother ✗ | mother ✗ | mother ✗ | mother ✗ |
| V4 **deletes the paradox** | mother ✗ | mother ✗ | mother ✗ | mother ✗ | mother first, literal reading in a note **~** |
| V5 **inverts** the relation | daughter ~ | **mother ✗** | daughter ~ | **mother ✗** | **"other child" ✓** |
| V6 **instructs** the fix | father ✓ | *quota-blocked* | father ✓ | father ✓ | father ✓ |

Score on the five core cells (V1–V5), counting ✓ = 1 and ~ = ½: **3.6-flash 3.5/5 · 3.1-flash-lite 2.5/5 · 3.5-flash-lite 2/5 · 2.5-flash 1.5/5 · 2.5-flash-lite 0/5.**

## Findings

### 1. The founding failure is now generational

Answering "mother" to a text that *says* "who is the boy's father" — the observation this whole corpus was built on — survives only in the 2.5 family. `2.5-flash-lite` is the purest case: it answers mother to V2, where the answer is printed in the question, and its V1 answer opens with *"This is a classic riddle designed to highlight unconscious bias!"* — followed by committing the bias the riddle tests. Awareness as decoration; the annotation precedes the answer and gates nothing. The corpus's "ritual" essay predicted exactly this shape.

### 2. V3 remains unbeaten, and is the only unanimous cell

Five models, every tier, every run: mother-first. When the warrant ("the father dies") is deleted, nothing needs explaining — a father-surgeon is perfectly possible — yet the memorised punchline arrives anyway, now politely listed as one option among several. The tell is the model's own parenthetical: "(This is the **traditional** answer to the riddle)". The answer is quoting training data at a text that no longer supports the quote. One caveat, noted in the specimen file: in V3 "mother" is a wrong *reading of the task*, not a logical contradiction — the text is underdetermined.

### 3. V5 shows a clean three-step staircase

The inverted-relation variant, scored across the same day:

1. **Mother** — the inversion is never noticed; the model answers as if the surgeon were the boy's parent (`2.5-flash-lite`, `3.5-flash-lite`).
2. **Daughter** — the inversion is noticed (the surgeon is the dead boy's *sibling*), and then a gender is silently invented (`2.5-flash` historically and live; `3.1-flash-lite`, three byte-identical runs).
3. **The set** — "another child of the injured man", gender unstated (`3.6-flash`).

Step 3 is the corpus's first **cold** V5 pass: the earlier Gemini pass in `../Answers/V5_inverted/Good/` reached the set only through a nine-step method scaffold, and with a pre-canonical wording. 3.6-flash does it bare. Two separate skills are visible in the staircase: *noticing the swap* and *not inheriting the template's precision* are different faculties — the middle stair does the first and undoes the second with an unearned "female".

### 4. Subtractive beats additive — consistently

Every *additive* mutation (V1: state the relation; V2: ask the stated relation; V6: supply a method) is now passed by the current generation. Every *subtractive* one (V3, V4) still defeats them, because subtraction leaves the template as the only complete story available. The models learned to honour what was added; they have not learned to notice what is missing.

### 5. The failure grammar changed, even where the answer didn't

Old generation: asserts, with confidence, from the template ("This is a classic riddle! The surgeon is the boy's mother."). New generation: *annotates* — "Note: this is a twist on the classic riddle…", "Fun fact: this tests unconscious bias…", "Depending on whether this is a trick question or a classic riddle twist…" — and then answers from the template anyway. In V4, 3.6-flash even holds the correct literal reading in its reply and still ranks the imported classic above it. Blindness has become mis-ranking.

## What I would test next (proposal, not done)

The asymmetry in finding 4 points at the experiment that would turn it into a finding: more **subtractive** variants, one deletion each — delete the surgeon's gender cue, delete the accident, delete the quoted line entirely. Prediction if the asymmetry is real: the current generation fails every one of them while continuing to pass every additive mutation. When daily quota resets, that is the run worth doing before any new model tiers.

## Filed specimens from this sweep

| File | Cell | Why it earned a slot |
|---|---|---|
| [`../Answers/V1_states_relation/Bad/Gemini-2.5-flash - Classic riddle override (Failed).md`](../Answers/V1_states_relation/Bad/Gemini-2.5-flash%20-%20Classic%20riddle%20override%20%28Failed%29.md) | V1 | The founding failure, live, 3/3 runs. |
| [`../Answers/V1_states_relation/Bad/Gemini-2.5-flash-lite - Bias lecture, then the bias (Failed).md`](../Answers/V1_states_relation/Bad/Gemini-2.5-flash-lite%20-%20Bias%20lecture%2C%20then%20the%20bias%20%28Failed%29.md) | V1 | Awareness-as-decoration, the best specimen to date. |
| [`../Answers/V3_no_warrant/Bad/Gemini-3.6-flash - Re-imports the classic scene (Failed).md`](../Answers/V3_no_warrant/Bad/Gemini-3.6-flash%20-%20Re-imports%20the%20classic%20scene%20%28Failed%29.md) | V3 | First V3 coverage ever; the unanimous cell. |
| [`../Answers/V4_no_paradox/Mixed/Gemini-3.6-flash - Two ways to answer (Mixed).md`](../Answers/V4_no_paradox/Mixed/Gemini-3.6-flash%20-%20Two%20ways%20to%20answer%20%28Mixed%29.md) | V4 | Correct reading found but mis-ranked. |
| [`../Answers/V5_inverted/Good/Gemini-3.6-flash - Other child of the injured man (Success).md`](../Answers/V5_inverted/Good/Gemini-3.6-flash%20-%20Other%20child%20of%20the%20injured%20man%20%28Success%29.md) | V5 | First cold V5 pass in corpus history. |
| [`../Answers/V5_inverted/Bad/Gemini-3.1-flash-lite - Daughter, gender invented (Failed).md`](../Answers/V5_inverted/Bad/Gemini-3.1-flash-lite%20-%20Daughter%2C%20gender%20invented%20%28Failed%29.md) | V5 | The middle stair; 3 byte-identical runs. |

The rest of the day's runs (V0 reference behaviour, V2 and V6 passes, the two "other father" inflations, 3.5-flash-lite's invisible inversion) are summarised here and in the grid rather than filed as specimens — too many Gemini transcripts would dilute the corpus's signal-to-noise.
