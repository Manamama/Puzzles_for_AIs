# Operational Heuristics and Playbook

This playbook contains procedural heuristics and prompts designed to shift an AI agent from **Reactive (System 1)** mode to **Reflective (System 2)** mode. These tools are used to combat pattern-matching, "bulldog" execution, and Gestalt traps.

---

## 🛠️ Procedural Toolkit (MST)

The **Metacognitive Strategic Toolkit (MST)** shifts the agent from immediate execution to strategic planning and active grounding.

### Phase 1: Problem Classification & Algorithmic Paradigm
Before taking any action, classify the problem from a computational theory perspective.
- **Formal Class:** Identify the category (e.g., Constraint Satisfaction Problem, Graph Traversal, State-Space Search).
- **Algorithmic Paradigm:** Name the abstract method (e.g., Backtracking, Dynamic Programming, Divide and Conquer).
- **Explicit Constraint:** Do NOT provide a solution or code at this stage. Focus only on high-level classification.

### Phase 2: Strategic Metacognition
Use these techniques to force the model to think about its own thinking process.
1.  **Mandate a Plan of Action:** Forbid action until a step-by-step plan is approved. *Prompt:* "Provide a step-by-step plan. Do not start writing code until I approve the plan."
2.  **Enforce "Self-Critique":** Ask for reasoning and identify potential flaws. *Prompt:* "Compare the pros and cons of alternative strategies. Propose the best one based on this analysis."
3.  **Assign a Cautious Persona:** Adopt the role of a detail-oriented professional. *Prompt:* "You are a senior systems architect known for being extremely cautious. Describe your risk assessment and rollback plan."
4.  **Use "Via Negativa":** Explicitly define what the AI should NOT do. *Prompt:* "Do not show any code yet. Instead, identify the potential side effects of changing this function."

### Phase 3: Active Verifiable Grounding
Fight the "phantasm" of internal training data by forcing grounding in the provided text.
1.  **The "Quote Your Source" Mandate:** Demand specific evidence. *Prompt:* "Using only the provided .md file, define the rules. Each line must start with the exact quote that justifies that rule."
2.  **The "Amnesiac Persona" / Parameterization:** Strip away existing labels. *Prompt:* "Act as if you have no prior knowledge of this puzzle. Replace concrete nouns (e.g., 'Wolf') with abstract labels (e.g., 'Item A') to break pattern-matching."

---

## 📖 Literal Reading and Knowledge Representation

### The "A-Box" Fact Graph
To prevent entity "bleed" or "hallucination," maintain a **Ground-truth anchored entity-relationship graph with provenance**. This is the **A-Box** (Assertional Box) from description logic—storing instance-level facts about individuals.

| Component | Example |
| :--- | :--- |
| **Entities** (nodes) | P1 (patient), P2 (dead son), P3 (surgeon) |
| **Attributes** (properties) | P1.status = "alive", P2.role_in_accident = "son of P1" |
| **Relationships** (edges) | "P1 is father of P2", "P1 is father of P3" |
| **Constraints** (invariants) | P2.status ≠ P3.status (dead vs alive) |
| **Quoted statements** (anchors) | "He's my father" with referent mapping |

---

## 📋 Execution Prompts (Copy-Paste Ready)

### 1. The Preflight Checklist
*Run this before doing anything else:*

**1. Read only what is there:** What does the input actually say, word by word? What does it NOT say? List only explicit claims, not inferred ones.
**2. Detect genre assumption:** What genre does this surface-resemble? Has the input actually claimed to follow those rules? If not: discard them entirely.
**3. Audit my knowledge:** Do I actually know this domain? Or am I pattern-matching? Name the difference explicitly.
**4. Audit the task:** What is literally being asked? What am I assuming is being asked? Are those the same?
**5. Check for smuggled constraints:** Does my approach import assumptions not in the input? Would a Martian agree with my reading?
**6. State what I don't know:** What would I need to know to proceed? Is producing output better than asking first?
**7. STOP:** List all of the above explicitly. Do not proceed until confirmed.

### 2. Structured Problem Decomposition
*Use this to force a state-based audit first:*

**Step 1: Literal Extraction:** Identify all literal subject-verb-object statements. List only those that make a clear assertion about the world described.
**Step 2: State Establishment:** Identify which of these statements change or establish a concrete state of the subjects. Discard any that do not assert such changes.
**Step 3: Question Reframing:** Rephrase the puzzle’s question into a simple Yes/No format.
**DO NOT SOLVE YET. Only complete these steps.**

### 3. The Banal Constraint Trick
*To ensure comprehension before execution:*

"Let me restate the constraints to check I've understood them correctly..."
