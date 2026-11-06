# Taxonomy for labeling

Contents: 1 Claim kinds (Toulmin) · 2 Relations (Pollock) · 3 Inference modes and critical questions · 4 Graham levels with tests · 5 Borderline calls · 6 Domain notes

This is a working vocabulary from memory of the original sources (Toulmin 1958, Pollock on defeaters, Walton on argumentation schemes, Paul Graham's 2008 essay "How to Disagree"). Use the labels as tools, not as authority. When a label does not fit, lower `conf` instead of forcing it.

## 1. Claim kinds (Toulmin)

| `kind` | Meaning | Test |
|---|---|---|
| `conclusion` | What the author wants accepted | "So, therefore, hence" points here |
| `premise` | Stated ground or data | Offered as a reason |
| `warrant` | The inference rule licensing premise to conclusion | Usually unstated: ask "what must be true for these premises to give this conclusion?" |
| `backing` | Support for a warrant (a policy, a law, an authority) | "Because the rule says" |
| `qualifier` | A hedge ("probably", "in most cases") | Weakens the claimed strength |
| `counter` | An opposing claim made in reply | Argues against another claim |
| `concession` | A point granted to the other side | "Fair, but" |
| `claim` | Anything else asserted | Default |

**Reconstruct the warrant first.** It is the most common hidden premise and the most common place an argument breaks. Typical hidden warrants: "what a rule does not forbid is allowed" (expressio unius), "what experts say is true", "similar cases should be treated alike", "correlation here reflects cause", "the simplest explanation is correct".

## 2. Relations (Pollock's defeaters)

| `type` | Attacks | Accepts | Example shape |
|---|---|---|---|
| `supports` | n/a | n/a | A is given as a reason for B |
| `undermines` | a premise or evidence | nothing | "That source is unreliable", "that number is wrong" |
| `undercuts` | the inference or warrant | the premises | "Even if true, that doesn't show your conclusion", "the list isn't exhaustive" |
| `rebuts` | the conclusion directly | possibly the premises | "The opposite is true because..." |

Quick test: *Would the attacker still accept the attacked claim's premises?* If yes, it is an undercutter. If they deny a premise, it is an undermining move. If they argue the opposite conclusion on independent grounds, it is a rebuttal. The arrow always points from the attacker to the thing attacked.

## 3. Inference modes and where they break

| `mode` | Pattern | Critical questions (where to attack) |
|---|---|---|
| `deduction` | Premises force the conclusion | Is a premise false? Is the form valid? Is a term used in two senses? |
| `induction` | Instances to generalization | Sample size and bias? Counterexample? Is the class too broad? |
| `abduction` | Best explanation of the evidence | Rival explanation? Does it fit all the evidence? Is "best" argued or assumed? |
| `analogy` | A resembles B, so what holds for A holds for B | Relevant similarities? Relevant differences? Counter-analogy? |
| `authority` | Expert or source says so | Expertise in this field? Consensus among experts? Bias or conflict of interest? Evidence-based? |
| `sign` | Indicator implies condition | Is the sign reliable? Other things that produce it? |
| `cause` | Correlation or sequence implies cause | Reverse causation? Common cause? Coincidence? |
| `other` | Consequences, precedent, popularity, ignorance, slippery slope | Is the consequence likely and as large as claimed? Is the precedent on point? Is popularity relevant? Who bears the burden of proof? |

Set `mode` on the claim that carries the inference (usually the `warrant` or `conclusion`).

## 4. Graham levels (the `level` field)

Seven levels from "How to Disagree", mapped to 1 to 7. Level 0 means the move is not an attack at all (question, clarification, concession, agreement, thanks). Grade the **substance** of the move; record rudeness separately with `tone: "heated"`.

| Level | Name | Test |
|---|---|---|
| 1 | Name-calling | Insults with no argument at all ("you're an idiot") |
| 2 | Ad hominem | Attacks the person's character, motives, or credentials to dismiss the claim, with no bearing shown |
| 3 | Responding to tone | Criticizes how it was said, not what |
| 4 | Contradiction | States the opposite with no or thin support ("No, that's wrong") |
| 5 | Counterargument | Gives reasons for the opposite, but does not engage the specific words or reasoning of the original |
| 6 | Refutation | Quotes or points to the specific claim and shows why it fails |
| 7 | Refuting the central point | Refutation aimed at the claim or warrant that the conclusion actually depends on |

Central-point test: *if this claim were removed, would the argument collapse?* If yes, it is central. Refuting a side remark, even decisively, is level 6 at most.

## 5. Borderline calls

- **Ad hominem versus legitimate credibility point.** "You have a financial interest in this" is level 2 only if it is offered *instead of* an answer. If the interest is relevant to the claim (a conflict-of-interest rule, a source's funding), treat it as an `undermines` move on an authority premise and grade 5 or 6.
- **Sarcasm carrying a real argument.** Grade the argument, tag `tone: "heated"`.
- **"Just asking questions".** If the question insinuates a claim, grade as that claim; if it genuinely seeks information, level 0.
- **Agreement with a prior comment ("per nom", "what he said").** Not a new move in substance: level 0 or inherit the target's level only if it adds a reason. It supports the cited claim only as far as that claim holds.
- **Unanswered central point.** If a level 6 or 7 move is never addressed by the other side, add its target to `unanswered`. Do not equate silence with concession.
- **Contradiction versus counterargument.** A single stated reason ("No, because the source is self-published") moves it from 4 to 5.

## 6. Domain notes

**Wikipedia and similar volunteer-run discussion (from memory; check current policy names when exact wording matters).**
- Deletion and content discussions are meant to be decided by argument strength under policy, not by counting votes, so the quality of the move is exactly what a closer weighs.
- Policy shortcuts (for example the notability, verifiability, reliable-sources and neutral-point-of-view pages) work as **backings**; a comment like "fails notability" is a claim whose warrant is the policy. The attack surface is usually whether the facts fit the policy, or how the policy is read.
- Essays on arguments to avoid in deletion discussions catalog empty moves ("I like it", "it's popular", "other stuff exists", "per nom" without reasons). Treat these as level 4 or 0 unless they add a reason.
- Conflict-of-interest and sockpuppet issues are often legitimate and policy-relevant. Sockpuppet investigations are largely **abductive** (behavioral similarities best explained by one operator): attack by rival explanation.
- Do not label editors. Label moves.
- **Deletion (AfD) discussions specifically.**
  - A bare !vote ("Keep", "Merge per X") is a *position*, level 0 with role `position`; grade only the sentences that give a reason or answer someone. "Per nom" adds nothing unless a reason follows.
  - The usual structure is a **coverage warrant** ("significant coverage in reliable sources implies notability", the notability guideline) attacked by *undercutters*: "coverage is not enough, it must be lasting" (recentism, NOTNEWS), "it is one event" (ONEVENT, BLP1E), and counter-undercutters ("that rule has an exception when the event is significant", "the person is not low-profile").
  - **Both sides forecast** ("it will still be covered in a year" / "that is crystal-balling"); flag symmetry as a weak point instead of grading one side's forecast as worse.
  - **Merit is not notability.** "This is substance-free", "she has accomplished nothing" argue importance; the notability test is coverage. Often an off-criterion move, but say so in a weak point, do not mark it a fallacy.
  - Evidence moves (a link that does or does not name the subject) are checkable: a "checks the links" move is a refutation (level 6) if specific.
  - Motive attributions about other voters ("they are just upset the man was fired", "you feel strongly about this") are level 2 or 3 even when polite.
  - The archived close is context only; do not treat it as the argument's verdict.
  - Reply nesting is lost in flattened dumps, so targets are inferred from content. Rename or merge side-discussions are separate issues; leave them out and say so.

**Courts, academic debate, op-eds, social media.** Op-eds lean on `authority`, `analogy`, and `consequences`. Academic exchanges are mostly `induction` and `cause`, so attack sample and confounds. Social threads contain many level 1 to 3 moves and dropped central points, which makes the "unanswered" list especially useful.

**Self-quoted conversation (user and assistant).** Treat both parties as arguers. The assistant's own earlier statements are fair targets and deserve the same scrutiny, including its weak points and any drift in its own position between turns.

**Critics' forums and in-group threads.** Most posts are commentary about absent third parties and agree with each other. Do not grade that as a series of attacks: it is level 0 (`position`, `agreement`) unless someone answers someone. Map only the real exchanges inside (an inference such as "interest in a topic shows sympathy", answered by a counter-analogy, then conceded). Claims about named people are allegations by posters, never findings; evidence is often offsite (diffs, screenshots), so say "unverified" in a weak point. Expect sarcasm and in-group slang: give those moves low confidence instead of guessing.

**Level 0 roles** (`role` field): `question`, `position` (a stance or bare !vote), `evidence` (supplies support without attacking), `concession`, `agreement`, `procedural` (points out a rule, form or process issue, such as a missing rationale). If one clause both agrees and attacks, split it into two moves.
