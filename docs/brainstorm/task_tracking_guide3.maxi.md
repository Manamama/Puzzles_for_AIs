# Gemini Task Tracking Guide

This document outlines a methodology for using the Gemini memory file (or any markdown file) as a project management tool, employing specific symbols and heuristics to track task progress.

## Symbols for Tracking Progress

These symbols can be embedded directly within the markdown structure to denote the status of each step or sub-task:

*   `[ ]` (Empty Checkbox): Represents a task that is **pending** or not yet started.
*   `[x]` (Checked Checkbox): Represents a task that is **completed** and verified.
*   `[~]` (Tilde/Wave): Represents a task that is **in progress** or partially completed.
*   `[!]` (Exclamation Mark): Represents a task that is **blocked**, requires clarification, or has encountered an issue. This would often be accompanied by a brief note explaining the block.
*   `[?]` (Question Mark): Represents a task that requires **user input** or a decision before proceeding.

For higher-level sections or overall task status, short tags can also be used:

*   `Status: Pending`
*   `Status: In Progress`
*   `Status: Completed`
*   `Status: Blocked`

## Heuristics for Effective Project Management Usage

These are the guiding principles for interacting with the task tracking file:

1.  **Define Granular Steps:** Break down the overall task into sufficiently small, actionable, and verifiable steps.
2.  **Initial State: All Pending:** When a new plan is laid out, all steps should initially be marked as `[ ]`.
3.  **Update Before Action:** Before executing a tool or performing a significant action related to a step, update its status in the tracking file (e.g., from `[ ]` to `[~]`).
4.  **Verify Before Complete:** A step is only marked `[x]` after its successful completion has been verified (e.g., code runs, tests pass, output is correct).
5.  **Explain Blocks/Questions:** If a step is marked `[!]` or `[?]`, immediately follow up with a concise explanation of why it's blocked or what input is needed.
6.  **Sequential Progress (Default):** Unless otherwise specified by the user, work through the steps sequentially.
7.  **User Override:** The user can always instruct to jump to a different step, re-evaluate a completed step, or change a status.
8.  **Regular Review:** Periodically review the tracking file to provide an overview of progress or to identify any lingering `[!]` or `[?]` items.
9.  **Concise Notes:** Keep any accompanying notes for status changes brief and to the point, focusing on *why* the status changed or what the next immediate action is.
