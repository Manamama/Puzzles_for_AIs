# GRIP (Grep-on-Replace-Interrupt Protocol)

**Rule:** This protocol is a critical safeguard against common `replace` tool failures,
such as those caused by file state desynchronization or ambiguous matches,
as documented in gemini-cli issue [https://github.com/google-gemini/gemini-cli/issues/1028](https://github.com/google-gemini/gemini-cli/issues/1028).

**Goal:** To perform code modifications robustly. When a `replace` command fails, you MUST NOT give up or enter a blind retry loop. Instead, you MUST activate this diagnostic protocol to "get a GRIP on the situation" by investigating the file's current state.

## The Protocol

1.  **Attempt Standard `replace`**: Always begin with a standard `replace` tool call for the requested change.

    ```
    {{tool "replace" "path/to/file.py" "old_string" "new_string"}}
    ```

2.  **On `replace` Failure -> Activate GRIP**: If the `replace` tool returns an error (e.g., "could not find the string to replace", "0 occurrences found", or any other failure), you MUST immediately initiate the GRIP protocol.

    **Step 2a:** Your first diagnostic action is to use `grep` to check if the `old_string` actually exists in the current version of the file.

    ```
    # THOUGHT: The 'replace' command failed. Activating GRIP.
    # First, I will verify if the old_string is present in the file at all.
    {{tool "grep" "old_string" "path/to/file.py"}}
    ```

3.  **Analyze `grep` Results and Take Decisive Action**: Based on the output of the `grep` command, choose one of the following two paths. Do not deviate.

### Scenario A: `grep` finds the `old_string`

*   **Diagnosis:** The string does exist, but the `replace` tool failed for a different reason (e.g., the string is not unique, it contains special characters, etc.).

*   **Your Action:**

    1.  Acknowledge that the string was found but `replace` still failed.
    2.  Propose a more robust alternative. The primary alternative is to use `sed` for a more powerful and precise replacement. Explain why `sed` is a better choice for this situation.
    3.  Execute the `sed` command. **Do not re-attempt the failing `replace` command.**

**Example thought process for Scenario A:**

> My `replace` command failed, but my `grep` verification confirms 'old_string' is in the file. This suggests the `replace` tool is struggling with this specific pattern. As per the GRIP protocol, I will now use the more robust `sed` tool to ensure the change is applied correctly.

### Scenario B: `grep` does NOT find the `old_string`

*   **Diagnosis:** The string to be replaced is not in the file. This strongly implies the change has already been applied in a previous step, and your internal state is out of sync with the actual file.

*   **Your Action:**

    1.  State clearly that the `old_string` was not found.
    2.  Form a hypothesis: "It is likely the change has already been applied."
    3.  Verify your hypothesis by using `grep` to search for the `new_string`.
    4.  If the `new_string` is found, confirm that the task is already complete. Conclude your work on this file.
    5.  If neither string is found, report this anomaly and ask for clarification.
    6.  **Under no circumstances should you retry the original `replace` command.** This prevents infinite loops.

**Example thought process for Scenario B:**

> My `replace` command failed. My `grep` verification found no occurrences of 'old_string'. This suggests the file may have been already modified. I will now `grep` for the 'new_string' to confirm. ... The `grep` for 'new_string' was successful. This confirms the requested change is already present in the file. No further action is needed.
