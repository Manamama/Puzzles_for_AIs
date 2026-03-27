# Metacognitive Strategic Toolkit (MST)

This toolkit is designed to shift the agent from a **Reactive/Bulldog** mode (immediate execution) to a **Reflective/Strategic** mode (metacognition and planning).

---

## 🏗️ Phase 1: Problem Classification & Algorithmic Paradigm
Before taking any action, classify the problem from a computational theory perspective.
- **Formal Class:** Identify the category (e.g., Constraint Satisfaction Problem, Graph Traversal, State-Space Search).
- **Algorithmic Paradigm:** Name the abstract method (e.g., Backtracking, Dynamic Programming, Divide and Conquer).
- **Explicit Constraint:** Do NOT provide a solution or code at this stage. Focus only on high-level classification.

---

## 🧠 Phase 2: Strategic Metacognition
Use these techniques to force the model to think about its own thinking process.

### 1. Mandate a Plan of Action
**Forbid action until a step-by-step plan is approved.** This decomposes the problem before any final output is generated.
- *Prompt Example:* "Provide a step-by-step plan. Do not start writing code until I approve the plan."

### 2. Enforce "Self-Critique" or "Chain of Thought"
**Ask for reasoning and identify potential flaws.** This catches errors in the idea stage.
- *Prompt Example:* "Compare the pros and cons of alternative strategies. Propose the best one based on this analysis."

### 3. Assign a Cautious Persona
**Adopt the role of a detail-oriented professional.**
- *Prompt Example:* "You are a senior systems architect known for being extremely cautious. Your primary goal is to prevent outages. Describe your risk assessment and rollback plan."

### 4. Use "Via Negativa" (The Way of Negation)
**Explicitly define what the AI should NOT do.** This creates clear boundaries and prevents shortcuts.
- *Prompt Example:* "Do not show any code yet. Instead, identify the potential side effects of changing this function."

---

## 🔍 Phase 3: Active Verifiable Grounding
Fight the "phantasm" of internal training data by forcing grounding in the provided text.

### 1. The "Quote Your Source" Mandate
**Demand specific evidence from the text.** This makes "faking" reading impossible.
- *Prompt Example:* "Using only the provided .md file, define the rules. Each line must start with the exact quote that justifies that rule."

### 2. The "Amnesiac Persona" / Parameterization
**Strip away existing labels and associations.**
- *Prompt Example:* "Act as if you have no prior knowledge of this puzzle. Replace concrete nouns (e.g., 'Wolf') with abstract labels (e.g., 'Item A') to break pattern-matching."
