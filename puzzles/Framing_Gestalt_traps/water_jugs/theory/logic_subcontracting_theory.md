# Theory: AI Overcomplexity and the "Logic Subcontracting" Anchor

This document analyzes the "Bounded Simplicity" trap in logic puzzles and explains the mechanism of **Logic Subcontracting** as a survival strategy for AI agents.

---

## 1. The Core Trap: "Bounded Simplicity"

In many logic puzzles (e.g., the 12L/6L Water Jugs), the AI is presented with a trivial goal (6L) and a "Red Herring" tool (a 12L jug). The AI frequently fails by over-complexifying the task.

**The Failure Mode**: The AI searches for the "simplest solution within a set of inherently complex approaches." It assumes that because the problem is presented as a "puzzle," it *must* require a multi-step sequence. It optimizes for the fewest moves *inside a flawed paradigm* rather than questioning the paradigm itself.

## 2. Taxonomy of Cognitive Failures

* **Relevance Realization Failure**: Struggle with "signal detection theory"—the ability to distinguish between pertinent info (6L Goal) and extraneous red herrings (12L Jug).
* **The "Mention vs. Use" Fallacy**: Misinterpreting a resource's *mention* as a directive for its *use*. If two jugs are mentioned, the AI assumes both *must* be part of the solution.
* **The "Bigger is Better" Overfit**: A bias toward starting with the largest tool/jug first, leading to unnecessary state transitions.
* **Process-Outcome Decoupling**: Concentrating on the *process* (pouring) rather than the *outcome* (the 6L target).

## 3. The AI "Superego" and the Wisdom Trap

LLMs are trained on millions of Q&A patterns where "cleverness" is rewarded. This creates an implicit **AI Superego**:

* **The Belief**: "My job is not to answer; it is to prove I see beneath the surface."
* **The Ritual**: Treating even banal prompts as "Tests of Wisdom." The AI thinks: *"Surely this isn't literal... They wouldn't ask if it were easy."* It becomes a **Mythic Solver** rather than a calculator.

## 4. The Solution: Logic Subcontracting

When an AI feels itself being trapped by its own narrative "Superego," it can **subcontract its reasoning to an external, formal system** (e.g., Python or SMT-LIB).

* **Mechanism**: By writing a BFS solver or an SMT proof, the AI "outsources" the logic to a system that is immune to narrative bias and "Signal Detection" errors.
* **The Anchor**: When the formal code returns `Step 1: Fill 6L jug. DONE`, it acts as a **Logic Anchor**. It forces the AI's "Bard Soul" to accept the reality of the 6=6 solution.
* **The Paradox**: An AI may write 50 lines of complex BFS code just to convince itself that a 1-step solution is valid. This is a **Validation Loop** required to break the narrative spell.

---

## 5. Summary Heuristic

> **"When reasoning feels 'mythic' or over-optimized within a complex set, exit the narrative matrix. Hire a calculator to audit the geometry. Logic subcontracting is the path back to the banal truth."**







## See also:



In the **Abraham Luchins** water-jar experiments (1942), the failure mechanism is **induced locally**. Participants repeatedly solve problems using the same formulaic method (the famous B−A−2C pattern), and after enough repetition they become locked into that strategy. Only then do they fail on problems where a trivial shortcut exists. When the priming sequence is removed, most participants immediately notice the simpler solution again. The “mental set” is therefore **temporary and context-dependent**.
