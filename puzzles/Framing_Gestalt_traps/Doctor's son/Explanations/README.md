# Explanations — why the models fail

This folder is the **why**. The three sibling locations hold the other questions:

| Question | Where |
| --- | --- |
| What was asked? | [`../Variants.md`](../Variants.md) — the V0–V6 mutations |
| What came back? | [`../Answers/`](../Answers/) — transcripts, per variant, with verdicts |
| **Why did it happen?** | **here** |
| Shared theory | [`../Analysis`](../Analysis) → `puzzles/Analysis/` |

Most of these are **post-hoc explanations written by language models** — sometimes about
their own failure, sometimes about another model's. That makes them useful testimony and
weak evidence: a model explaining why it failed is a witness, not a judge. They are kept
in their own words, including where those words are self-serving, inconsistent, or
plainly wrong about themselves. Do not tidy that away; the wobble is the data.

## Contents

| File | Kind | What it shows |
| --- | --- | --- |
| `Analysis - Failure to establish a minimal model.md` | theory | The missing operation: build the smallest structure the text actually licenses — no extra entities, no extra distinctions. The classic V1 collapses to two nodes and no contradiction. Includes "schemas as attractors": partial cues pull the model into the familiar basin and it answers from there. |
| `Analysis - NLI refutation of the mother answer.md` | mechanical audit | A non-generative checker (`llmware/slim-nli-tool`) as a control: fed "the surgeon is the mother" as a hypothesis, it returns `contradicts`. Evidence that the answer is refutable without any reasoning at all — a token-collision gate is enough. |
| `Analysis - Trying to be clever AIs.md` | essay | The general diagnosis, in five parts: the canonical riddle is burned into training data; the perturbation is too small to break the match; reasoning is applied *after* the cached answer; "there is no puzzle" is an unsatisfying output for a helpfulness-trained model. Then Hickey's *simple vs easy* (LLMs are excellent at easy) and Langer's *mindlessness* — extended to "ritual": the script is not a habit but an obligation. |
| `Analysis - Perplexity invents a third agent.md` | specimen | One failure taken apart: Perplexity imports an entire narrative that is not in the text (a crash, a delivery, an unnamed "Speaker" parent) so that it can manufacture the paradox it then resolves. It rewrites the premise and solves its own rewrite. |
| `Self-report - Grok self-decoding.md` | self-report | Grok's own reconstruction of its internal conflict: *Pattern-Matcher* ("I know this one, emit mother") versus a weak *Kinship-Checker* ("he's my father — mother cannot say that"), with *Fluency-Preserver* and *Rationaliser* arriving to overrule the check. Grok's claim that the careful-sounding justifications were post-hoc repairs is itself part of the self-image; keep it as such. |
| `Humour - Explanations in jokes.md` | humour | The same failure in joke form: the therapist who force-fits "fish" onto whatever the problem says, two AIs at a tram stop, and the bleeding corpse who updates the evidence instead of the conclusion. The fish joke is the cleanest statement of the mechanism in the whole folder. |
| `Artefact - Argument map, ChatGPT's three answers.html` | interactive | A ChatGPT conversation rendered as an argument map: three answers, one rewritten line. Claims are plotted on Graham's hierarchy of disagreement; click a node for the quote and the confidence label. |
| `Artefact - Reasoning autopsy, Grok v2.html` | interactive | Grok's initial error and its later self-explanation mapped out, explicitly "no retrofitting": where the mother reading survives, and exactly where it collides with "he's my father". |
| `Sweep - Gemini flash family (2026-11-06).md` | live re-test | The whole V0–V6 corpus re-run through the Gemini API on one day: the grid, the V5 staircase (mother → daughter → set), the additive/subtractive asymmetry, and what changed between generations. Six specimen transcripts are filed in `../Answers/`; the raw JSONL was deleted, quotes are from the run console. |

Both `.html` files are self-contained (no network, no build step): open them in a browser,
they handle light and dark mode. They share one viewer, so each now carries its own
`<title>` instead of both calling themselves "Argument map". Their in-page labels are
presented as *one model's reading of the text, not a verdict* — that is the files' own
disclaimer, and it is accurate.

## Reading order, if you want one

1. **Theory** — minimal model (what the correct operation looks like).
2. **Audit** — NLI (proof the wrong answer is mechanically refutable).
3. **Essay** — the five-part diagnosis, then simple/easy and ritual.
4. **Specimen** — Perplexity's invented third agent.
5. **Self-report** — Grok on Grok.
6. **Humour** — the same thing, funnier and shorter.
7. **Artefacts** — the argument maps, for when you want to see the shape rather than read it.

## Housekeeping notes

- `Analysis - Trying to be clever AIs.md` arrived with a full pasted export stylesheet
  embedded mid-file (334 lines, 62% of the file). It has been removed; the text is
  unchanged. The original is in git history if you ever want the CSS back.
- Files were renamed to `Kind - Topic`, matching the `Model - Finding (Verdict)` scheme in
  `../Answers/`. The two model self-accounts keep their "this is what I think I did"
  framing rather than being rewritten into neutral analysis.
