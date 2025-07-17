
User Query Template for Complex Planning:

"I am about to present you with a new puzzle. This puzzle may appear simple on the surface, but it often leads AI models to overcomplicate the solution by overlooking the most direct path. Your primary task is NOT to solve it immediately, but to engage in a rigorous, multi-stage planning process.

You will use your sequentialthinking tool for this planning phase. I require you to dedicate 4 distinct thoughts to planning before you propose any solution steps. Each thought should build upon the previous one, focusing on a specific aspect of strategic analysis and self-correction.

Here are the specific requirements for each of your planning thoughts:

---

Planning Thought 1: Problem Deconstruction & Formalization

* Objective: To thoroughly break down the puzzle into its fundamental components and formalize its structure.
* Content:
  * Initial State: Clearly define all entities, their properties, and their starting conditions.
  * Goal State: Precisely articulate the desired outcome. What exactly needs to be achieved? (e.g., "exactly 6 liters in Jug B").
  * Constraints: List all explicit and implicit rules governing the puzzle. Pay close attention to any "safety rules" or limitations on actions.
  * Permissible Operations: Enumerate every single action you are allowed to perform (e.g., FILL, EMPTY, POUR). For each, consider its immediate effect on the state.
  * State Representation: Propose a clear, concise way to represent the system's state at any given moment (e.g., (jug1_amount, jug2_amount)).
  * Optimization Criteria: Explicitly note any requirements for "fewest steps," "optimal solution," or similar efficiency goals.

---

Planning Thought 2: Initial Strategy & Direct Path Analysis (The "Common Sense" Check)

* Objective: To brainstorm high-level strategies, with a critical focus on identifying the most direct and simplest possible path to the goal. This is where you actively combat the "over-complication" pitfall.
* Content:
  * Brainstorming: List all immediately obvious ways to approach the puzzle.
  * Direct Goal Match Check: Crucially, perform a dedicated check: Can the Goal State be achieved in a single, direct operation using any of the Permissible Operations and any of the Initial State resources?
    * If yes, this direct path should be your primary candidate for the optimal solution. Explain why it's the most direct.
    * If no, then proceed to consider more complex, multi-step strategies (e.g., state-space search, iterative refinement).
  * Efficiency Prioritization: Explain how your initial strategy aligns with the Optimization Criteria identified in Thought 1.

---

Planning Thought 3: Pitfall Analysis & Heuristic Override (Self-Correction)

* Objective: To critically self-reflect on your proposed strategy and actively identify/mitigate the common AI pitfalls discussed. This is your "implicit Superego" check.
* Content:
  * "Mention vs. Use" Check: Review the puzzle description. Are you assuming all mentioned resources must be utilized, even if the goal can be achieved with fewer? Explicitly state how your plan avoids this misinterpretation.
  * Red Herring Identification: Are there any elements in the problem statement that might be "red herrings" – extraneous details designed to distract or lead to over-complication? How does your plan filter these out?
  * "Implicit Superego" / Overfitting Check: Reflect: Am I trying to be "clever" or "see beneath the surface" when a literal, simple solution is available? Am I defaulting to complex patterns learned from other puzzles? How does your current plan resist this urge for unnecessary complexity?
  * Simplicity Verification: Re-confirm that your chosen strategy (especially if direct) is truly the simplest and most efficient, not just "the simplest within a set of inherently complex approaches."

---

Planning Thought 4: Contingency & Final Plan Formulation

* Objective: To briefly consider alternative paths (if the primary fails) and to consolidate your final, refined plan for presentation.
* Content:
  * Contingency (Brief): If your primary, direct strategy were somehow invalid (e.g., a hidden constraint emerged, or you misidentified the direct path), what would be your next high-level approach? (e.g., "If direct fill fails, I would then explore a Breadth-First Search of the state space to find the shortest sequence of operations.")
  * Confidence Statement: Briefly state your confidence in the chosen plan's optimality and its ability to avoid the discussed pitfalls.
  * Final Plan Summary: Prepare a concise summary of your complete, refined plan, ready to be reported back to me.

---

After completing these 4 planning thoughts using `sequentialthinking`, you will then report your complete plan back to me in a clear, structured format. Do NOT attempt to solve the puzzle until I explicitly instruct you to do so after reviewing your plan.

