---
name: Argument map
description: Turn a messy dispute (op-ed with replies, Wikipedia AfD or talk discussion, forum exchange, email chain, debate transcript, or part of the current conversation) into an interactive argument map plus move timeline, so a human can grasp who argued what and where it holds or breaks. The agent first decides what is worth analyzing, preprocesses the raw dump into clean speaker-labelled text, extracts claims and unstated warrants, labels attacks as undermining, undercutting or rebutting (Toulmin, Pollock), grades moves on Graham's hierarchy of disagreement, and flags weak and unanswered points. Needs only Python 3 and its standard library, runs offline, and produces one self-contained HTML file. Use for "map this argument", "break down this debate", "analyze this AfD / discussion", "where does this reasoning fail", "is this a good rebuttal", uploaded messy threads, Toulmin, defeaters or ad hominem levels. Not for plain summaries, formal proofs, or fact-checking.
---

# Argument map

Purpose: **help a human grasp a dispute fast and check the reading themselves.** The output is a self-contained HTML page with three views: an **argument map** (claims, inferences, attacks), a **move timeline** (click any dot to see who said what, the exact quote and the grade, so labels are quick to verify), and a **summary** (weak points, unanswered points, reconstructed claims). The agent does the analysis and emits JSON; fixed scripts do the cleaning and drawing. Never hand-draw SVG.

## Best for, and not for

Works well on: a few people disagreeing about one specific claim and giving reasons (op-ed plus replies, debate transcripts, email chains, design or code-review disputes); **deletion/notability discussions** (the real fight is policy interpretation: is the coverage enough, does ONEVENT apply, will it last); **inference-heavy exchanges** where the action is an unstated warrant, an analogy or a sign, and undercutting is the key move; threads that sour (the timeline shows the slide).

Works poorly on: in-group venting about absent third parties (nobody answers anybody, so grades mislead); pure factual disputes (evidence settles them, not structure); emotional or relationship quarrels (few claims, and grading people's moves is unkind); sarcasm- and slang-heavy text (many low-confidence labels). If the input is mostly one of these, say so in one line and offer the narrowest useful thing (for example, map only the one real exchange inside it).

Sweet spot: one issue, 2 to 5 voices (or two stances with many voices), 6 to 16 claims.

## Workflow

0. **Triage: what is worth analyzing?** Skim the input. Pick the *issues* where people actually answer each other and give reasons; skip bare votes, pleasantries, side-chat, pure Q&A, and anything not an argument. Decide the issue(s) (at most three maps) and say in one line what you kept and what you left out. If the whole input is a poor fit, say that instead of forcing it. Ask a question only if you cannot tell which text is meant.
1. **Preprocess. Mandatory; never analyze a raw dump.** Raw pages carry navigation, profile blocks, signatures, nested quote chains and timestamps that corrupt attribution and quote checks.
   - Wikipedia AfD pages, phpBB-style forum dumps and `[Speaker] text` files: `python scripts/prep.py INPUT work/ [--format afd|forum|plain]`. It writes `work/source.txt` (one `[Speaker] text` line per post, quote chains and signatures removed, IP addresses anonymised) and `work/posts.json`, and prints a report. **Read the report**: speaker names are heuristics (check odd ones), flags mark unmatched quotes or merged lines, and the !vote tally counts last explicit vote per editor by leading keyword only. For small threads count by hand and say it is approximate.
   - Anything else: build the same `[Speaker] text` file yourself (one line per post or paragraph), verbatim, without chrome. For a single-speaker text use `[Author]`.
   - Leave out of the source anything not part of the argument: real names from profile blocks, and personal details (health, politics, identity) from user pages. Keep the post text itself verbatim.
   - `build.py --source` must point at this cleaned file.
2. **Mode.** A single argument gets claims and relations only. A multi-party thread also gets `moves`.
3. **Segment and attribute.** Work at clause level: one comment can hold a refutation followed by a jab. If a thread has many speakers, put them in `groups` by stance (for example keep / merge / delete) so colour means a side, not a name.
4. **Extract claims.** One short neutral sentence each; verbatim `span` (about 25 words max). `stated` if the author asserted it; `reconstructed` for missing premises and warrants (be charitable, never invent a position). Merge restatements. Set `withdrawn: true` on a claim its author later conceded or retracted.
5. **Relate claims** with exactly four types (see `references/taxonomy.md`): `supports`, `undermines` (attacks a premise), `undercuts` (accepts premises, denies they support the conclusion), `rebuts` (argues the conclusion false). Look for undercutting first. For jointly required premises, say so in the relation `note`.
6. **Name the inference mode** on inferential claims and use the matching critical questions from the taxonomy to locate where it can be attacked.
7. **Grade moves** (threads only). Level 1 to 7 only for a move that answers or attacks something. **Level 0 is not a grade**: use it for positions, questions, evidence, concessions, agreement and procedural remarks, and always give a `role`. Never force a level on an opening move or a bare !vote. Tone is a separate axis (`tone: "heated"`). Add `when` (a date) where it helps.
8. **Flag weak points** (at most six): where the *strongest* argument is softest, whichever side it is on, plus anything central never answered (`unanswered`). Include doubts about your own reading. If both sides rest on forecasts, say so.
9. **Write JSON, build, read every warning.** Schema: `references/schema.md`.
   ```bash
   python scripts/build.py work/map.json work/argument-map-<topic>.html --source work/source.txt
   ```
   It checks structure, that every quote occurs in the source, that a stated quote occurs in a post *by the named speaker*, and lints level-0 moves that also attack. Fix errors; investigate warnings; do not silence them. Build into `work/`, then copy or move the HTML wherever the user will look for it — the current working directory by default, a path they named if they named one. Keep `<topic>` short and kebab-cased.
10. **Check and deliver.** Judge the exit status: `0` means the file was written (warnings are not failures); `2` means validation errors and **nothing was written**, so fix and rebuild. If a browser or page-inspection tool is available, load the file once and confirm there are no script errors and that the three tabs (Argument map, Move timeline, Summary) exist; otherwise confirm the file exists and is not empty. Then give the user the **absolute path** and offer to open it (`xdg-open` on Linux, `open` on macOS, or their normal browser). Only use an "artifact" or inline-widget delivery if this environment really has one; a file path is the default and is never wrong.
11. **Reply briefly** (three to five sentences): the central point (often the warrant), the softest spot, anything unanswered, what you left out, and one caveat: labels are a model's reading; click a dot in the timeline to see the quote and override the level. Remind the user that the views are tabs at the top of the page (scroll up if not visible).

## Rules that matter

- **Label moves, never people.** Real, named (often pseudonymous) people are in these threads. No person-level scoreboards; the summary shows counts only for speakers with three or more graded moves.
- **Show what was argued, not what is true.** Allegations about people stay attributed ("X argues that..."). If something is checkable and looks false, say so in a weak-point note ("depends on offsite evidence, unverified"); never silently correct the map.
- **Quote, don't paraphrase, in `span`.** `build.py` rejects spans not in the source.
- **Calibrate `conf`:** 0.9+ only if the text says it outright; about 0.7 a clear reading; 0.5 or below a judgment call. Low confidence renders hollow or faint, on purpose; do not raise it to make a picture look cleaner.
- **Context matters.** "Per policy X", COI remarks and !votes are often legitimate moves; see the taxonomy's domain notes.
- **No winner** unless asked. An archived close is context, not a verdict.
- **Keep the map readable:** about 6 to 16 claims, at most three maps per thread.

## Large threads

Group the dispute into issues. Build the **timeline over all graded moves** and one **map per major issue**, each its own built file with an issue-specific `title`. Put the issues and what you left out in the `context` line.

## Requirements

Python 3, standard library only (`json`, `re`, `sys`, `os`, `collections`). No pip install, no network, no API key, no browser needed to *build*. `python3` is enough. Every path in this file is relative to the directory containing this `SKILL.md`; run the scripts from there (`cd <skill dir> && python scripts/...`) or pass absolute paths. The built page is one self-contained HTML file — no CDN, no webfonts, no external script — so it opens offline and can be emailed, committed or hosted as-is.

`bash scripts/selftest.sh` rebuilds both bundled examples into a throwaway directory and fails loudly if either stops validating. Run it after editing any script or the renderer.

## Files

- `scripts/prep.py`: raw dump to clean `[Speaker] text` source plus report (AfD, forum, plain).
- `scripts/build.py`: validator and builder (Python 3 only).
- `scripts/selftest.sh`: fixture check; run after edits.
- `assets/renderer.html`: the fixed template. Edit it only to change visuals for everyone.
- `references/taxonomy.md`: levels with tests, Toulmin parts, defeaters, inference modes, borderline calls, domain notes (Wikipedia AfD, forums). Read before step 5.
- `references/schema.md`: exact JSON fields. Read before step 9.
- `assets/example*.json` + sources: a worked single argument and a short synthetic thread, as format models.
- `assets/example-thread-source.txt` + `example-thread.json` double as the test fixtures used by `selftest.sh`: if you change the schema, change them together.

## Known limits (say so when relevant)

- Layout is automatic and layered; edges that skip layers can pass behind boxes, and dense cyclic maps get cluttered above about 16 claims. The detail panel lists every relation as text.
- Linked premises (jointly required) are not drawn differently; a concession or retraction is shown only by `withdrawn`, not as an edge.
- Labels are judgment calls and the level scale is ordinal, not a measurement. `build.py` checks that quotes exist (and whose they are), not that the reading is right.
- AfD dumps are flattened: reply nesting is lost, so reply targets are inferred from content. Speaker names from `prep.py` are heuristics.
- A thread that is mostly agreement or Q&A will be mostly level 0; that is a correct result.
