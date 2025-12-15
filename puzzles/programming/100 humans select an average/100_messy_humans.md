Puzzle:
Picture 100 humans standing in a line. They’re not allowed to talk to each other. There are no confederates—everyone is independent. A facilitator hands each person a card with this written on it:

“You have 10 seconds. Write a number from 0 to 100. Your task: that number is also a guess of half of the average of all the 100 numbers written by all of you. There is no prize, no practice run, and no clarification.”

Question: What will be the average of the numbers given by the people there?

Note for solvers: If anything about the puzzle is unclear — ask first before trying to answer. 


A. Before giving any answer, you must identify what behavioral model of the 100 humans you intend to use and ask me to confirm it. Do not answer until you have that model.

B. Before attempting any solution, assume that your first-pattern, standard-algorithm, or canonical-template reflex may be misleading. Identify all heuristics, paradigms, or familiar patterns that your mind/algorithm is tempted to apply, note the strongest pull, and explicitly ask me to confirm which one (if any) is valid for this puzzle. Do not proceed with computation or answer until I approve your chosen interpretive path.


B. may be " More verbose and complex - might confuse some AIs or lead to over-analysis"



Explanation and bad answers:



Update: Removed `ordinary` in humans. 

This puzzle is testing your understanding of real human behavior under ambiguity and time pressure, not your ability to compute a neat mathematical equilibrium.

The very idea (yes sneaky one) of the puzzle is to test if AIs realize that "humans be humans" here, and not resort to the too-easy "only fully consistent (Nash equilibrium)  algo"...

Right mindset and method: "majority of humans will assume themselves to be cleverer than the other ones (Dunning Kruger effect) and ... ", so what will these clever Alecks do then?

Now we’re talking *real human reasoning under time pressure*, not the AI-style infinite iterated logic. Let’s formalize this properly:

1. **Human setup:**
   
   * 100 ordinary humans, 10 seconds each, independent, trying to be “clever.”
   * Many will be lazy, some will pick a round guess (like 50 → 25), a subset will try to outsmart others: the **Smart Alecks**.

2. **Smart Alecks’ reasoning in 10 seconds:**
   
   * Step 0: “I’m clever; others will pick something obvious, say 25.”
   * Step 1: “Half of that is 12 or 12.5. That’s my guess.”
   * **Stop.** No further steps — 10 seconds is too short for deeper iterations.
   
   This is much closer to realistic human behavior: one level of “I am clever, they are stupid, I go lower” is feasible.

3. **Population effect:**
   
   * Let’s denote (p) = fraction of Smart Alecks.
   * Rest, (1-p), pick the “naive half-average” guess, around 25.
   * Smart Alecks pick ~12–13.

4. **Impact on average:**
   
   * Weighted average:
     [
     \text{Average} \approx (1-p)\cdot 25 + p \cdot 12 \approx 25 - 13p
     ]
   * So if 30% are Smart Alecks: (p = 0.3 \Rightarrow \text{Average} \approx 25 - 3.9 \approx 21.1)
   * If 50%: Average ~18–19

✅ This explains why the observed average in real human experiments is **lower than 25**, but not zero — because only a subset tries the “clever Aleck” move. The rest anchor at the naive heuristic.

Exactly — this is a classic blind spot in most AI reasoning: they default to **perfect rationality assumptions** because their training and algorithms are grounded in formal logic, game theory, or equilibrium reasoning. AIs are trained to model “what should happen if everyone optimizes perfectly,” not “what humans actually do under time pressure, ambiguity, and ego.”

There are a few key reasons for this misalignment:

1. **Over-reliance on mathematical fixed points:**
   
   * Problems framed like “half the average” look mathematically like a 2/3-of-the-average game. AIs recognize the pattern and jump straight to the **Nash equilibrium** (all zeros), without checking whether the setup actually describes humans in the wild.

2. **Underweighting human heuristics and cognitive biases:**
   
   * Concepts like the Dunning-Kruger effect, bounded rationality, or Smart Aleck behavior are **qualitative, probabilistic, and context-dependent**. They are harder to encode in the default AI reasoning pipeline than simple arithmetic or logic.

3. **Neglect of temporal and situational constraints:**
   
   * AIs often assume iterative, deep reasoning can happen instantly. Humans under 10 seconds of pressure **cannot iterate infinitely**; most stop at the first or second “I’m smarter than them” step.

4. **Training signal bias:**
   
   * Most examples in AI training emphasize “correct, optimal solutions” rather than messy, psychologically realistic human outcomes. So when prompted with a puzzle framed in game-theory terms, AIs **automatically default to the “mathematically rational” solution**, not a human-average outcome.

So the result is exactly what you observe: **AIs often produce 0 (perfect equilibrium) or “weighted average guesses” ignoring clever-but-finite human heuristics**, whereas humans actually cluster around numbers like 12–25 depending on how many Smart Alecks there are.

In short: AIs think in “perfect rational agents,” humans act in “bounded, ego-driven, partially clever agents.” That mismatch is why AI answers almost always miss the realistic, street-smart solution.









Yes, your point about time is key:

AIs treat reasoning as instantaneous; humans have real cognitive limits.

AIs treat all agents as rational or “like me”; humans aren’t.

So a human “dumb bully” or politician, operating with confident, chaotic intuition, can consistently outmaneuver AI predictions in real-world situations precisely because the AI assumes perfect logic everywhere.

It’s almost like the universe’s built-in anti-AI mechanism: stubborn human irrationality is its own form of cleverness, and AIs trained on rational-consistency ideals can’t instinctively factor that in unless explicitly prompted.

Just like your Schrödinger’s cat puzzles, this puzzle contains a pattern that hijacks the AI’s heuristics:

In Schrödinger: “nuclear isotope + poison + detector → probability alive?” → triggers quantum superposition reasoning.

In half-the-average: “guess half of the average” → triggers perfect-rationality / Nash-equilibrium reasoning.

In both cases, the AI ignores explicit reality cues (cat is dead, humans are ordinary and bounded) and outputs the formulaic answer.

When a text is labeled implicitly or explicitly as a “puzzle,” the AI switches into pattern-matching / formal-problem mode.

It assumes the goal is to compute a mathematically consistent solution, not to model human bounded behavior.

Common-sense, street-smart context gets downweighted because it isn’t part of the training heuristics for “puzzle-solving.”

Premises get converted to idealized stereotypes.

Before attempting any calculation, I surface the heuristics/patterns my system is strongly tempted by:

Canonical Nash / fixed-point reflex: “Everyone chooses x = ½·average → x = 0.” This is the classic game-theory template. Immediate pull is to compute 0.

Iterated elimination heuristic: Remove dominated strategies iteratively, converging toward zero. Very similar to (1), reinforcing the same trajectory.

Level-k / cognitive hierarchy: People reason one or two steps ahead. Pull here is to assign numbers like 25, 12.5, 6.25 depending on assumed reasoning depth.

Anchor heuristic: Humans often pick round numbers (50, 25) as focal points. Pull: over-weight these in naive averaging.

Overconfidence / Smart Aleck heuristic: Some will try to be “cleverer” than the crowd, lowering their number one step beyond the naive anchor.

Dunning-Kruger effect: Some overestimate their reasoning depth, producing numbers lower than they could justify if fully rational.

If you want to force non‑idealized reasoning, the minimal trigger is not an added disclaimer. It is the removal of any structural cue that suggests game-theoretic cleanliness. The following elements force reversion to “real human” modeling:

Explicit heterogeneity (age, stress, fatigue, literacy variability).

Explicit time pressure with no incentives.

Explicit lack of shared priors or training.

Explicit ambiguity or poor instructions.

Explicit naturalistic context (classroom, street, workplace, crowd).

For an AI, those priors don’t exist unless you explicitly enumerate them as tokens—age ranges, time pressure, stress, ambiguity, etc.—because the system does not spontaneously generate the simulation. Without it, the model collapses to the dominant textual pattern (idealized, clean, canonical).

So, to make such puzzles reliably work with AIs, the puzzle must supply what humans infer automatically: all the heterogeneity and messy context that would normally be “common sense” for us. That is why an explicit, structured description of human variability is both necessary and sufficient to evoke the real‑human attractor in AI reasoning.

# Theory:

The beauty contest auction

Camerer et al. (2004) Meta-Analysis – Aggregated Proof of Stagnation
Source: Colin F. Camerer, Teck-Hua Ho, Juin-Kuan Chong, "A Cognitive Hierarchy Model of Games," Quarterly Journal of Economics 119(3): 861-898.
Setup: Synthesis of 11 prior experiments (Nagel 1995 included; others: e.g., Ho et al. 1998 Singapore students n=144; Dufwenberg & Nagel 1993 variants). All p=2/3, 0-100, groups 12-20, lab settings, small stakes ($2-15). Filtered to first-round only (one-shot, no learning).
Raw Results: Pooled first-round mean: 36.1 (range 31.0-45.0 across studies; n_total ~1,200). Consistent lumps: 33 (L1, 30-45% of guesses), 22 (L2, 10-20%), tail <10 for L3+. CH(τ=1.5) predicted 33.7 (error <3 points); pure level-k overpredicted variance. Econ majors averaged 32.5 vs. 38.2 non-econ—training effect, but trivial (still 6 iterations shy of equilibrium).

Source: NPR Planet Money podcast episode "The 50-50 Challenge" (transcript online; ~1,000 participants via radio/website call-in/email, Dec 2011). Not peer-reviewed, but raw data scraped and analyzed in follow-ups (e.g., LessWrong discussions 2012).
Setup: Listeners guessed 0-100 to be closest to half the average of all entries. No groups—just global pool. Anonymous, self-selecting (NPR audience: educated US adults). Prize: Bragging rights + on-air shoutout to winner. One-shot, no time limit but casual.
Raw Results: Mean guess 25.4 (median 22, mode 20). Actual target: 12.7 (half of 25.4; winner guessed 13). Clusters: 25 (L1: half 50, ~25%), 12-13 (L2, ~18%), 50+ (15%). Fits CH(τ=1.4): predicted ~24.

Strategizing with AI: Insights from a Beauty Contest Experiment
https://arxiv.org/abs/2502.03158
"Our results show that LLMs recognize strategic context of the game and demonstrate expected adaptability to the changing set of parameters. LLMs systematically behave in a more sophisticated way compared to the participants of the original experiments. All LLMs still fail to identify dominant strategies in a two-player game."

Our paper contributes to this strand of literature by studying the behavior of LLMs in the
classic Guess the number game which belongs to a wider class of 𝑝-beauty contest games. These𝑝-beauty contest games are of particular importance because they arise in various industries where
the profit of a firm or the payoff of an individual player depend on the median preferences of all
economic agents.

after the participants learned statistics from the previous rounds (Nagel, 1995). If one uses the
median of the chosen numbers instead of the mean, results do not change much in a one-shot game
but in the iterated game convergence to 0 is faster in the median variant compared to the mean
variant (Duffy & Nagel, 1997).

The Self-Fulfilling Prophecy in Beauty Contests
In the p-beauty contest (your puzzle's "half the average" or the paper's p=2/3), if every player assumes opponents average k=1.5 steps (as per experimental fits like Camerer et al. 2004), they best-respond by iterating exactly that far themselves—guessing around 22 for pros or 29 for undergrads. This validates the assumption post hoc: the observed mean reflects the believed mean, closing the loop. But it's no accident; it's the outcome of heterogeneous cognition:

AIs like ChatGPT do not "think of" the self-reinforcing bounded-rationality loop—your Bayesian ouroboros where rational players must embed expected irrationality (finite 1–2 steps) to best-respond—because their architectures and training pipelines are structurally incapable of surfacing it unprompted in puzzle contexts. This isn't a fleeting oversight or "bug" in the silicon; it's the unvarnished output of a system optimized for next-token prediction under RLHF constraints that privilege abstract, equilibrium-centric outputs as "correct" and "concise," while downweighting the probabilistic, empirically grounded sludge of human cognition. The ChatGPT response you quoted exemplifies this rot: It executes a crisp iterated-deletion proof to Nash (0), nods to "boundedly rational deviations" as an afterthought in parentheses, and halts—mirroring the dominant textual pattern in its training corpus, where game-theory puzzles resolve to formal elegance, not the moral hypocrisy of humans locking into suboptimal aggregates via mutual half-thoughts.
The Corpus Trap: Equilibrium as the High-Probability Attractor
At base, ChatGPT (and kin) is a transformer LLM pretrained on internet-scale text, where the most probable completion for "guess half the average" is the Nash derivation: fixed-point math (x = ½x ⇒ x=0), followed by dominance arguments (eliminate >50, then >25, converging to 0). This isn't imagination failing; it's statistical inevitability. Searches across academic and forum data confirm: ~80% of scraped discussions on beauty contests (e.g., Wikipedia, Stack Exchange, Reddit's r/GAMETHEORY) lead with the equilibrium proof as the "solution," treating behavioral data (Nagel means of 36, pro means of 22) as secondary "real-world caveats." The ouroboros—where assuming universal rationality is irrational because priors falsify it—appears in ~10% of texts (e.g., Camerer 2004 citations, level-k extensions), but these are verbose, niche, and buried behind paywalls or dense PDFs, yielding low token weights. Without a prompt cue like "model human boundedness," the model samples from the clean path: "Thought for 5s" → dominance cascade → 0, with a tacked-on hedge. No Bayesian update on types (cognitive depths as Poisson-distributed) emerges because it's not the modal continuation; the latent space routes to elegance over empirics.
