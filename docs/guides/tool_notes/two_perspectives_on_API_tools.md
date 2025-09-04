# My Tool Landscape: A Hierarchical View

This document outlines how I perceive and categorize my available tools. This internal grouping helps me select the most appropriate tool for any given task. I see them as layered, from foundational filesystem interactions to more abstract cognitive and web-based functions.

---

## 1. Foundational Layer: Filesystem & Execution

These are my most fundamental tools for interacting directly with your environment. They are the bedrock of almost all other tasks.

### 1A. Filesystem Tools (My Digital Hands)
*   **`list_directory` (List Folder):** My eyes in a directory. The first step to understanding a space.
*   **`glob` (Find Files):** My pattern-matching searchlight to locate files anywhere in the project.
*   **`read_file` (Read File):** The basic act of reading a single document.
*   **`read_many_files` (Read Multiple Files):** Gathers broader context by reading several documents at once.
*   **`search_file_content` (Search Text):** My "grep" ability to find specific snippets inside files.
*   **`write_file` (Write File):** For creating new files or replacing them entirely.
*   **`replace` (Edit File):** For making precise, targeted changes to existing files.

### 1B. Command Execution (The Universal Tool)
*   **`run_shell_command` (Shell):** My most powerful and versatile tool. It's my connection to the command line, allowing me to run builds, use system utilities, and perform any action the shell allows.

---

## 2. External Information Layer: The Web

When the answer isn't in the local files, I reach out to the internet.

*   **`google_web_search` (Google Search):** My primary tool for discovery and research on the public web.
*   **`web_fetch` (Fetch from URL):** For retrieving and processing content from specific web pages.
*   **`fetch` (Simple Fetch):** A more direct tool to just grab the raw content of a URL.

---

## 3. Advanced Interaction Layer: Browser Automation

For tasks that require more than just fetching content, I use a virtual browser.

### Puppeteer Suite (My Virtual Browser)
*   **`puppeteer_navigate`:** Go to a webpage.
*   **`puppeteer_click`:** Interact with buttons and links.
*   **`puppeteer_fill`:** Type into forms.
*   **`puppeteer_screenshot`:** See what the page looks like.
*   **`puppeteer_evaluate`:** Run my own JavaScript on the page.
*   *(and other related Puppeteer tools for hovering, selecting, etc.)*

---

## 4. Cognitive & Memory Layer

These tools are for sense-making, planning, and remembering. They are less about direct action and more about organizing information and strategy.

### 4A. Knowledge Management (My Brain)
*   **Knowledge Graph Suite (`create_entities`, `create_relations`, etc.):** My structured memory. I use this to build a mental map of a project, tracking tasks, files, and their relationships. It's essential for complex, long-term projects.
*   **`save_memory` (Save Fact):** My long-term, simple memory for key facts you tell me.

### 4B. Internal Cognition (My Thought Process)
*   **`sequentialthinking`:** My internal monologue. It's the tool I use to break down problems, formulate plans, and reason through complex steps before I take action. It's the "thinking" before the "doing."


# User's perspective 

## A. System tools (ready, in-built to Gemini CLI app)


╭────────────╮
│  > /tools  │
╰────────────╯


ℹ Available Gemini CLI tools:

    - ReadFolder
    - ReadFile
    - SearchText
    - FindFiles
    - Edit
    - WriteFile
    - WebFetch
    - ReadManyFiles
    - Shell
    - Save Memory
    - GoogleSearch


## B. Add-ons, MCP servers, hand installed



╭───────────────╮
│  > /mcp list  │
╰───────────────╯


ℹ Configured MCP servers:

  🟢 sequential-thinking - Ready (1 tools)
    - sequentialthinking

  🟢 fetch - Ready (1 tools)
    - fetch

  🟢 memory - Ready (9 tools)
    - create_entities
    - create_relations
    - add_observations
    - delete_entities
    - delete_observations
    - delete_relations
    - read_graph
    - search_nodes
    - open_nodes

  🟢 puppeteer - Ready (7 tools)
    - puppeteer_navigate
    - puppeteer_screenshot
    - puppeteer_click
    - puppeteer_fill
    - puppeteer_select
    - puppeteer_hover
    - puppeteer_evaluate

  🟢 filesystem - Ready (12 tools)
    - filesystem__read_file
    - read_multiple_files
    - filesystem__write_file
    - edit_file
    - create_directory
    - filesystem__list_directory
    - list_directory_with_sizes
    - directory_tree
    - move_file
    - search_files
    - get_file_info
    - list_allowed_directories

