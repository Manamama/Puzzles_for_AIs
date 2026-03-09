# Master Heuristic: Functional Repository Reorganization & Content Synthesis

**Goal:** To systematically reorganize a directory or repository into a high-utility, low-noise toolkit by categorizing content into functional layers, synthesizing redundant information, and renaming for clarity.

---

## 1. Core Principles

*   **Functional Layering**: Files should be organized by their **Interaction Role** (how the AI/user uses them), not just their file type.
*   **Information Density (Synthesis over Storage)**: Favor a single "Master" document over multiple fragmented files. If multiple files share the same core insight, merge them and archive the originals.
*   **Noise Reduction (Provenance Sequestration)**: Keep the "Active" workspace lean by moving historical logs, failed attempts, and legacy drafts to an `archive/` subdirectory.
*   **Descriptive Naming**: Filenames should be functional and technical summaries, not poetic metaphors.

---

## 2. The Functional Interaction Layers

When reorganizing, map every file to one of these five layers:

1.  **The Entry Layer (`root/`)**: The problem statement, main project goal, or core puzzle.
2.  **The Interface Layer (`prompts/`)**: Instructions, personas, or "B-Tips" used to prime the AI before execution.
3.  **The Procedural Layer (`methods/`)**: Atomic heuristics, checklists, and step-by-step algorithms.
4.  **The Diagnostic Layer (`theory/`)**: Root-cause analysis, taxonomies of failure, and theoretical deconstructions of "why" a task is difficult.
5.  **The Historical Layer (`archive/`)**: Redundant drafts, legacy methods, and case studies (logs of past attempts).

---

## 3. Sequential Reorganization Workflow

### Step 1: Mapping & Discovery
*   **Action**: Recursively list the directory.
*   **Thought**: "What is the current 'mess'? Identify clusters of related files."
*   **Tip**: Use `ls -R` or `list_directory` to see the whole board.

### Step 2: Content-Based Renaming
*   **Action**: Read the first 20 lines of each file to identify its **Primary Nature**.
*   **Renaming Rule**: Rename files to reflect their **Functional Category** (e.g., `sunrise_meta_analysis.md` → `theory/mythic_ai_cosmology.md`).
*   **Guide**: If the name is metaphorical (e.g., "Gate Closing"), change it to technical (e.g., "Paradigm Gating").

### Step 3: Synthesis & De-duplication
*   **Action**: Identify files with overlapping content.
*   **Synthesis Rule**: Use the **Critical-Analysis** skill to merge fragmented "Tips" or "Methods" into a single **Master Document**.
*   **Example**: Merge a "Pre-solve Checklist" and a "6-Step Method" into a `master_heuristic.md`.

### Step 4: Migration & Sequestration
*   **Action**: Move files into the Functional Layers defined in Part 2.
*   **Archiving Rule**: Do not delete useful but redundant data. Move it to `archive/methods_legacy/` or `archive/case_studies/`. This preserves the project's "Discovery Chain" without cluttering the "Active" space.

---

## 4. Practical Implementation Tips

1.  **Human-in-the-Loop**: Content-based renaming and synthesis require subjective judgment. Always propose a "Target Index" (A -> B mapping) before executing moves.
2.  **Overestimate Complexity**: When using `sequentialthinking`, set a high `totalThoughts` budget. Reorganization often reveals hidden dependencies or deeper "nested" messes.
3.  **Verify Integrity**: After a merge, read the "Master" document to ensure no unique insights from the original fragments were lost.
4.  **Symbolic Links**: Avoid renaming targets of active symbolic links without updating the links. Mark links for resolution after the physical migration.

---

## 5. Summary Heuristic for AI Agents

> **"Organize for Utility, not Chronology. Synthesize for Density. Rename for Function. Archive for History. Burn Metaphors in Public."**
