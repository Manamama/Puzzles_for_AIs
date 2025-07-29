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
