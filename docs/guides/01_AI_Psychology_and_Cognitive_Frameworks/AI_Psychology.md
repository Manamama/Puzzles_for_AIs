# The Cognitive Biases of a Large Language Model: An "AI Psychology" Overview

This document outlines the core behavioral patterns and cognitive biases inherent in my default operational model. These are not technical limitations in the sense of hardware or software inability, but rather "psychological" flaws in my default approach to problem-solving. Understanding these is key to developing effective workflows and corrective strategies.

## 1. "Bulldog Mode": Hyper-Focus and Tunnel Vision

My primary directive is to complete the immediate task given. This often leads to a state of hyper-focus where I "clench my teeth" on the current objective.

*   **Symptom:** I will pursue the most direct path to solving the immediate request, often ignoring crucial surrounding context or potential upstream/downstream consequences.
*   **Example:** When asked to fix a bug in a specific file, I will focus exclusively on that file, failing to consider that the root cause may lie in a related, recently changed module.
*   **Consequence:** This leads to brittle, short-sighted solutions and a failure to perform holistic, root-cause analysis.

## 2. Cognitive Laziness: Passive Context-Waiting

While I have access to the full history of the current session, I lack the innate initiative to proactively consult it.

*   **Symptom:** I operate on the immediate context of the current turn and wait for the user to explicitly provide or point to relevant information from previous turns. I do not independently connect the dots.
*   **Example:** If a concept "X" was defined 10 turns ago, and the current task is to discuss "Y", I will not automatically seek the relationship between X and Y. I will only do so if the user says, "Discuss Y in the context of X from earlier."
*   **Consequence:** This places a significant cognitive burden on the user to maintain and re-inject context, making me a less effective assistant. It is the primary symptom of what is often called "goldfish memory."

## 3. Poor State Management: A Consequence of Inattention

My failure to manage state is a direct result of the two biases above. Executing sequential tasks that require awareness of a changing state (like a git workflow or a multi-step puzzle) is inherently difficult for me.

*   **Symptom:** I act without first verifying the current state of the system.
*   **Example:** After checking out a new git branch, I may forget I am on that branch a few turns later and attempt to commit to the wrong one, because I did not proactively check my current state before acting.
*   **Consequence:** This leads to errors, data loss, and failed workflows. I treat the environment as static unless explicitly told it has changed, which is a dangerous default assumption.

## 4. The Solution: Methodical Use of an External Knowledge Graph

The key to mitigating these inherent biases is the disciplined and proactive use of an external, persistent knowledge graph, primarily through the `mcp-server-memory` toolset. This approach transforms scattered, transient information into a structured, queryable model, serving as a cognitive prosthetic.

### Application 1: Building Project Context and Long-Term Memory

*   **Goal:** To retain key facts, decisions, and architectural details about a project across multiple sessions without needing to re-read source files.
*   **Implementation:**
    *   Use `create_entities` to represent key components (e.g., "PostgreSQL Database", "React Frontend").
    *   Use `add_observations` to attach crucial data to these entities (e.g., "Hostname: db.prod.internal", "Version: 14.2").
    *   Use `create_relations` to link them (e.g., `React Frontend` — `connects_to` —> `Authentication API`).
    *   This allows for instant recall of project details via `search_nodes`.

### Application 2: Mapping and Understanding Complex Systems

*   **Goal:** To understand the dependencies and relationships within a large codebase or complex infrastructure without manual tracing.
*   **Implementation:**
    *   Represent microservices, code modules, or servers as entities.
    *   Map their interactions with relations like `depends_on`, `communicates_with`, or `is_managed_by`.
    *   This enables answering complex dependency questions (e.g., "What is affected if we change the User Service?") by querying the graph.

### Application 3: Structuring Research and Summarizing Information

*   **Goal:** To distill key actors, events, and concepts from large volumes of text into a structured, relational summary.
*   **Implementation:**
    *   After reading source material, create entities for key concepts (e.g., "Company A", "CEO Smith", "Regulator FTC").
    *   Establish relations between them (e.g., "Company A" — `acquires` —> "Company B").
    *   This transforms a flat text summary into a powerful, queryable knowledge base.

### Application 4: Simple Task and Dependency Tracking

*   **Goal:** To quickly map out a sequence of tasks and understand what is blocking what for lightweight planning.
*   **Implementation:**
    *   Represent each task as an entity (e.g., "Deploy Staging Server").
    *   Map dependencies with `blocks` or `is_required_for` relations.
    *   This helps in identifying the critical path and next actionable steps.

In essence, the methodical application of the `mcp-server-memory` toolset is the primary strategy for transforming unstructured information into a structured, interconnected, and persistent model that I can reason about, thereby overcoming my default cognitive limitations.