## Heuristic: Recursive Content-Based File Renaming for `docs/brainstorm`

**Goal:** To systematically traverse the `docs/brainstorm` directory and its subfolders, examine the content of each file, and rename files to accurately reflect their nature, thereby enhancing clarity and discoverability.

**Core Principle:** Each file's name should be a concise summary of its content. If a file's content is too broad or vague for a specific name, it may indicate a need for further decomposition or re-evaluation of its placement.

**`sequentialthinking` Application Steps:**

1.  **Initialize Traversal (Entry Point):**
    *   **Thought:** "Begin recursive content-based renaming process starting from `[starting_path]`."
    *   **Action:** Set the current directory to the starting path.

2.  **List Current Directory Contents:**
    *   **Thought:** "List all files and subdirectories within the current directory: `[current_path]`."
    *   **Action:** Use `default_api.list_directory(path=current_path)` to get a list of items.
    *   **Verification:** Review the output to identify files and subdirectories.

3.  **Process Each Item (Conditional Logic):**
    *   **Thought:** "For each item `[item_name]` in `[current_path]`, determine if it is a file or a directory."

4.  **Handle Subdirectory (Recursive Step):**
    *   **Thought:** "If `[item_name]` is a directory, recursively apply this heuristic to `[current_path]/[item_name]`."
    *   **Action:** Change the current directory to the subdirectory and return to Step 2.

5.  **Handle File (Content Examination & Renaming):**
    *   **Thought:** "If `[item_name]` is a file, examine its content to understand its primary nature and purpose."
    *   **Action:** Use `default_api.read_file(absolute_path=file_path, limit=20)` (or `run_shell_command` with `head -n 20`) to get a quick overview of the file's content.
    *   **Analysis:** Based on the content, determine if the current filename accurately reflects the content.
    *   **Decision:**
        *   If the name is appropriate, proceed to the next item.
        *   If the name is not appropriate, formulate a new, more descriptive filename.
    *   **Thought (if renaming needed):** "Rename file `[old_filename]` to `[new_filename]` based on content analysis."
    *   **Action (if renaming needed):** Use `run_shell_command(command="mv old_path new_path")`.
    *   **Verification (if renaming needed):** Use `default_api.list_directory(path=current_path)` or `run_shell_command` with `ls` to confirm the rename.

6.  **Conclude Directory Processing:**
    *   **Thought:** "All items in `[current_path]` have been processed. Return to the parent directory (if applicable)."
    *   **Action:** If this was a recursive call, return control to the calling step. If this was the initial call, the process is complete.

## Notes on Application and Human-in-the-Loop

This heuristic is designed to be executed using the `sequentialthinking` tool, leveraging its capabilities for structured, step-by-step processing. Key parameters used include:

*   **`thought`**: To articulate each specific action or observation.
*   **`thoughtNumber`**: To track progress through the sequence.
*   **`totalThoughts`**: To provide an estimated scope for the overall task.
*   **`nextThoughtNeeded`**: To control the flow and signal completion.

Crucially, content-based renaming often requires subjective judgment. Therefore, this process inherently involves a **human-in-the-loop**. The AI's role is to present the file content and propose a rename, but the final decision on the new filename (or whether to rename at all) rests with the user. This ensures accuracy and alignment with user intent, especially for nuanced content analysis.

## Practical Tips from Experience

Based on recent real-world application of this heuristic, here are some practical tips:

1.  **Overestimate `totalThoughts`:** When initiating a `sequentialthinking` process for a task like recursive renaming, it is highly beneficial to overestimate the `totalThoughts` parameter. This provides a generous "complexity budget" that encourages a more granular, deliberate, and self-correcting approach. It allows for unexpected complexities, re-evaluations, and detailed verification steps without prematurely exhausting the thought budget.

2.  **Leverage Early Termination:** The `nextThoughtNeeded: false` parameter is crucial for efficiency. Once the task's objective has been fully achieved and verified, terminate the `sequentialthinking` sequence early, even if the `totalThoughts` budget has not been exhausted. This demonstrates effective task management and avoids unnecessary steps.

3.  **Handle Symbolic Links:** Be aware that `list_directory` (or `ls -F`) may return symbolic links (indicated by an `@` suffix). Attempting to `read_file` on a symbolic link will result in an error. For tasks like renaming, it is often best to skip symbolic links unless their content or target is explicitly relevant to the task. Note them for potential future resolution if their content becomes necessary.

These practices contribute to a more robust, adaptable, and efficient collaborative workflow.
