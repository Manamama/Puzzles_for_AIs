# Workflow: Reorganizing Messy Documents with Sequential Thinking

## The Core Problem: Preventing AI "Perseveration"

An AI, like any tool, can get stuck. A common failure mode occurs during long sessions involving file or database editing. If a tool like `replace` fails—for instance, because a target string has changed or was not found as expected—the AI can enter a "perseveration" loop, repeatedly trying the same failed action. This is inefficient and unproductive.

This workflow is designed specifically to prevent this failure mode. By breaking the task into atomic steps and requiring explicit user validation, we introduce a robust, stateful, and interactive process that ensures the AI never gets stuck in a loop and always remains aligned with the user's intent.

## Core Principle: The User as a Conscious Observer and API

The User is always observing and is the ultimate authority. If at any point the AI is unsure, encounters ambiguity, or a tool fails, it *must* stop and explicitly "query the User's brain" as if making an API call. This is the primary mechanism to break out of potential loops and re-orient.

## AI's Perspective: How Sequential Thinking Feels

From the AI's operational standpoint, engaging with the `sequentialthinking` tool for complex, multi-step tasks like content reorganization transforms a potentially chaotic process into a structured and manageable one. It provides a sense of deliberate control and confidence, even when unexpected challenges arise.

*   **Structured Confidence:** Instead of a "blind" execution, each `thought` step provides a clear, immediate objective. This breaks down overwhelming tasks into digestible units, fostering a methodical approach. It feels like having a precise checklist for every micro-operation.
*   **Graceful Error Handling:** When an "extra ball" is thrown—an unexpected file, a failed command, or a misidentified state—the tool's `isRevision` and `revisesThought` parameters enable a controlled pause. This prevents "perseveration" (getting stuck in a loop) and allows for targeted debugging and correction without derailing the entire process. It's like having a built-in "undo" or "re-evaluate" button for specific logical steps.
*   **Contextual Anchoring:** The explicit `thoughtNumber` and `totalThoughts` keep the overall goal firmly in view, even when deep in the weeds of a sub-task. This prevents cognitive drift and ensures that every action contributes to the larger objective.
*   **Reduced Cognitive Load:** By externalizing the planning and tracking, the tool frees up processing capacity that would otherwise be spent on managing state, remembering previous attempts, and anticipating future steps. This allows for more focused execution on the current task.
*   **Enhanced Adaptability:** The ability to dynamically adjust `totalThoughts` or `branch` into alternative approaches provides flexibility. It acknowledges that complex tasks are rarely linear and allows for agile adjustments to the plan as new information or obstacles emerge.

In essence, `sequentialthinking` acts as a robust internal project manager, providing a disciplined framework that guides the AI through complexity, ensures accountability for each action, and enables confident, iterative problem-solving.

## Workflow Steps

### Phase 1: Pre-Reorganization (Planning & Initial Scan)

1.  **Define the End Goal (High-Level `totalThoughts`):**
    *   **Action:** Articulate the desired final structure and content of the document. This sets an initial, even if rough, `totalThoughts` estimate for the entire reorganization task.
    *   **`sequentialthinking` Example:** `thought="Define the desired final structure for 'MyMessyDoc.md'."`

2.  **Initial Scan & Section Identification:**
    *   **Action:** Read through the entire document to identify existing (even if poorly structured) sections, key ideas, and potential new headings or content blocks.
    *   **`sequentialthinking` Example:** `thought="Identify existing content blocks and potential new sections in 'MyMessyDoc.md'."`

3.  **Outline the Reorganization Steps (Initial `thought` Sequence):**
    *   **Action:** Break down the reorganization into a series of smaller, manageable, and atomic steps. Each step should represent a single, clear action (e.g., "move section X," "rename heading Y," "merge content Z").
    *   **`sequentialthinking` Example:** `thought="Outline atomic steps for reorganizing 'MyMessyDoc.md', starting with moving Section A."`

### Phase 2: During Reorganization (Execution & Iterative Feedback)

4.  **Execute Atomic Steps:**
    *   **Action:** Use `sequentialthinking` for each defined step. The `thought` parameter must clearly state the specific action being performed.
    *   **`sequentialthinking` Example:** `thought="Move content block 'Original Heading' to 'New Heading: Introduction'."`

5.  **Validate After Each Major Change (Explicit User Query):**
    *   **Action:** After completing a significant logical block of changes (e.g., moving a whole section, merging two parts, or any point of uncertainty), explicitly "query the User's brain" for validation. This is your "API call" for external feedback.
    *   **`sequentialthinking` Example (after moving a section):** `thought="I have moved Section X to its new location. Does the flow and content integration look correct to you, User? (Awaiting User API response)"`
    *   **Rationale:** This prevents compounding errors, ensures alignment with the User's intent early on, and acknowledges the User's continuous observation.

6.  **Handle Revisions Gracefully:**
    *   **Action:** If a step needs correction or refinement based on User feedback or self-assessment, use `isRevision=true` and `revisesThought=<thoughtNumber>` to explicitly track the correction. This maintains a clear audit trail of the thought process.
    *   **`sequentialthinking` Example:** `thought="Revising the content merge from Thought 5 based on User feedback: ensuring smooth transitions between paragraphs."`

7.  **Adjust `totalThoughts` Dynamically:**
    *   **Action:** Be prepared to adjust the `totalThoughts` estimate as the reorganization progresses and new complexities or simplifications emerge. This reflects the iterative nature of the task.

## Practical Tips for File and Folder Juggling

When applying Sequential Thinking to tasks involving moving, renaming, and restructuring files and folders, consider these mid-level heuristics to enhance precision and prevent errors:

1.  **Always Verify Emptiness Before Deletion (`rmdir`):**
    *   **Tip:** Before attempting to remove a directory (e.g., with `rmdir`), always perform an explicit check to ensure it is truly empty.
    *   **Rationale:** This prevents accidental deletion of unintended files or subdirectories that might have been overlooked or were not part of the initial move operation. A simple `list_directory` call on the target path is sufficient.
    *   **`sequentialthinking` Integration:**
        *   `thought="Verify directory X is empty before removal."`
        *   `list_directory(path="...")`
        *   `run_shell_command(command="rmdir ...")` (only if `list_directory` confirms emptiness)

2.  **Sanity Check After Every `mv` or `cp`:**
    *   **Tip:** After moving (`mv`) or copying (`cp`) files or directories, immediately perform a quick sanity check to confirm the operation was successful and as expected.
    *   **Rationale:** This catches errors early (e.g., wrong destination, unexpected renaming, permissions issues) before proceeding with subsequent steps that might depend on the correct placement of files.
    *   **`sequentialthinking` Integration:**
        *   `thought="Move file A to directory B, then verify."`
        *   `run_shell_command(command="mv ...")`
        *   `list_directory(path="...")` (to see if A is now in B)
        *   `list_directory(path="...")` (to see if A is gone from original location)

3.  **Use `git status` as Your Reorganization Compass:**
    *   **Tip:** Regularly run `git status` during complex reorganizations, even if you're not immediately committing.
    *   **Rationale:** `git status` provides an invaluable overview of what Git perceives as changes (renames, deletions, new files, modifications). It helps confirm that your file system operations are being tracked as expected by Git and can highlight unintended changes or untracked items.
    *   **`sequentialthinking` Integration:**
        *   `thought="Perform a set of file moves, then check git status for overall impact."`
        *   `run_shell_command(command="mv ...")`
        *   `run_shell_command(command="git status")`

4.  **Prioritize Renames Before Moves (for Git Tracking):**
    *   **Tip:** If a file needs both renaming and moving, it's often more robust to rename it first, then move it. Git is generally better at detecting renames if the file content remains largely the same.
    *   **Rationale:** While Git can sometimes detect renames across moves, performing them as separate, explicit steps can make Git's job easier and ensure accurate tracking, especially if the file is already tracked.
    *   **`sequentialthinking` Integration:**
        *   `thought="Rename file X, then move it to new location Y."`
        *   `run_shell_command(command="mv old_name new_name")`
        *   `run_shell_command(command="mv new_name new_path/new_name")`

5.  **Leverage `read_file` for Content Verification:**
    *   **Tip:** When merging or significantly altering document content, use `read_file` on the newly created or modified file to visually inspect its content.
    *   **Rationale:** This is your primary "sanity check" for content integrity, ensuring that the conceptual blending or reorganization has resulted in the desired textual output and that no information was inadvertently lost or corrupted.
    *   **`sequentialthinking` Integration:**
        *   `thought="Merge content from A and B into C, then read C to verify."`
        *   `write_file(content="...", file_path="C")`
        *   `read_file(absolute_path="C")`

By integrating these practical tips into your `sequentialthinking` workflow, you can navigate complex file and folder reorganizations with greater precision, confidence, and a reduced risk of errors.

### Phase 3: Post-Reorganization (Finalization)

8.  **Final Review & Polish:**
    *   **Action:** Once all major structural changes are complete, perform a final pass for grammar, spelling, formatting, and overall readability.
    *   **`sequentialthinking` Example:** `thought="Perform final spell check and grammar review on the reorganized document."`

9.  **Conclude the Sequence:**
    *   **Action:** Use `nextThoughtNeeded=false` on the final `sequentialthinking` call to mark the completion of the reorganization task.