# Standard Operating Procedure: 5-Step Project Viability Analysis

**Objective:** To systematically evaluate the functional reality of a software project, distinguishing genuine capability from conceptual frameworks or non-functional facades.

---

### Step 1: Deconstruct the Project's Stated Purpose

*   **Action:** Perform a comprehensive review of all user-facing documentation (`README.md`, `CONTRIBUTING.md`, official wikis, etc.).
*   **Deliverable:** A concise summary of the project's explicit goals, its intended audience, and its core value proposition.
*   **Key Metrics:**
    *   **Clarity of purpose:** Is the goal well-defined?
    *   **Scope:** Is the project's scope ambitious, realistic, or trivial?
    *   **Target User:** Is it a tool for developers, end-users, or automated agents?

---

### Step 2: Isolate and Analyze the Core Functional Logic

*   **Action:** Conduct a targeted source code review to identify the primary "engine" of the project—the specific modules, functions, or classes that execute the core value proposition identified in Step 1.
*   **Deliverable:** A code-backed assessment of the core logic's implementation.
*   **Key Metrics:**
    *   **Logic-to-Boilerplate Ratio:** What percentage of the codebase is dedicated to the core function versus setup, configuration, and protocol handling?
    *   **Complexity & Sophistication:** Is the logic sophisticated, a simple algorithm, a wrapper for an external API, or a hardcoded placeholder?
    *   **Dependencies:** Does the core logic rely on powerful external libraries (e.g., ML frameworks, physics engines) or is it self-contained?

---

### Step 3: Simulate and Evaluate the Core Value Proposition

*   **Action:** Perform a mental "dry run" of the project's primary use case from the perspective of its intended user. This simulation will focus on the raw input-to-output transformation of the core logic identified in Step 2, ignoring all superficial naming conventions and technical jargon.
*   **Deliverable:** A qualitative judgment on the practical utility of the project's output.
*   **Key Metrics:**
    *   **Value-Add:** Does the output provide significant, non-obvious value to the user?
    *   **Context-Awareness:** Does the output intelligently reflect the nuances of the input, or is it generic and context-free?
    *   **Heuristic Superiority:** For an AI agent user, is the tool's output superior to the agent's own baseline capabilities?

---

### Step 4: Render a Final Project Classification

*   **Action:** Synthesize the findings from Steps 1-3 into a definitive classification of the project's current state.
*   **Deliverable:** A formal classification with a supporting rationale.
*   **Classification Tiers:**
    *   **Tier 1: Production-Ready / Viable:** The project successfully delivers on its stated purpose with a robust, functional core.
    *   **Tier 2: Viable Prototype:** The project has a solid architectural foundation and is explicitly designed for a more sophisticated core logic to be implemented. The current core is a clear and deliberate placeholder.
    *   **Tier 3: Non-Viable / Conceptual Framework:** The project's core logic is fundamentally trivial, non-functional, or non-existent. Its value is purely conceptual or academic, and it does not perform its stated function in a meaningful way.

---

### Step 5: Propose a Minimal Viable Test Plan

*   **Action:** If the project is classified above Tier 3, design a concise, empirical test plan to verify its functionality.
*   **Deliverable:** A sequence of shell commands and/or code snippets to build, run, and interact with the project.
*   **Plan Components:**
    *   **Setup:** Commands to install dependencies and build the project (e.g., `npm install`, `npm run build`).
    *   **Execution:** Command to run the project as a server or executable.
    *   **Client Interaction:** A specific, well-chosen input to send to the running project (e.g., a `curl` request, a simple client script).
    *   **Success Criteria:** A clear definition of what a successful output would look like versus a failed or trivial output, based on the analysis from Step 3.
