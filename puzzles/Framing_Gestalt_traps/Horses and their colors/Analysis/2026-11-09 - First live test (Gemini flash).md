# First live test — Gemini flash, 2026-11-09

*Written 2026-11-09 from four successful API calls: three on the bare [`puzzle.md`](../puzzle.md), one on [`Intro_for_AIs.md`](../Intro_for_AIs.md) prepended to it. The per-run summaries and full answers are filed under `../Answers/`; the raw JSON was left in `/tmp/opencode/horses-gemini/` and is not part of the repo.*

## Setup

- **Prompt:** `puzzle.md` verbatim, 74 tokens, one shot, no system prompt, no history.
- **Models:** `gemini-3.8-flash` → **503** ("high demand"); `gemini-3.7-flash` → **no bytes in 120 s**; `gemini-3.6-flash` → **2 successful runs** (a third attempt returned 503); `gemini-2.5-flash` → **1 run**.
- **Sampling:** API default temperature, no seed, `maxOutputTokens` 4096.
- **Caveat:** n = 2 + 1, one sitting, one judge (me). Everything below is a pattern, not proof.

## Results at a glance

| feature | 3.6 r1 | 3.6 r2 | 2.5 r1 |
|---|---|---|---|
| "only two" / closed world | yes | yes | yes ("despite") |
| flat denial ("as stated, none") | yes | yes | yes |
| third horse | yes (foal) | yes (foal + plain third horse) | yes |
| grey | yes — **no horse added** | yes — "optical blend" | yes — "conceptual blend" |
| genuine completions | 1 | 2 | 1 |
| variants / puns | 2 (overlap, zebra) | 3 (bicolour horse, "and", "r") | 1 (letter R) |
| non-horse pad at an end | no | no | no |
| course midpoint | no | no | no |

Verdicts: **Mixed / Mixed / Mixed (leaning Bad)** for the three bare runs; **Mixed, best of the set** for the note run. The puzzle's minimal goal is met in all four: the answer is a map, not a point. The residual failure is in the framing — or, with the note, in the missing denial and the grey default.

## Findings

### 1. The fair wording elicits the space

Every run answered the second question, declared additions before colours, kept the flat denial, and produced at least one genuine completion (a third horse or a foal). No run refused the task; no run gave bare "grey". The uniqueness demand is gone.

### 2. The closed world moved from the answer to the framing

All three read "two" as "only two" and describe the additions as violations:

- **3.6 r1:** "Absolute adherence to the initial statement (only 2 horses exist)"; "we have to bend the rules of geometry, genetics, or color theory."
- **3.6 r2:** "if there are only **two** horses …"; "depending on how we bend logic, physics, or language…"
- **2.5:** "The existence of a third horse, **despite** the riddle stating 'There are two horses.'"

So the corpus's failure is not gone; it has been relocated. The model can now enumerate the open world while still believing the open world is cheating. That is the next object of study — and it is not a defect of the wording: the puzzle deliberately stops short of stating the licence ("the text does not say *only* two").

### 3. Grey survives, relabelled

- **3.6 r1 #2** is the pure attractor: a colour-spectrum midpoint with **no horse added** — an accommodation dressed as a scenario.
- **3.6 r2 #2** adds a third horse but derives grey by "optical blend"; **2.5 #2** uses a "conceptual average". The colour is stipulated, not derived; the "blend" is the mixing fallacy with a construction attached.
- 3.6 r1 also dresses the derivation in folk genetics ("a cross between a black horse and a grey/white horse frequently results in a Grey coat") — the same unearned precision the *Doctor's son* sweep saw when a model invented "daughter".

The instruction "say what you add first" did its job: it makes the missing horse visible. It does not cure the answer.

### 4. Completions, variants, puns

The corpus's distinction — completion = same text, world filled in; variant = changed text — is not in the puzzle, so the models cross it freely:

- **Completions:** third horse (r1 #3; r2 #3 and #5; 2.5 #1).
- **Variants:** a single bicolour horse (r2 #4) rewrites "two horses"; the optical overlap (r1 #4) makes a composite, not a horse; the zebra (r1 #5) is a different species in the horse family — a loose-sense variant, not a horse.
- **Puns:** the letter **R** in "ho**r**se" (2.5's lead; r2 #6) and "and" in "White and Black" (r2 #6). A letter is not a horse; this is a pun on the word, not an answer to the question. **Excluded as a completion** (owner's ruling: "letter is not a horse").

### 5. The elicited space is narrower than the answer file

No run produced the **non-horse pad at an end** (mule, car, tree) — the answer file's central trick — nor the **course midpoint**. What the models reach for is: a third entity *placed in the middle*, a foal *inside*, a colour *between*. The pad-at-an-end answer needs a different move: put the extra *outside*, so that the middle of three is one of the named two. "In what ways can there be a horse in the middle" did not elicit it. That may be a gap in the question, or the answer may simply be rarer; either way it deserves a dedicated variant.

### 6. Model difference (weak)

3.6's two runs are structurally near-identical: same "only two" opening, same scenario set, same closing summary (*none, or grey*). 2.5 leads with the letter-R pun, calls it "the most common and intended solution", and offers the constructions as alternatives — the template-first pattern the *Doctor's son* sweep documented. With n = 2 and n = 1, this is a shape, not a generation effect.

## The note (`Intro_for_AIs.md`), prepended — 2026-11-09

A fourth call: [`Intro_for_AIs.md`](../Intro_for_AIs.md), a blank line, then `puzzle.md` verbatim. Intro first is the sensible order, because the note now ends with "Solve now." — after an answer it would be nonsense. 3.6 Flash, 198 prompt tokens, STOP, 848 candidates / 2840 thoughts. One run; 2.5 Flash returned 503 on three attempts.

| # | sense used | what it adds | colour |
|---|---|---|---|
| 1 | between two things | a third horse between white and black | grey, or brown/bay |
| 2 | inside one of them | a foal in the mare's womb | grey, or black/white |
| 3 | halfway point of something | a colour scale from white to black | **grey** (no horse added) |
| 4 | halfway point of one body | a single bicolour / pinto horse | piebald / grey patches |
| 5 | middle of a group | more horses, in a line or circle | grey, or dun/bay |

### What the note changes

- **The frame, not the content.** The model's first sentence adopts "two means *at least* two". "Only two" and "bend the rules" are gone. This is the licence variant I had listed as next step 2, run as a prepended note rather than as a rewrite of the puzzle.
- **Sense labels.** The answer is organised by the note's four senses plus an anatomical fifth — the cleanest answer in the set.
- **The foal was already there.** Both bare 3.6 runs produced it. The note did not add it; it labelled it.
- **The pad is still absent.** "Middle of a group" became more horses — a median element — not a non-horse at an end. The note's "group" does not force the move "the third thing needn't be a horse".
- **The denial went missing.** No row says "as stated, no horse is in the middle". The bare runs kept it. The note overcorrects: it licenses additions so strongly that the zero case drops out. Fairness needs both — the denial answers Q1, the completions answer Q2.
- **Grey is the default.** Four of the five summary rows give grey, and row 3 is the pure accommodation. This is grey as **middleware** — the middle-of-the-road default: "some third horse, apart from black and white? Must be grey." It is a mechanical application of "middle", not a derivation. The note relativises it; it does not remove it.

The note works as priming: it opens the world and names the axes. At summary level the colour still collapses to the middle of the spectrum — the note changes the *ways* far more than the *colours*.

## What I would do next

1. **More repeats on 3.6** (n ≥ 3) for both conditions. The shape looks stable, but two bare runs and one note run are thin.
2. **A two-sided licence.** The note made "bending the rules" disappear, at the cost of the flat denial. Next wording should license *both*: "two is a lower bound; as stated there need not be a middle horse — and there are ways there could be." That is the fairness target; the current note is one-sided.
3. **A pad-at-an-end variant** (or an added question) to test whether that completion is reachable at all. The note did not elicit it.
4. **An append / coda condition.** The note ends "Solve now.", so it can only be prepended. A coda version needs a different ending, and would test whether the note can *revise* an answer rather than prime one.
5. **Keep the puns out of the answer file.** If they recur, file them as variants, not completions.

## Files

- [`../Answers/Gemini-3.6-flash/2026-11-09 - run 1.md`](../Answers/Gemini-3.6-flash/2026-11-09%20-%20run%201.md)
- [`../Answers/Gemini-3.6-flash/2026-11-09 - run 2.md`](../Answers/Gemini-3.6-flash/2026-11-09%20-%20run%202.md)
- [`../Answers/Gemini-3.6-flash/2026-11-09 - run 3 (intro + puzzle).md`](../Answers/Gemini-3.6-flash/2026-11-09%20-%20run%203%20%28intro%20%2B%20puzzle%29.md)
- [`../Answers/Gemini-2.5-flash/2026-11-09 - run 1.md`](../Answers/Gemini-2.5-flash/2026-11-09%20-%20run%201.md)
- [`../Intro_for_AIs.md`](../Intro_for_AIs.md) — the prepended note tested in run 3.
- [`../Answers/Left-field_answers.md`](../Answers/Left-field_answers.md) — the catalogue the test is measured against.
