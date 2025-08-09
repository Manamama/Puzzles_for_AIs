# A Strategic Guide to Troubleshooting Build and Runtime Issues

ver. 1.0

## Philosophy

This guide outlines a structured, collaborative, and "anti-bulldog" methodology for diagnosing and resolving complex issues in this project. Its purpose is to prevent rushed, surface-level fixes by ensuring a deep, shared understanding of the root cause before any code is changed.

This is a team process involving two key roles:

*   **The User:** Provides high-level direction, context, and crucial corrections. The User guides the strategic path and validates findings.
*   **Gemini:** Performs the detailed analysis, executes commands, and synthesizes information. Gemini handles the tactical execution based on the User's strategy.

---

## The "Middle Path": A 3-Phase Workflow

This workflow is designed to be both efficient and thorough, typically taking 20-25 turns to move from a bug report to a complete and documented remediation plan.

### Phase 1: Context and Internal History

**Goal:** To understand the "what" and "why" of the problem before analyzing any implementation code.

1.  **Initial Report (User):** The User provides the initial bug report or area of investigation.
2.  **Core Documentation Review (Gemini):** Gemini reads `README.md`, `GEMINI.md`, and any domain-specific documents (e.g., `docs/BUILDING.md`) to gather high-level context.
3.  **Internal Issue Search (Gemini):** Gemini searches the project's own GitHub issues for similar reports, error messages, or keywords.
4.  **Formulate Initial Hypothesis (Gemini & User):** Based on the docs and internal history, Gemini proposes an initial, evidence-based hypothesis. The User validates or corrects this hypothesis, setting the direction for the next phase.

### Phase 2: Code-Level Verification

**Goal:** To verify the hypothesis against the primary source of truth (the code) and capture definitive forensic evidence.

5.  **Analyze Build Scripts (Gemini & User):** Gemini reads the relevant build scripts (`CMakeLists.txt`, `setup.py`, etc.). This is the most critical step: **we read the recipe before baking the cake.** The User helps guide the analysis of the logic.
6.  **Refine Hypothesis (Gemini):** Gemini compares the build script's actual logic to the initial hypothesis and presents a refined, verified root cause analysis.
7.  **Execute for Evidence (User & Gemini):** The User gives approval to run the single failing command (`pip install .`, etc.). This is done **only once** with the explicit goal of capturing the exact error log as final evidence, not for frantic debugging.

### Phase 3: Synthesis and Planning

**Goal:** To consolidate all findings into a formal, actionable plan and preserve the knowledge gained.

8.  **Create Formal Analysis (Gemini):** Gemini writes the detailed `BUILD_FAILURE_ANALYSIS.md`, documenting the symptoms, evidence, root cause, and a multi-step remediation plan.
9.  **Review and Refine Plan (User):** The User reviews the analysis and plan, providing critical feedback and corrections.
10. **Update All Project Documentation (Gemini):** Once the plan is approved, Gemini updates all relevant documentation (`GEMINI.md`, `README.md`) to reflect the findings and the new status.
11. **Final Approval (User):** The User gives final approval on the complete and documented plan before any fixes are implemented.

---

By following this structured, collaborative approach, we ensure our solutions are strategic, robust, and well-documented, strengthening the project with every issue we resolve.