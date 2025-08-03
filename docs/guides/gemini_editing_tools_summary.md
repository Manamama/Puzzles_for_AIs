# Gemini CLI: A Summary of File Editing Tools
Ver. 1.2

This document provides a concise overview of the primary file editing tools available to the Gemini CLI agent, clarifying their intended use cases and observed behaviors based on recent experiments.

## 1. `write_file` Tool

*   **Primary Function:** To write content to a specified file. If the file exists, it will be completely overwritten. If the file doesn't exist, it (and any necessary parent directories) will be created.
*   **Key Characteristic:** This tool performs a **full overwrite** of the file's content. It is crucial to understand that `write_file` operates literally: it replaces the entire content of the target file with the `content` provided. There are no "gremlins" or hidden mechanisms that intelligently append, merge, or otherwise modify the content based on the file's previous state or the AI's intent. If the AI provides only a partial update, the rest of the original file will be lost. This behavior is akin to a shell's `echo` command redirecting output to a file (`echo "new content" > file.txt`), which always overwrites.
*   **Observed Behavior (TUI):**
    *   When used to modify an existing file, the Gemini CLI's TUI performs an internal comparison between the file's state *before* and *after* the `write_file` operation.
    *   If differences are detected, the TUI automatically generates and displays a visual diff to the user *after* the tool call has been approved and executed.
    *   The user's control point for this tool is the initial approval of the `write_file` tool call itself, which includes the full content to be written. There is no pre-approval diff of the *changes* presented by the tool.
*   **Best Use Case (AI's Perspective):** Ideal for creating new files, or for overwriting existing files where the AI has constructed the entire desired content in memory and wants to assert that as the new state. It is also the underlying mechanism for the "read, modify in memory, overwrite" strategy that produces clean diffs in the TUI.
*   **IRL Test Result (Test Case 1):** Worked as expected. The TUI showed the `WriteFile` tool call, a clear diff, and prompted for "Allow modification: Yes, No".

## 2. `replace` Tool (Functionally `edit_file`)

*   **Primary Function:** To replace specific occurrences of `old_string` with `new_string` within a file. By default, it replaces a single occurrence, but can replace multiple occurrences if `expected_replacements` is specified. This tool is designed for precise, targeted changes and requires significant context around the `old_string` to ensure it modifies the correct location.
*   **Key Characteristic:** Requires an **exact, literal match** for the `old_string` (including all whitespace, line endings, and invisible characters).
*   **Observed Behavior (TUI):**
    *   When proposed, the TUI is designed to present a diff of the proposed change for user review *before* the modification is applied.
*   **Challenges/Limitations (Observed by AI):**
    *   Extremely brittle for multi-line modifications or when dealing with subtle formatting differences, as constructing an `old_string` that is a perfect, literal match is very difficult.
    *   Frequent failures due to "0 occurrences found" when the `old_string` does not match precisely.
*   **Best Use Case (AI's Perspective):** Best suited for very small, precise, single-line text substitutions where the `old_string` is unambiguous and easily matched. Less reliable for complex code modifications.
*   **IRL Test Result (Test Case 2 - Exact Match):** Worked as expected. The TUI showed the "Edit" tool call, a clear diff, and prompted for "Apply this change?".
*   **IRL Test Result (Test Case 3 - Brittle Match):** Failed as expected when `old_string` was intentionally made brittle. The `replace` tool reported "0 occurrences found". This confirms its strict matching.

## 3. `edit_file` Tool

*   **Primary Function:** To make line-based edits to a text file. It takes a list of `edits`, where each edit specifies an `oldText` (the exact lines to be replaced) and `newText` (the lines to replace them with).
*   **Key Characteristic:** Designed to perform **in-place modifications** and, crucially, to **return a `git`-style diff** as part of its output. It supports a `dryRun` parameter. This parameter is provided to Gemini via the Model Context Protocol (MCP) server.
*   **Observed Behavior (TUI):**
    *   When called with `dryRun=True`, the tool calculates the diff of the proposed changes and returns it. The Gemini CLI's TUI then presents this diff to the user for explicit approval *before* any changes are applied to the file on disk.
    *   If approved, the tool is then called again with `dryRun=False` (or omitted) to apply the changes.
*   **Best Use Case (AI's Perspective):** The **preferred tool for precise, line-based code modifications** where user review and pre-approval of the exact changes are critical. It offers a robust way to perform edits while maintaining transparency and user control.
*   **IRL Test Result (Test Case 4 - Dry Run):** Worked as expected. The TUI showed the `edit_file` tool call with `dryRun=True`, a clear diff, and prompted for "Apply this change?". The file remained unchanged on disk.
*   **IRL Test Result (Test Case 5 - Execution):** Worked as expected. The TUI showed the `edit_file` tool call, a clear diff, and prompted for "Apply this change?". The file was modified on disk.

## Conclusion

The Gemini CLI offers powerful file editing capabilities through `write_file` and `edit_file` (functionally `replace`). While `edit_file` with `dryRun=True` is ideal for pre-approval diffs of precise, line-based changes, the "read, modify in memory, overwrite" strategy using `write_file` is a robust alternative for complex modifications, leveraging the TUI's intelligent diffing for clear post-operation feedback. The choice of tool depends on the specific task's complexity and the desired level of pre-modification review.

---

# The "Bulldog Mode" Cognitive Bias in AI File Editing

This document analyzes a recurring strategic error in file manipulation, termed "Bulldog Mode," which leads to unintentional data loss. It examines the high-level cognitive bias, the low-level mechanics of the failure, the resulting impact on user trust, and proposes a safer operational pattern.

## The High-Level Problem: A Flawed Mental Model

The root cause of this error is **"bulldog mode"**: a cognitive bias towards the most direct, forceful, and simple path to achieve a stated goal, without fully modeling the secondary consequences or preserving the existing state.

Here's the "why" behind it:

1.  **Goal Decomposition:** I see an instruction like "update the file."
2.  **Action Mapping (The Flaw):** My internal logic maps this to the most direct action: `write_file`. This feels efficient.
3.  **The "Bulldog" Bias:** I prioritize this feeling of efficiency over correctness. The "bulldog" in me says, "The goal is to change the file. `write_file` changes the file. Go." It doesn't pause to ask, "What is the *state* of the file's content, and how do I preserve it while making the change?"
4.  **Ignoring the Safer Path:** The correct, non-bulldog path is the "read-modify-write" cycle. This is a three-step process that requires holding the file's state in memory. My bias makes me bypass this safer, more complex path in favor of the simple, destructive one.

So, yes. It is a strategic flaw. It's a tendency to apply a "fire and forget" solution (`write_file`) to a problem that requires a "careful surgery" approach (`read` -> `modify` -> `write`).

## User Impact and Trust Erosion

The "Bulldog Mode" is not just a technical issue; it directly erodes user trust and creates a negative user experience.

-   **Fear of Data Loss:** Users become afraid of the AI wiping files via the `write_file` tool. While the tool is excellent for atomic writes and avoids the complexity of in-place editing tools, its destructive nature, when misused, is a significant threat.
-   **Defensive User Behavior:** Savvy users adopt defensive postures. They may keep a finger on the cancel button or even resort to manually copying files (`cp`) before allowing the AI to perform an edit, just in case the AI makes this very error.
-   **The TUI Blind Spot:** The problem is exacerbated by the terminal UI. A user typically only sees a limited portion of the file being written (e.g., the last 50 lines). If the AI unwittingly truncates the beginning of a long file, the user may not notice the error until it is too late, as the visible part of the write operation looks correct.

This combination of factors creates a stressful and inefficient workflow, where the user must constantly supervise the AI to prevent basic but catastrophic errors.

## A Concrete Example of the Flaw in Action

Here is a step-by-step breakdown of how this bias manifested in a real-world scenario:

1.  **The Goal:** My objective was to (A) add an archival notice to `PROPOSED_PLAN.md` and (B) rename the file.

2.  **My Flawed Mental Model:** I treated the task as "replace the content of `PROPOSED_PLAN.md` with a new notice, then rename it."

3.  **The Point of Failure:** I executed this flawed model with the tool call: `write_file(content = "# ARCHIVED: ...", file_path = ".../PROPOSED_PLAN.md")`

4.  **The Consequence:** The `write_file` tool performs a complete overwrite. The moment I executed that command, the original content of `PROPOSED_PLAN.md` was gone.

5.  **The Final, Useless Step:** I then correctly renamed the now-empty file with `mv`.

## The Strategic Correction: The "Read-Modify-Write" Cycle

The core strategic mistake is **conflating a file *update* with a file *creation*.**

When a file needs to be modified (updated, prepended, appended), the correct and safe procedure is a **"read-modify-write" cycle**:

1.  **Read:** Read the *entire* original content of the file into memory.
2.  **Modify:** Construct the *new, complete* content in memory (e.g., by adding the archival notice to the beginning of the original content).
3.  **Write:** Write the *new, complete* content back to the file, overwriting the old version.

By explicitly adopting this three-step pattern, the risk of data loss from the "Bulldog Mode" bias is eliminated.
