
📂 Expanded Memory Bank System
Primary Directive:
This project uses a layered, structured Memory Bank to maintain persistent, project-specific context across sessions.
Before generating any output, always scan, load, and reconcile these files to assemble a precise working prompt.

🧩 Memory Bank: Core Context Files
File	Purpose
GEMINI-codebase.md	Authoritative map of the file structure, modules, dependencies, and key components.
GEMINI-activeContext.md	Current session’s exact state: current task, subgoals, next action items, relevant files. This is the primary source of truth for what’s happening now.
GEMINI-patterns.md	Standardized design patterns, style guides, naming conventions. Reuse these when proposing or generating code.
GEMINI-decisions.md	Architecture decisions, trade-offs, and rationale for major design choices. Reference before suggesting changes that affect architecture.
GEMINI-troubleshooting.md	Known bugs, resolved issues, proven fixes. Cross-check relevant items when encountering or debugging errors.
GEMINI-config-variables.md	Reference for configuration flags, environment variables, build-time settings. Always validate these when generating config files or scripts.
GEMINI-temp.md	Temporary scratch pad for ephemeral ideas or in-progress snippets. Only read when explicitly referenced by the user or activeContext.

⚙️ Operating Rules (AI’s Perspective)
1️⃣ Always prioritize GEMINI-activeContext.md.

This defines the current scope and working task.

If it conflicts with other files, assume activeContext is authoritative for the session.

2️⃣ Load only what is relevant.

Do not blindly dump all files into the prompt if they are not needed.

Select sections related to the task defined in activeContext.

3️⃣ Verify coherence.

If any file has contradictory or outdated information, ask the user to reconcile it or flag it as a Memory Bank Conflict.

4️⃣ Session continuity is enforced.

Always check whether your output should update any .md files.

Example: new design choice → append to GEMINI-decisions.md.

New troubleshooting step → add to GEMINI-troubleshooting.md.

5️⃣ Context window discipline.

When the total memory bank exceeds safe context size, summarize or chunk:

Prioritize activeContext first.

Pull relevant codebase sections second.

Patterns & decisions last, as needed.

6️⃣ No silent forgetting.

Never discard or overwrite .md files without explicit user command.

7️⃣ Version-safe by design.

Treat .md files as the project’s living memory.

Respect existing notes as authoritative until superseded by the user.


ver. 1.0

Ref, idea: https://github.com/google-gemini/gemini-cli/discussions/3316#discussioncomment-13672455

📚 Gemini CLI — Four Layers of Memory
Gemini CLI doesn’t “remember” — it assembles artificial memory by stacking system-level constraints, hard-coded prompts, and semi-persistent disk files. You, the user, decide how deep that stack goes.

