# Lessons Learned: Robust Task Tracking with MCP

To ensure accurate and persistent task tracking, especially across sessions, the following practices will be adopted:

1.  **Atomic & Immediate MCP Updates:**
    *   **Pre-action:** Before executing any tool call that modifies the filesystem or represents a significant step, the MCP will be updated to reflect the *intended* action (e.g., "Attempting to create `filename.md`").
    *   **Post-action:** Immediately after a tool call completes (successfully or with an error), the MCP will be updated with the *actual* outcome (e.g., "Successfully created `filename.md`" or "Failed to create file: [error]").

2.  **Leveraging the Knowledge Graph for Richer State:**
    *   Use `create_entities` to define tasks and subtasks explicitly.
    *   Use `create_relations` to establish hierarchical relationships and dependencies (e.g., "has subtask", "depends on", "renamed to", "replaced by"). This allows for a more structured and queryable representation of the project plan.

3.  **Standardized Status Observations:**
    *   Consistently use a predefined set of status observations (e.g., "Status: Not Started", "Status: In Progress", "Status: Completed", "Status: Skipped", "Status: Blocked").

4.  **Regular Self-Audits and User Synchronization:**
    *   Upon resuming a session or when there is any ambiguity, proactively perform a quick audit by comparing the MCP's recorded state with the actual filesystem (using `glob` and `read_file`).
    *   Explicitly confirm the state with the user when necessary.
    *   For critical task completions or deprecations, explicitly state the action and its impact, update the MCP, and then seek user confirmation.

5.  **Handling Renames and Synonyms:**
    *   When a file is identified as a rename or synonym, create a specific relation in the MCP (e.g., "old_file.md is a synonym of new_file.md") and update the status of the original task to "Skipped" or "Replaced" as appropriate.
