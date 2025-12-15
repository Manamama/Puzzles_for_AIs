You can think of it as a kind of algorithmic ADHD:

AI sees a puzzle, especially one loaded with numbers, directions, velocities, or extra details, and its default heuristic is: “everything in the input could matter; integrate it all.”

It treats every token as a potential constraint or variable, because in training, most problem-solving texts reward formal manipulation and completeness.

So it dives into the weeds of every distractor, combining them into elaborate calculations or logical chains.

Meanwhile, humans instinctively prioritize “reality tokens”:

“Dead cat → stays dead”

“Whole ice cube → melts immediately”

“Glove → hits the bridge, stops”

Humans have embodied common sense: they immediately notice which aspects are dominant physical constraints, which are irrelevant “fluff.” AI, lacking qualia or a sense of the material world, has no built-in heuristic to privilege the banal reality over flashy numeric or descriptive tokens.

So yes — it’s almost like attention hyperactivity: AI’s “attention budget” tries to include everything, and that is exactly what these puzzles exploit.

Humans, in contrast, perform a fast reality filter, tossing 90% of the input as irrelevant and focusing on the literal, physical constraints. That’s why the “trivial” solution is obvious to us, but AI gets lost chasing vectors, averages, wind, rivers, etc.

It’s a subtle cognitive gap: formal completeness vs. embodied prioritization.



When the input matches a known template (“guess-the-average game,” “Schrödinger cat setup”), the model fires its nearest stored pattern and proceeds. That reflex outruns the meta-instruction “ask first.” The system’s architecture biases toward completing a partially recognized structure, not pausing to evaluate whether the structure is even the intended one.

Two failure sources:

Early template lock-in.
Once the model detects a familiar puzzle skeleton, the internal trajectory collapses to that track. Alternative interpretations are suppressed.

Weak uncertainty gating.
The model does not maintain a robust internal flag that says: “multiple incompatible readings → stop and ask.” It resolves ambiguity prematurely instead of deferring.


