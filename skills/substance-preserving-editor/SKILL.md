---

name: substance-preserving-editor
description: Protocol for high-fidelity document consolidation and conceptual shifting, preventing lossy 'banal summarization'.

---

# Substance-Preserving Editor (BTS Protocol)

This skill provides a methodology for consolidating large amounts of deep technical, poetic, or analytical text into fewer files without losing the "substance" or "artefacts" (metaphors, nuances, complex dialogues). It is designed to counteract the AI tendency to perform lossy compression (banal bullet points).

## The Core Principle: Block-Transfer, Not Summarization

Treat the source material as a collection of **immutable logic blocks** and **artefacts**. Your goal is to relocate these blocks into a new structure, removing only literal noise while preserving the full cognitive weight of the original thoughts.

---

## The BTS (Block-Transfer Synthesis) Methodology

### Phase 1: Establish the "Substance Floor"

Before making any changes, establish a quantitative baseline.

1.  **Run `wc` (Word/Byte Count):** Calculate the total size of all source files.
2.  **Record the Floor:** This value is your "Substance Floor."
3.  **The 80% Rule:** The final output must retain at least **80%** of the Substance Floor. If the output falls below this, you have likely performed "banal summarization" and must self-interrupt to restore missing content.

### Phase 2: Identify and Assign Logic Blocks

Do not read to "understand the gist." Read to identify discrete units of value.

1.  **Block Definition:** A "Logic Block" is a paragraph, a dialogue exchange, a set of technical axioms, or a developed metaphor.
2.  **Mapping:** Assign each block to one of your target files/buckets.
3.  **Transfer:** Copy blocks **literally**. Do not rephrase or "simplify" them.

### Phase 3: Surgical De-noising (The Only Permitted Pruning)

Pruning is limited to "connective tissue" and literal duplication.

*   **Allowed to remove:**
    *   Conversational scaffolding (e.g., "Good point," "I agree," "Let's dive into...").
    *   Literal duplicates (e.g., identical copies of the same 12-step list or table).
    *   Empty introductory/closing filler from chat exports.
*   **PROHIBITED from removing:**
    *   Unique metaphors (even if they point to the same concept).
    *   Technical nuance or detailed step-by-step logic.
    *   Long-form dialogues or reflections that serve as "experience generators."

### Phase 4: Final Audit and Justification

Verify the result against the initial floor.

1.  **Final `wc` check:** Compare the final size to the Substance Floor.
2.  **Explicit Justification:** If the reduction is >20%, you must explicitly list what was removed and why (e.g., "Removed 15KB of exact duplicate log data").
3.  **Heuristic Check:** Ask: "Is this a collection of artefacts, or a summary of conclusions?" If it's the latter, revert and re-incorporate the blocks.

## Execution Modes

Based on the size of the source material, use the appropriate execution mode:

1.  **Single-Pass Synthesis (20KB–100KB):**
    *   **Method:** Ingest the entire file in one `read_file` call, identify duplicates in one "muse" turn, and emit the final result in one `write_file` turn.
    *   **Goal:** Efficiency. This range fits comfortably within the active context window, allowing for simultaneous cross-referencing of the floor and the draft.

2.  **Multi-Pass / Tower of Hanoi (>100KB):**
    *   **Method:** Segment the source material into chunks. Process each chunk into "Logic Block" buckets sequentially.
    *   **Goal:** Reliability. Prevents context-overflow and ensures that high-signal artifacts at the beginning of a large file aren't "forgotten" by the time the AI reaches the end.

---

## Summary Workflow

**Quantitative Baseline -> Block Mapping -> Literal Transfer -> Surgical De-noising -> Final Audit.**

Use this skill when moving between conceptual frameworks or cleaning up "messy" analytical directories to ensure that the AI's "System 1" doesn't amputate the "System 2" substance.
