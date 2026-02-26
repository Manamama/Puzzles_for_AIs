# Project Documentation

This directory contains all documentation for the Puzzles_for_AIs project, organized into logical categories to enhance discoverability and understanding.

## Structure

*   **`code/` (Top-Level Directory):** Contains all project-specific code, including API usage analysis scripts and CLI log prettifiers.

*   **`docs/` (This Directory):** Houses all documentation.
    *   **`concepts/`:** For foundational, theoretical, or abstract ideas that explain *what* something is or *why* it works (e.g., AI collaboration frameworks, memory systems).
    *   **`brainstorm/`:** A dedicated space for unstructured thoughts, raw ideas, and miscellaneous notes, now organized into subfolders:
    *   `tool_notes/`: Notes related to specific AI tools or platforms.
    *   `project_management/`: Notes related to project management.
    *   `conceptual_notes/`: Notes on conceptual ideas or analogies.
    *   `draft_guides/`: Early drafts or notes for potential guides or scripts.
    *   **`strategy/`:** For high-level strategic documents, visions, and analyses that guide the project's direction (e.g., life assistant vision, implications and risks).
    *   **`guides/`:** For practical, actionable guides, workflows, and best practices (e.g., Git/GitHub workflows, sequential thinking guides, API interaction guides).

## Contents Overview

### Concepts
*   `ai_collaboration_framework.md`: Explores the dual-process model of AI cognition and tips for effective collaboration.
*   `memory_system.md`: Details on how Gemini CLI manages and utilizes its memory.

### Brainstorm
*   Contains miscellaneous notes, ideas, and temporary thoughts, now organized into specific subfolders.

### Strategy
*   `implications_and_risks.md`: Analysis of the implications, strengths, weaknesses, opportunities, and threats of AI acting as a development and life actor.
*   `life_assistant_vision.md`: A comprehensive vision for Gemini CLI as a "Life-Process Orchestrator" and personal assistant.

### Guides
*   `debug_workflow.md`: A `git`-based framework for self-debugging and root cause analysis.
*   `git_and_GitHub_workflow.md`: Best practices for Git and GitHub CLI usage.
*   `google_api_interaction_guide.md`: A comprehensive guide to interacting with various Google APIs using `curl` and Python.
*   `sequential_thinking_workflow.md`: A unified guide to using the `sequentialthinking` tool for content housekeeping and reorganization.


### Guides: Modern Context – 2026 Update

The practical guides in **`docs/guides/`** (e.g. API interaction patterns, tool hierarchies, heuristics, lessons learned, workflow steps) are early, hand-crafted examples of what became the open **Agent Skills** standard in late 2025 / early 2026.

Agent Skills are portable folders containing a `SKILL.md` file (YAML frontmatter + Markdown instructions) plus optional assets (scripts, examples, references). They allow AI agents to load task-specific procedural knowledge **on-demand** (with user consent), avoiding permanent context bloat. Your guides prefigured this pattern almost exactly — detailed procedures, tool mappings, pitfalls, and user guidance — long before the format was formalized.

If you're using a modern agent like **Gemini CLI** (v0.26+), **Claude Code**, **Cursor**, or similar:
- You can convert most of these guides into native skills with minimal changes: wrap the content in a `SKILL.md`, add basic YAML frontmatter (at least `name` and `description`), and drop the folder into:
  - `~/.gemini/skills/` (user-global)
  - `.gemini/skills/` (project-local)
- The agent will auto-discover them and propose activation when relevant (e.g. "Jira hierarchy" or "Asana task location").

**Official resources to modernize / migrate these guides:**
- [Agent Skills home & overview](https://agentskills.io/home)
- [Full SKILL.md specification](https://agentskills.io/specification) – details YAML fields, required/optional elements, and best practices
- [Gemini CLI docs on skills support](https://github.com/google-gemini/gemini-cli) – look in docs/ or recent release notes (added ~Jan 2026); skills are activated via propose + consent flow

No need to rewrite the wheel — your original content is already high-quality and directly portable. If you update any guide, consider adding a note at the top like:

> **2026 Note:** This guide is a proto-version of an **Agent Skill**. See modern format at https://agentskills.io/specification for native integration in Gemini CLI / Claude Code / Cursor.
