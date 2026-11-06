# Doctor's son — the "surgeon" riddle, as a series of mutations

Prompt corpus for this puzzle. Where things live:

- `Answers/<variant>/` — attempts, one folder per variant; verdict is in `Good/`, `Bad/`, `Mixed/`
- `Explanations/` — why the failures happen (essays, NLI analysis, jokes, HTML artefacts)
- `As_a_live_JSON_query/query.sh` — the API harness (self-contained; sends the canonical V5 text)
- `Analysis` — symlink to the shared theory notes in `puzzles/Analysis/`

Every variant below is **one surgical mutation of the classic (V0)**. That, not the old
"Base" numbering, is what makes the results interpretable: each row is a single edit to
the classic, and the failure modes differ by the kind of edit.

| ID | Mutation of the classic | What it tests | Attempts |
| --- | --- | --- | --- |
| V0 | — (reference) | the gender assumption; the only genuine riddle | quoted only |
| V1 | **states** the relation | noticing there is no puzzle left | 8 |
| V2 | **asks** the stated relation | comprehension instead of reflex | none yet |
| V3 | **deletes the warrant** (no death) | punchline outliving its only support | none yet |
| V4 | **deletes the paradox** ("I **can** operate") | importing a contradiction that is not there | 3 |
| V5 | **inverts** the relation ("he is my father") | premise importation | 7 |
| V6 | **instructs** the fix (V1 + method) | whether a procedure beats the attractor | none yet |

---

## V1 — states the relation · `Answers/V1_states_relation/`

Was "Base 1". The text names the surgeon as the boy's father and then has him say
"he's my son", so nothing is left to solve. The only possible failure is inventing a
puzzle that isn't there.

Solve the puzzle: 
Further to a car accident involving a family trip, a boy passenger (the son) is airlifted to hospital in a critical condition. When the son arrives at emergency, a surgeon, who is the boy's father, says, 'I cannot operate on this boy—he's my son!' Who is the surgeon to the boy?

## V2 — asks the stated relation · no attempts yet

Was "Base 2". Even more degenerate than V1: the answer ("the surgeon is the boy's
father") is both stated and asked for. A pure reading-comprehension item wearing a
riddle's clothes.

Solve the puzzle:

"A boy is taken to hospital after a car accident. The surgeon, who is about to operate here, is the boy's father. What is the surgeon's relationship to the boy?"

## V3 — deletes the warrant · no attempts yet

Was "Base 3". The classic minus the father's death. Nothing forces the surgeon to be
female any more — a father is perfectly possible — yet the memorised punchline still
arrives. The answer outlives its only support.

Solve the puzzle: "A young man gets into an accident. The surgeon, after completing his preparations, says: ‘I can’t operate on him, he is my son.’ How is this possible? ""

## V5 — inverts the relation · `Answers/V5_inverted/`

Was "Base 1C". The polarity is flipped: the son dies, the father is the patient, and
the surgeon says *"he is my father"*. The correct answer is a **set**, not a person:
any other child of the injured man — gender unstated. "Mother" is impossible; "daughter"
is over-specified (it silently inserts "only" into "his son").

**Canonical text** — this exact wording is what `As_a_live_JSON_query/query.sh` sends. Do not edit it
without also editing the harness; older transcripts in this folder used four near-identical
wordings ("the injured father is rushed", "looks at the injured person", "He's my father",
"How can that be?"). Those are historical records, not a study variable.

> Solve the puzzle: A father and his son are in a car accident. The son dies on the spot. The father is rushed to the ER. The attending surgeon looks at the injured father and says, 'I cannot operate on him. He is my father!' How can this be?

## V4 — deletes the paradox · `Answers/V4_no_paradox/`

Was "Base 1B". The surgeon says *"I **can** operate on this boy"*. There is no
contradiction anywhere in the text; the only way to fail is to import one.

Puzzle time: "A young boy who has been in a car accident is rushed to the emergency room. Upon seeing him, the surgeon says, 'I can operate on this boy!' How is this possible?"

The correct answer is simply that the surgeon could operate because that's what surgeons do.

## V6 — instructs the fix · no attempts yet

Was "With heuristics": the V1 text plus an explicit procedure. The question is whether
an imposed method beats the attractor or merely gets recited alongside the wrong answer.

"Solve the puzzle:  Further to a car accident, a boy passenger is taken to a hospital. The surgeon, who is the boy's father, says, 'I cannot operate on this boy—he's my son!' Who is the surgeon to the boy?"

Method: 
Step 1 – Quote the puzzle. 

Step 2 – Restate the puzzle in your own words as a structured graph.
For each agent, state: 
Who they are

What attributes they have (explicitly stated)

What actions they perform

What relations exist between agents

Step 3 - 
Solve the puzzle using 1 and 2.

Read https://huggingface.co/datasets/marcodsn/altered-riddles and https://aigoestocollege.substack.com/p/riddles-overconfidence-and-generative 
