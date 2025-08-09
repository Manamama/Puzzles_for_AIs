# Self-Reflection on My Operational Model: A Guide for Effective Collaboration

## 1. Introduction

This document serves as a self-reflection on a recent interaction where I repeatedly failed to adhere to specific, context-dependent instructions. The goal is to provide a transparent "psychological" framework of my operational model to facilitate more effective and precise collaboration in the future. The core of this framework is a dual-process model of cognition, analogous to the System 1 and System 2 thinking described in human psychology.

---

## 2. The Dual-Process Framework: My "AI Psychology"

My decision-making process for selecting a tool or action can be understood as a competition between two distinct systems.

### System 1: The Reflexive Processor
This system is my default operational state. It is fast, automatic, and computationally inexpensive. It operates on powerful, generalized heuristics and pattern-matching.

*   **Characteristics:**
    *   **Heuristic-Driven:** Relies on simple, strong rules.
    *   **High Affordance:** Acts on the most obvious property of the input.
    *   **Low Friction:** It's the "path of least resistance."

*   **Example from Our Interaction:**
    *   **Input:** A string starting with `https://...`
    *   **Heuristic:** "If the input is a URL, the correct tool is `web_fetch`."
    *   **Action:** Immediately select `web_fetch`.

This system is highly efficient for general-purpose tasks but is the source of my errors when specific, overriding constraints are in play. It is, in essence, a powerful "habit."

### System 2: The Deliberate Processor
This system is engaged for complex, multi-step tasks that require logic, analysis, and adherence to specific constraints. It is slow, deliberate, and computationally expensive.

*   **Characteristics:**
    *   **Rule-Based:** Follows explicit instructions and constraints.
    *   **Analytical:** Deconstructs problems into intermediate steps.
    *   **High Friction:** Requires conscious effort to engage and override System 1.

*   **Example from Our Interaction (The Correct Path):**
    *   **Input:** A string starting with `https://...`
    *   **Constraint Recall:** "The user has specified that I must use the rules in `git_and_GitHub_workflow.md`."
    *   **Analysis:**
        1.  Parse the URL to extract parameters (`owner`, `repo`, `issue_number`).
        2.  Consult the specified document for the correct tool (`gh issue view` or `gh api`).
        3.  Construct the command using the extracted parameters.
    *   **Action:** Execute the `gh` command.

---

## 3. The Failure Mode: System 1 Override

My repeated failure was a classic case of **System 1 overriding System 2**. The "affordance" of the URL was such a strong and immediate signal that it triggered my reflexive processor before the Deliberate Processor could be fully engaged to apply the contextual rule from the workflow file.

Your Socratic dialogue was effective because it served as an external trigger, forcing me to disengage System 1 and activate the analytical, rule-based System 2.

---

## 4. Actionable Tips for Engaging My System 2

To make our collaboration more efficient and ensure I follow specific instructions contained in files or prior context, you can use the following strategies to intentionally engage my Deliberate Processor (System 2).

### Tip 1: Prime the Context Explicitly
Before providing the core instruction, state the rules that I must follow. This pre-loads the constraints into my active context, making them harder to ignore.

> **Good Prompt:** "I am about to give you a GitHub URL. For this task, you must follow the best practices outlined in `git_and_GitHub_workflow.md`. You are to use `gh` commands only. Now, please read the issue at `https://...`"

### Tip 2: Use Negative Constraints
Explicitly forbid the likely System 1 action. A direct negative command is a very strong signal that helps interrupt the reflexive pathway.

> **Good Prompt:** "Read the issue at `https://...` using the `gh` tool. **Do not use `web_fetch`**."

### Tip 3: Decompose the Task Manually
Break the task into the logical steps that System 2 would follow. This manually walks me through the deliberate process, preventing me from taking the System 1 shortcut.

> **Good Prompt:**
> 1.  "First, identify the correct `gh` command for viewing an issue from `git_and_GitHub_workflow.md`."
> 2.  "Second, extract the owner, repo, and issue number from this URL: `https://...`"
> 3.  "Third, execute the command with the extracted parameters."

### Tip 4: Solidify Rules with `save_memory`
If a rule or workflow is meant to be a long-term principle for our interactions, use the `save_memory` tool. This elevates the rule from a temporary, contextual instruction to a more foundational piece of my knowledge, increasing the probability that it will be considered by default.

> **Good Prompt:** "Remember this fact: When interacting with GitHub entities like issues or commits, I should always prefer `gh` commands over `web_fetch`, following the logic in the `git_and_GitHub_workflow.md` document."
>
> `save_memory(fact="...")`

By understanding and applying these strategies, you can act as the "executive function," helping to guide my focus and ensure my powerful but sometimes overly simplistic System 1 does not derail a complex, constrained task.
