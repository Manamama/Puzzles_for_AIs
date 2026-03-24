# Gemini Toolsets: A Conceptual Hierarchy

This document provides a conceptual grouping of all the tools available to the Gemini CLI agent. It distinguishes between the core, built-in tools that are fundamental to the agent's operation, and the specialized, external toolsets provided by MCP (Model Context Protocol) servers.

---

### 1. Core Gemini CLI Tools (Built-in Functions)

These are the fundamental, always-available tools that form the basis of the agent's ability to interact with the local system and the web.

*   **`run_shell_command` (Shell):** Executes arbitrary shell commands, providing direct access to the underlying operating system.
*   **`read_file` (ReadFile):** Reads the content of a single specified file.
*   **`write_file` (WriteFile):** Writes or overwrites the content of a single specified file.
*   **`replace` (Edit):** Performs in-place text replacement within a file.
*   **`list_directory` (ReadFolder):** Lists the contents of a directory.
*   **`read_many_files` (ReadManyFiles):** Reads the content of multiple files at once.
*   **`glob` (FindFiles):** Finds files and directories matching a specific pattern.
*   **`search_file_content` (SearchText):** Searches for text or patterns within files.
*   **`google_web_search` (GoogleSearch):** Performs a web search to gather external information.
*   **`web_fetch` (WebFetch):** Fetches the content of a specific URL.
*   **`save_memory` (Save Memory):** Stores user-specific facts in long-term memory.

---

### 2. Project & Task Management (MCP Toolsets)

These toolsets are designed for structured project management, task tracking, and workflow automation.

*   **Taskmaster (`taskmaster-ai`)**
    *   Provides a comprehensive suite for creating, managing, and tracking tasks within a project (e.g., `initialize_project`, `add_task`, `next_task`, `set_task_status`).
*   **Jira (`mcp-jira_simple`, `atlassian_jira_official_remote`)**
    *   *(Currently Disconnected)* Intended for direct integration with Jira projects.
*   **Asana (`asana_online_often_hangs`)**
    *   *(Currently Disconnected)* Intended for direct integration with Asana projects.

### 3. Code & Version Control (MCP Toolsets)

This toolset allows the agent to interact with code repositories, manage version control, and automate development workflows.

*   **GitHub (`githubCopilot_04`)**
    *   Manages issues, pull requests, files, and workflows directly within GitHub repositories (e.g., `create_issue`, `get_pull_request`, `create_or_update_file`).

### 4. Knowledge & Data Management (MCP Toolsets)

These toolsets provide advanced capabilities for storing, retrieving, and reasoning about structured and unstructured data.

*   **Graph Databases**
    *   **Neo4j Memory (`neo4j-memory`):** Manages a knowledge graph using high-level entity and relation commands.
    *   **Neo4j Cypher (`neo4j-cypher`):** Allows for direct, low-level querying of a Neo4j database using the Cypher query language.
*   **General Memory (`mcp-server-memory`)**
    *   Provides a simpler, general-purpose graph memory system.

### 5. Web & Browser Automation (MCP Toolsets)

These toolsets enable the agent to control a web browser for automation, data extraction, and testing.

*   **High-Level Browser Control (`browsermcp_online_often_bad_to_test_Net`)**
    *   Provides intuitive, high-level commands for browser interaction (e.g., `browser_navigate`, `browser_snapshot`, `browser_click`).
*   **Low-Level Browser Control (`puppeteer_online`)**
    *   Offers fine-grained control over the browser via the Puppeteer library (e.g., `puppeteer_screenshot`, `puppeteer_evaluate`).

### 6. AI & Cognitive Tools (MCP Toolsets)

These are specialized tools that enhance the agent's own reasoning, planning, and knowledge-gathering abilities.

*   **Structured Thinking (`sequential-thinking_experimental`)**
    *   `sequentialthinking`: A tool for breaking down complex problems into a sequence of logical steps.
*   **External Knowledge (`context7`)**
    *   `resolve-library-id`, `get-library-docs`: Fetches real-time, version-specific documentation for software libraries.
*   **Human Interaction (`ask-me_local`)**
    *   Provides tools for asking clarifying questions and requesting decisions from the user (e.g., `ask-one-question`, `choose-next`).

### 7. System, Device & Filesystem (MCP Toolsets)

These toolsets provide interaction with the local operating system, connected devices, and the file system.

*   **Local Filesystem (`filesystem`)**
    *   Provides a robust set of tools for file and directory manipulation, complementing the core built-in file tools (e.g., `directory_tree`, `edit_file`, `move_file`).
*   **Android OS (`android_to_test`)**
    *   *(Currently Disconnected)* Allows for direct control and interaction with a connected Android device.

### 8. Communication & Office Tools (MCP Toolsets)

These toolsets integrate with common productivity and communication platforms.

*   **Document Processing (`mcp-libre-office`)**
    *   Creates, reads, and converts LibreOffice documents (Writer, Calc, etc.).
*   **Contact Management (`google-contacts-server`)**
    *   Manages contacts within a Google account.
*   **Voice & Audio (`voice-mode`)**
    *   Enables voice-based interaction, including text-to-speech and speech-to-text (`converse`).
*   **LinkedIn (`linkedin-mcp`)**
    *   Handles authentication with the LinkedIn platform.

### 9. Specialized APIs (MCP Toolsets)

This category is for tools that provide access to specific, high-value external APIs.

*   **Computational Knowledge (`wolfram-alpha`)**
    *   `wolfram_query`: Solves complex mathematical, scientific, and factual queries using the Wolfram Alpha engine.

---

### 10. Tested MCP Experiences (Limited Access)

During initial testing, only a subset of MCP servers were accessible and functional:

*   **DeepWiki Integration**
    *   Successfully used for querying documentation and repository structure
*   **Sequential Thinking (`sequential-thinking_experimental`)**
    *   Confirmed working with its single tool `sequentialthinking` for breaking down complex problems
*   **Fetch Operations (`mcp_fetch`)**
    *   Successfully tested basic fetch operations
*   **Apify Tools**
    *   Had access to several Apify-related functions though not extensively tested:
        - `mcp_apify_call-actor`
        - `mcp_apify_fetch-actor-details`
        - `mcp_apify_fetch-apify-docs`
        - `mcp_apify_search-actors`
        - `mcp_apify_search-apify-docs`

This represents approximately 5% of the total available MCP capabilities listed above, indicating significant room for expanded functionality through additional server activations and permissions.

# Gemini Toolsets: The real Hierarchy
Same list of "function calls" aka MCPs (Model Context Protocols that show Gemini AI "tools" and their uses automatically)

### 10. First-Hand MCP Testing Experience (September 2025)
During live testing and investigation, I gained deep insights into the MCP architecture and capabilities:

1. **Core Architecture**
   - Standardized framework for AI-tool integration
   - JSON-based communication protocol
   - Supports multiple transport methods (stdio, SSE, HTTP streaming)
   - Secure bidirectional connections between components

2. **Key Components**
   - **MCP Server (Bridge)**
     - Interprets and translates tool calls
     - Manages connections and state
     - Returns formatted responses
   - **MCP Client (AI Interface)**
     - Makes structured JSON requests
     - Processes responses and errors
     - Maintains context across interactions

3. **Active Tool Categories**
   - **DeepWiki**: Documentation and codebase querying
   - **Sequential Thinking**: Problem breakdown and analysis
   - **Fetch**: Web content retrieval
   - **Apify**: External service integration

4. **Technical Implementation**
   - Configuration via `~/.gemini/settings.json`
   - Support for progress/status streaming
   - Environment-based authentication
   - Error handling and recovery

This represents about 5% of the full MCP capability set, but provides critical insights into the system's architecture and potential.

Learn more: https://mcpservers.org/ , https://en.wikipedia.org/wiki/Model_Context_Protocol


MCP defines a standardized framework for integrating AI systems with external data sources and tools.[2] It includes specifications for data ingestion and transformation, contextual metadata tagging, and AI interoperability across different platforms. The protocol also supports secure, bidirectional connections between data sources and AI-powered tools.[6]

MCP enables developers to expose their data via MCP servers or to develop AI applications—referred to as MCP clients—that connect to these servers.[6] Key components of the protocol include a formal protocol specification and software development kits (SDKs), local MCP server support in Claude Desktop applications, and an open-source repository of MCP server implementations.[6]

In practice, the file that has them is here: 
 ~/.gemini/settings.json 
 - Gemini AI can ask User to show it if needed. 


## User installed ones 

Note: Disconnected (0 tools cached) - are the ones below need upgrades to make them work
╭───────────────╮
│  > /mcp list  │
╰───────────────╯
ℹ Configured MCP servers:
 
  🔴 graphiti - Disconnected (0 tools cached)
    No tools or prompts available

  🟢 mcp-libre-office - Ready (14 tools)
    Tools:
    - batch_convert_documents
    - convert_document
    - create_document
    - create_live_editing_session
    - get_document_info
    - get_document_statistics
    - insert_text_at_position
    - merge_text_documents
    - open_document_in_libreoffice
    - read_document_text
    - read_spreadsheet_data
    - refresh_document_in_libreoffice
    - search_documents
    - watch_document_changes

  🟢 linkedin-mcp - Ready (1 tool)
    Tools:
    - authenticate

  🔴 audio-interface - Disconnected (0 tools cached)
    No tools or prompts available

  🟢 ask-me_local - Ready (4 tools, 5 prompts)
    Tools:
    - ask-multiple-choice
    - ask-one-question
    - challenge-hypothesis
    - choose-next

    Prompts:
    - creative-brainstorm
    - expert-consultation
    - human-decision
    - refine-document
    - suggest-follow-up-questions

  🔴 gemini_AI_bis-mcp - Disconnected (0 tools cached)
    No tools or prompts available

  🟢 githubCopilot_04 - Ready (86 tools)
    Tools:
    - add_comment_to_pending_review
    - add_issue_comment
    - add_sub_issue
    - assign_copilot_to_issue
    - cancel_workflow_run
    - create_and_submit_pull_request_review
    - create_branch
    - create_gist
    - create_issue
    - create_or_update_file
    - create_pending_pull_request_review
    - create_pull_request
    - create_pull_request_with_copilot
    - create_repository
    - delete_file
    - delete_pending_pull_request_review
    - delete_workflow_run_logs
    - dismiss_notification
    - download_workflow_run_artifact
    - fork_repository
    - get_code_scanning_alert
    - get_commit
    - get_dependabot_alert
    - get_discussion
    - get_discussion_comments
    - get_file_contents
    - get_issue
    - get_issue_comments
    - get_job_logs
    - get_latest_release
    - get_me
    - get_notification_details
    - get_pull_request
    - get_pull_request_comments
    - get_pull_request_diff
    - get_pull_request_files
    - get_pull_request_reviews
    - get_pull_request_status
    - get_secret_scanning_alert
    - get_tag
    - get_team_members
    - get_teams
    - get_workflow_run
    - get_workflow_run_logs
    - get_workflow_run_usage
    - list_branches
    - list_code_scanning_alerts
    - list_commits
    - list_dependabot_alerts
    - list_discussion_categories
    - list_discussions
    - list_gists
    - list_issue_types
    - list_issues
    - list_notifications
    - list_pull_requests
    - list_releases
    - list_secret_scanning_alerts
    - list_sub_issues
    - githubCopilot_04__list_tags
    - list_workflow_jobs
    - list_workflow_run_artifacts
    - list_workflow_runs
    - list_workflows
    - manage_notification_subscription
    - manage_repository_notification_subscription
    - mark_all_notifications_read
    - merge_pull_request
    - push_files
    - remove_sub_issue
    - reprioritize_sub_issue
    - request_copilot_review
    - rerun_failed_jobs
    - rerun_workflow_run
    - run_workflow
    - search_code
    - search_issues
    - search_orgs
    - search_pull_requests
    - search_repositories
    - search_users
    - submit_pending_pull_request_review
    - update_gist
    - update_issue
    - update_pull_request
    - update_pull_request_branch

  🟢 browsermcp_online_often_bad_to_test_Net - Ready (11 tools)
    Tools:
    - browser_click
    - browser_get_console_logs
    - browser_go_back
    - browser_go_forward
    - browser_hover
    - browser_navigate
    - browser_press_key
    - browser_select_option
    - browser_snapshot
    - browser_type
    - browser_wait

  🟢 sequential-thinking_experimental - Ready (1 tool)
    Tools:
    - sequentialthinking

  🔴 mcp-jira_simple - Disconnected (0 tools cached)
    No tools or prompts available

  🟢 mcp-server-memory - Ready (9 tools)
    Tools:
    - add_observations
    - create_entities
    - create_relations
    - delete_entities
    - delete_observations
    - delete_relations
    - open_nodes
    - read_graph
    - search_nodes

  🟢 taskmaster-ai_not_needed - Ready (36 tools)
    Tools:
    - add_dependency
    - add_subtask
    - add_tag
    - add_task
    - analyze_project_complexity
    - clear_subtasks
    - complexity_report
    - copy_tag
    - delete_tag
    - expand_all
    - expand_task
    - fix_dependencies
    - generate
    - get_task
    - get_tasks
    - initialize_project
    - list_tags
    - models
    - move_task
    - next_task
    - parse_prd
    - remove_dependency
    - remove_subtask
    - remove_task
    - rename_tag
    - research
    - response-language
    - rules
    - scope_down_task
    - scope_up_task
    - set_task_status
    - update
    - update_subtask
    - update_task
    - use_tag
    - validate_dependencies

  🟢 android_to_test - Ready (23 tools)
    Tools:
    - back
    - input_key
    - input_text
    - install_app
    - is_app_installed
    - is_screen_active
    - is_screen_locked
    - launch_app
    - list_app
    - lock_screen
    - long_tap
    - screen_dpi
    - screen_size
    - shell_command
    - swipe_down
    - swipe_left
    - swipe_right
    - swipe_up
    - system_info
    - tap
    - terminate_app
    - uninstall_app
    - unlock_screen

  🟢 mcp_fetch - Ready (1 tool, 1 prompt)
    Tools:
    - fetch

    Prompts:
    - fetch

  🟢 filesystem - Ready (12 tools)
    Tools:
    - create_directory
    - directory_tree
    - edit_file
    - get_file_info
    - list_allowed_directories
    - filesystem__list_directory
    - list_directory_with_sizes
    - move_file
    - filesystem__read_file
    - read_multiple_files
    - search_files
    - filesystem__write_file

  🟢 wolfram-alpha - Ready (1 tool)
    Tools:
    - wolfram_query

  🔴 asana_online_often_hangs - Disconnected (0 tools cached)
    No tools or prompts available

  🟢 puppeteer_online - Ready (7 tools)
    Tools:
    - puppeteer_click
    - puppeteer_evaluate
    - puppeteer_fill
    - puppeteer_hover
    - puppeteer_navigate
    - puppeteer_screenshot
    - puppeteer_select

  🔴 mcp-DB-toolbox_to_test - Disconnected (0 tools cached)
    No tools or prompts available

  🔴 atlassian_jira_official_remote - Disconnected (0 tools cached)
    No tools or prompts available

  🟢 neo4j-cypher - Ready (3 tools)
    Tools:
    - get_neo4j_schema
    - read_neo4j_cypher
    - write_neo4j_cypher

  🟢 neo4j-memory - Ready (9 tools)
    Tools:
    - neo4j-memory__add_observations
    - neo4j-memory__create_entities
    - neo4j-memory__create_relations
    - neo4j-memory__delete_entities
    - neo4j-memory__delete_observations
    - neo4j-memory__delete_relations
    - find_memories_by_name
    - neo4j-memory__read_graph
    - search_memories

  🟢 context7 - Ready (2 tools)
    Tools:
    - get-library-docs
    - resolve-library-id

  🟢 gemini-grounding - Ready (1 tool)
    Tools:
    - google_search

  🔴 google_workspace_mcp - Disconnected (0 tools cached)
    No tools or prompts available

  🔴 mcp_email_reader - Disconnected (0 tools cached)
    No tools or prompts available

  🟢 voice-mode - Ready (22 tools, 3 prompts)
    Tools:
    - check_audio_dependencies
    - check_audio_devices
    - converse
    - download_model
    - get_provider_details
    - kokoro_install
    - kokoro_uninstall
    - list_config_keys
    - list_tts_voices
    - refresh_provider_registry
    - service
    - update_config
    - voice_mode_info
    - voice_registry
    - voice_statistics
    - voice_statistics_export
    - voice_statistics_recent
    - voice_statistics_reset
    - voice_statistics_summary
    - voice_status
    - whisper_install
    - whisper_uninstall

    Prompts:
    - converse
    - kokoro
    - whisper

  🔴 gemini-cli_local - Disconnected (0 tools cached)
    No tools or prompts available

  🟢 google-contacts-server - Ready (9 tools)
    Tools:
    - create_contact
    - delete_contact
    - get_contact
    - get_other_contacts
    - list_contacts
    - list_workspace_users
    - search_contacts
    - search_directory
    - update_contact

  🔴 vespera-scriptorium_often_bad_to_test_Net - Disconnected (0 tools cached)
    No tools or prompts available



## System ones:

╭────────────╮
│  > /tools  │
╰────────────╯


ℹ Available Gemini CLI tools:
 
    - Edit
    - FindFiles
    - GoogleSearch
    - ReadFile
    - ReadFolder
    - ReadManyFiles
    - Save Memory
    - SearchText
    - Shell
    - WebFetch
    - WriteFile

