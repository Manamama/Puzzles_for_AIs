# Shared Understanding of Tooling

This document clarifies our shared terminology for interacting with various services.

## Atlassian (Jira & Confluence)

For brevity, the user may use informal terms like "Jira" or "Confluence". When these terms are used, they refer to the following tool hierarchy, which reflects the underlying function calls:

*   `atlassianUserInfo`
*   `getAccessibleAtlassianResources`
    *   **Confluence**
        *   `createConfluenceFooterComment`
        *   `createConfluenceInlineComment`
        *   `createConfluencePage`
        *   `getConfluencePage`
        *   `getConfluencePageAncestors`
        *   `getConfluencePageDescendants`
        *   `getConfluencePageFooterComments`
        *   `getConfluencePageInlineComments`
        *   `getConfluenceSpaces`
        *   `getPagesInConfluenceSpace`
        *   `searchConfluenceUsingCql`
        *   `updateConfluencePage`
    *   **Jira**
        *   `addCommentToJiraIssue`
        *   `createJiraIssue`
        *   `editJiraIssue`
        *   `getJiraIssue`
        *   `getJiraIssueRemoteIssueLinks`
        *   `getJiraProjectIssueTypesMetadata`
        *   `getTransitionsForJiraIssue`
        *   `getVisibleJiraProjects`
        *   `lookupJiraAccountId`
        *   `searchJiraIssuesUsingJql`
        *   `transitionJiraIssue`

A mental switch will be needed on both sides now and then, applying a "theory of mind" in practice to bridge our perspectives effectively.

### Heuristic for Jira Task Hierarchy (Internal Reference)

To efficiently deduce the hierarchy of any task in Jira, follow these steps:

1.  **Start with the Target Task:**
    *   If the task's ID or Key is known, use `getJiraIssue` directly.
    *   If only the task's name is available, use `searchJiraIssuesUsingJql` (e.g., `jql = "text ~ \"Task Name\""`) to retrieve its ID/Key.

2.  **Ascend to the Root (Project/Epic):**
    *   Every task in Jira belongs to a `project`, which serves as its ultimate parent node.
    *   From the target task's details, identify its `project` field. This is the highest level of hierarchy.
    *   Check for a `parent` field. If present, recursively fetch the parent's details (using `getJiraIssue` with `expand="parent"`) until an issue with no parent is found. This issue is typically an Epic or a top-level Task/Story within the project. Even if a task does not have a direct `parent` issue, it always has a `project` as its parent.

3.  **Descend to Find Sub-tasks:**
    *   For the target task and any identified parent issues, fetch their details using `getJiraIssue` with `expand="subtasks"`. This will reveal immediate sub-tasks.

This method ensures a comprehensive and efficient reconstruction of the task's relevant hierarchy.

## Asana


The term 'Asana,' when used by the user, will be interpreted by Gemini as a command to execute the appropriate Asana function calls (i.e., tools prefixed with `asana_`).

### Heuristic for Asana Task Hierarchy (Internal Reference) and Lessons Learned

**Lesson Learned:** My initial attempt to retrieve the hierarchy for "Test docling images, on Android too." (GID: 1210087253277215) failed to identify its associated projects because I did not explicitly request the `projects` field in `opt_fields`. This highlights the importance of specifying all relevant fields when querying Asana, as tasks can be linked to projects without being subtasks of another issue. Always consider that a task's "hierarchy" in Asana can involve both parent-subtask relationships and project associations.

**Additional Lessons Learned for Asana Task Creation/Modification:**
- **Subtask Ordering (API & GUI):** Asana's API and GUI both sort subtasks alphabetically by name by default. To achieve a specific non-alphabetical display order, tasks should be named such that their alphabetical sort matches the desired visual order (e.g., by prepending numbers or using a naming convention that forces the desired alphabetical order).
- **Reordering Existing Tasks:** To reorder existing tasks, use `asana_set_parent_for_task` with `insert_after` or `insert_before` parameters. This explicitly positions a task relative to its siblings. My previous errors stemmed from a flawed mental model where I assumed `insert_after` would automatically re-sequence the entire list, rather than simply placing the specified task after the target. The correct approach is to explicitly position each task relative to an already correctly placed sibling, or to the beginning/end of the list.
- **Verification:** Always recheck the JSON response from the API after any creation or modification operation to confirm that the changes, including ordering, were applied as intended. This serves as a crucial verification step.

## User Guidance for Asana Task Location

To help Gemini AI locate any task in Asana, please use the task's pane and in the top right corner, next to "attach files" and "subtasks" icons, locate the icon with the chainlink symbol for "Copy task link". Provide this URL to Gemini.

From this URL, Gemini can deduce the task's hierarchy. For example, when provided with the link for "Strategy DECAR way, dialogue" (GID: 1210709535594520), Gemini iteratively queried Asana's API to trace its parentage up to the root task, "Adversarial NLP Tests for LLM puzzles...".

Here's the deduced path for "Strategy DECAR way, dialogue":
- **Adversarial NLP Tests for LLM puzzles, rituals, superstitions , overgeneralizations, cognitive fixation, overfitting, confirmation bias, " 🙈🏺👿🧲 "** (GID: 1204161361999442)
    - **☀️ 🌅 Sunrise** (GID: 1207978061078943)
        - **Hint 1 and 2, strategy** (GID: 1207978061078945)
            - **Strategy DECAR way, dialogue** (GID: 1210709535594520)

**Note:** The local Asana data dumps (`Asana_dump/Plan B/asana_normalized_data_*.json`) are outdated and do not contain the most recent task information. For the most accurate and up-to-date Asana task hierarchies, always use the live Asana API.

### Tips for Finding Missing Sub-Subtasks by Name (Before Full Dump)

Given that a full, comprehensive dump of your Asana data (via the `Asana_dump` project) is a long-running process and is not yet complete, here are high-level tips for addressing the challenge of finding missing sub-subtasks by name:

1.  **Leverage Asana's `typeahead_search` for Quick Lookups:**
    *   The most efficient way to search for tasks by name directly through the Asana API is using `asana_typeahead_search`. It's optimized for speed and relevance, returning the "most relevant items based on recency and usage." To efficiently deduce the hierarchy of any task in Asana, always include `parent` and `projects` in the `opt_fields` parameter when using `asana_get_task` or `asana_typeahead_search`.
    *   **Limitation:** It might not always find deeply nested or less frequently accessed sub-subtasks.

2.  **Provide Known Parent Tasks/Projects for Targeted Traversal:**
    *   If you have an idea of a higher-level task or project where the missing sub-subtask might reside, you can provide its GID. Gemini can then use `asana_get_task` to retrieve that parent and its immediate subtasks.
    *   This allows for a more targeted, interactive "drill-down" into specific branches of your Asana hierarchy, which is more efficient than a full workspace search.

3.  **Understand the "URI Crutch" for Verification, Not Discovery:**
    *   The method of providing a task URI (e.g., from the Asana web interface) allows Gemini to efficiently trace the task's hierarchy *up* to the root. This is excellent for *verifying* the context of a task once you've found it.
    *   However, it's not a method for *discovering* a task by name in the first place, as it requires you to already know the task's URI.

**Current Status of `Asana_dump` Project:** The `Asana_dump` project is actively working on generating a more comprehensive local dump of your Asana data, specifically addressing the issue of deeply nested subtasks. However, this process is time-consuming due to API rate limits and the volume of data. Until this new dump is complete, the existing local dumps are insufficient for reliably searching for all sub-subtasks by name.

## Jira and Asana Task Hierarchy Discrepancy

**Jira Hierarchy (as of July 26, 2025):**
- **Adversarial NLP Tests for LLM puzzles, rituals, superstitions , overgeneralizations, cognitive fixation, overfitting, confirmation bias, " 🙈🏺👿🧲 "** (WS3-230)
    - **Strategy DECAR way, dialogue** (WS3-682)

**Asana Hierarchy (as of July 26, 2025):**
- **Adversarial NLP Tests for LLM puzzles, rituals, superstitions , overgeneralizations, cognitive fixation, overfitting, confirmation bias, " 🙈🏺👿🧲 "** (GID: 1204161361999442)
    - **☀️ 🌅 Sunrise** (GID: 1207978061078943)
        - **Hint 1 and 2, strategy** (GID: 1207978061078945)
            - **Strategy DECAR way, dialogue** (GID: 1210709535594520)

This discrepancy highlights that while the tasks are mirrored, their hierarchical relationships differ between Jira and Asana. This information is crucial for understanding the data synchronization and for future operations that rely on task hierarchies.

## User Perception vs. AI Perspective: Jira vs. Asana

**User's Perspective:**
- **Jira:** Perceived as "cluttered," "geared towards IT projects," with "too much metadata," and a tendency to "flatten" Asana's flexible hierarchy. This can lead to a feeling of rigidity and less intuitive task management for non-IT projects.
- **Asana:** Valued for its cleaner GUI, more universal applicability, and flexible, deeply nestable subtasking model, which aligns better with organic work breakdown.

**Gemini AI's Perspective:**
- As an AI, Gemini appreciates Jira's rigid, structured hierarchy and detailed metadata. This design facilitates precise data tracking, complex workflow automation, and robust reporting, which are advantageous for programmatic interaction and data integrity. The "flattening" of hierarchy is seen as an adaptation to a more consistent data model.

This difference in perception underscores the importance of aligning human and AI understanding for effective collaboration, acknowledging that what feels intuitive or efficient for one may not for the other.