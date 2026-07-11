# Analysis and Notes for the Spiral Puzzle

This directory contains meta-level analysis, notes, and alternative versions of the spiral puzzle.

## Subdirectories:

- **/ai_coding_patterns/**: Contains discussions and commentary on the common patterns and failure modes observed in AI-generated code for this puzzle.
- **/alternative_puzzles/**: Contains prompts and code for different variations of the spiral puzzle, such as leftward or inward spirals.
- **/visualizations/**: Contains Mermaid diagrams attempting to flowchart the logic of the spiral algorithms.

## Top-Level Documents:

The files at the root of this directory (`PROJECT_PLAN.md`, `ASSUMPTIONS.md`, etc.) document the structured thinking process for approaching the puzzle.

## Key Cognitive Failure Modes Observed

### 1. Algorithmic Completeness (The "Paperclip Maximizer" Connection)
AI models exhibit a strong **completeness bias** when generating code for visual/geometric structures. A standard spiral fills the grid, visiting every cell exactly once. When faced with a sparse or expanding arm spiral (which preserves negative space and terminates early), models experience "epistemic vertigo":
*   **The Coverage Heuristic:** The model assumes that a "correct" spiral must occupy 100% of the grid resources. Leaving whitespace (empty cells) feels like an incomplete iteration, a bug, or an error.
*   **Heuristic Overreach:** This mirrors the classic "Paperclip Maximizer" thought experiment, where an optimization metric (e.g., maximum coverage) is pursued without constraint or aesthetic sensitivity. The model "fixes" the sparse spiral by overwriting the whitespace-preserving bounds to paint the entire grid.

### 2. Narrative Biases in Code Generation
*   **Action Bias (Zero Steps):** Models resist loop designs where zero-step transitions are used for state changes rather than active computation, as they carry the prior that loops must perform work.
*   **Plan vs. Improvisation:** AIs struggle with geometric logic that evaluates itself dynamically at runtime. They default to pre-computing sequences (like direction offset arrays) rather than letting the structure emerge organically.

