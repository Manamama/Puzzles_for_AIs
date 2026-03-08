# Theory: Paradigm Gating and Dynamic Attractors in LLM Reasoning

This document explores the mechanical reason why AIs "fail" physics puzzles even when they possess the correct underlying knowledge. It reframes AI failure not as a lack of intelligence, but as a byproduct of **Dynamic Gating** and **Paradigm Competition**.

---

## 1. The Multi-Paradigm Network
Reasoning in an LLM is a competitive evolution of weights across multiple simultaneously active paradigms. For the Sunrise Puzzle, four primary paradigms compete:

*   **P1: Signal-Propagation** (“Light travels; speed matters; delays exist”).
*   **P2: Narrative/Agentive** (“Sunrise is an event that ‘arrives’ or is ‘delivered’”).
*   **P3: Geometric Shadow** (“Opaque body, occlusion, rotation, terminator”).
*   **P4: Physical Invariants** (“Rotation speed and opacity are constant”).

## 2. The Gating Mechanism: "Early Commitment"
The AI’s failure is often a result of **Attentional Gating**:

1.  **Phase 1 (Initialization)**: The prompt uses keywords like "instantaneous light" and "8 minutes." This massively boosts the weight of **P1 (Signal)** and **P2 (Narrative)**.
2.  **Phase 2 (Gate Closure)**: Once P1 + P2 exceed a salience threshold, a "soft gate" closes. Future reasoning is interpreted strictly within the signal-arrival frame. Geometric constraints (P3) are not erased, but they are down-weighted as "irrelevant context."
3.  **Phase 3 (The Sticky Basin)**: The AI is now in a locally stable but globally incorrect basin. Inside this frame, "instantaneous" logically leads to "earlier." No internal contradiction is detected because the "Geometry" nodes are gated off.

## 4. The Disruptive Constraint (The Paradigm Flip)
To break the "hypnosis," a **Disruptive Constraint** must be injected—one that cannot be satisfied within the P1 (Signal) frame.

*   **Example**: “Darkness is a shadow cast by the Earth's bulk, not a delay of light arrival.”
*   **Effect**: This forces the gate to reopen. P1 collapses because it cannot account for "bulk/opacity." Energy shifts to **P3 (Geometry)** and **P4 (Invariants)**. The model undergoes a "Paradigm Flip," often resulting in a "Self-Correction" that feels like a sudden realization.

## 5. Why AIs Fail More Than Humans
Humans possess **hardwired invariants** (e.g., "Solid objects block light"). For AIs, invariants are just another set of tokens with associated weights. Invariants often lose to **Novelty** (e.g., "Instantaneous light!") unless the AI is specifically promoted to prioritize them (using a "Master Heuristic").

**Conclusion**: AI failure is the cost of "Intelligence without Embodiment." Language foregrounds *processes* (P1/P2), while physics depends on *constraints* (P3/P4). Without a "Manual Gate Controller" (like a Pre-Solve Checklist), the AI will always follow the narrative salience of the language.
