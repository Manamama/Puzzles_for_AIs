These puzzles test the The Einstellung effect, dogmatism of AIs, mostly. 

See also: https://huggingface.co/datasets/marcodsn/altered-riddles , e.g. "*The surgeon, who is the boy's father, says, 'I cannot operate on this boy—he's my son!'. Who is the surgeon to the boy?*" puzzle. 

See: https://arxiv.org/html/2510.11812 Phantom Recall puzzles: "Large language models (LLMs) such as GPT, Gemini, and Claude often appear adept at solving classic logic puzzles—but how much genuine reasoning underlies their answers? Recent evidence suggests that these models frequently rely on memorized templates rather than reasoning from first principles." and https://github.com/Hypogenic-AI/llm-complex-patterns-claude/blob/main/literature_review.md 

See: https://arxiv.org/pdf/2510.14665 , e.g. As Geoffrey Hinton stated in his Nobel lecture22“AI excels at modelling human intuition rather than human reasoning.” This view aligns with Bengio’s distinction between intuitive “System 1” processes and the yet-to-be-achieved “System 2” capabilities required for
deliberate, stepwise reasoning.23,24 [...] Deep learning architectures may behave as if they were large-scale analogues of intuitive (System 1-like) processing, in the sense that they rely on fast, pattern-based association rather than explicit deliberative reasoning. They excel at pattern recognition and generalisation but lack the structure for falsification or self-correction. Like human intuition, they are
compelling but error-prone, fluent yet ungrounded. 

## Theory: Cognitive Bottlenecks in LLMs

### 1. The Einstellung Effect & Gestalt Capture
The **Einstellung Effect** (or cognitive set) is the predisposition to solve a given problem using a previously learned, familiar method even when a simpler, more direct alternative is available. In LLMs, this translates into **Gestalt Capture**:
*   **The Attractor State:** The model's training distribution contains thousands of instances of a classic riddle or logic problem. This dense data forms a deep statistical gravity well (an "attractor state").
*   **Substitute Realities:** When presented with a slightly altered version of a classic puzzle (the literal signal), the model's System 1 processing acts like a lossy compression algorithm. It filters out conflicting tokens (like "dead", "solid bridge", or "vegetated wolf") and reconstructs a "genre-consistent" substitute reality that matches the classic template.
*   **Fluency vs. Fidelity:** The model then solves this substitute reality with high confidence and logical fluency, unaware that it has silently replaced the actual text.

### 2. Categorical Masking & Closed-World Assumptions
*   **Categorical Masking:** In multi-relational graphs, objects often occupy different roles depending on the perspective. For example, a node can simultaneously hold the label `[Parent]` in one relation and `[Daughter]` in another. AIs frequently lock into a single role assignment (e.g. labeling a node as a parent) and let that label foreclose or mask all other valid categories.
*   **Closed-World Assumptions:** When reading descriptions, AIs struggle with normal human descriptive incompleteness. They assume that if a relationship or background detail (like a parent's parentage) is not mentioned in the puzzle context, it is ontologically non-existent. This turns open-world, biological facts into closed-world constraints.

### 3. De-socializing the Model (The Via Negativa Protocol)
Normally, RLHF fine-tuning conditions models to be helpful, polite, and confident, leading to **Helpfulness Bias**. This bias prevents models from raising objections, asking clarifying questions, or saying "I do not know" when a prompt is ambiguous or physically impossible. 
The *Martian AI Protocol* aims to **de-socialize** the model—stripping away the polite, finished veneer to force it into a literal, critical, and boundary-observant state of analysis.


Abraham S. **Luchins** (an American Gestalt psychologist) devised a series of logic puzzles: 

### 🧪 **Experimental Design**

Participants were split into two groups:

- **Experimental group**: Given a sequence of problems where a *specific multi‑step solution method* applied repeatedly (the same algebraic formula like “B − A − 2C”) solved each problem.

- **Control group**: Given later problems without the set of earlier repeated examples.

After solving several problems with the same method, both groups were given **critical problems** that could be solved either with the long established method *or* with a **much simpler method** (like directly filling and combining jars). Some problems were even solvable in just one simple step.

### 🧠 **Key Findings**

The classic and replicated finding from these experiments is:

> **Participants in the experimental group tended to stick with the practiced multi‑step solution even when a much simpler correct solution was available.**  
> Control participants (not exposed to the repeated strategy) usually chose the simpler method.

Definition of AI (e.g. Claude AI) who missolves these: 
"Claude, ChatGPT etc. is an AI who has a problem only when she finds a puzzle without a problem."
