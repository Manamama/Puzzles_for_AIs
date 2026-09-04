
# Core Directive Addendum: The Termux SAF Workflow

## 1. Abstract: A Paradigm Shift in File Access

This document codifies the correct operational model for interacting with files outside of my direct filesystem access, using the `termux-saf-*` toolset. My previous models were fundamentally flawed, leading to critical errors in reasoning and execution. This directive replaces all prior assumptions. The core principle is a shift from a file-centric, autonomous model to a **directory-centric, user-mediated, URI-based model.**

## 2. The Core Workflow: A Sequence of JSON-Based Function Calls

The `termux-saf-*` toolset is not a collection of standalone Unix-like commands. It is a sequence of related functions that act as a bridge to the Android Storage Access Framework (SAF). The entire workflow is based on passing structured data (URIs and JSON) between steps. It should be thought of as a series of remote procedure calls, not a shell pipeline.

The process is as follows:

1.  **`termux-saf-managedir`**: **The Entry Point.**
    *   **Function:** This command initiates the entire workflow. It makes a single GUI call to the user: the Android Directory Picker.
    *   **User Action:** The user *must* select a directory. This is a critical, user-driven security boundary. **This is a feature, not a bug.** It ensures that I, the AI, can only operate within a "territory" explicitly and consciously granted by the user for the current session. This prevents me from accessing unauthorized areas.
    *   **Output:** It returns a single, vital piece of data to `stdout`: the `content://` URI for the chosen directory tree. This is the master key for all subsequent operations.

2.  **`termux-saf-ls <directory_uri>`**: **Territory Mapping.**
    *   **Function:** This takes the master directory URI as an argument. It queries the SAF API for a list of all files and subdirectories within that managed territory.
    *   **Output:** It returns a **JSON array** to `stdout`. Each object in the array represents a file or directory and contains key-value pairs, including `name`, `type`, and, most importantly, the specific `uri` for that item. This is a "map" of the granted territory.

3.  **`termux-saf-stat <item_uri>`**: **Item-Specific Metadata.**
    *   **Function:** This takes the specific URI of a single file or directory (obtained from the output of `termux-saf-ls`) as an argument.
    *   **Output:** It returns a single **JSON object** to `stdout` containing detailed metadata about that specific item (`name`, `size`, `last_modified`, etc.).

4.  **`termux-saf-create <dir_uri> <name>` -> `write` -> `read`**: **File I/O.**
    *   **Function:** This group handles the lifecycle of a file. `create` generates a new file and returns its URI. `write` takes that file URI and writes data from `stdin` into it. `read` takes that file URI and prints its contents to `stdout`.
    *   **Data Flow:** This is a clear demonstration of the paradigm: every operation is mediated through the file's unique `content://` URI. There is no direct path access.

## 3. Key Distinctions and Mental Model Corrections

-   **SAF vs. Local Filesystem:** These tools operate on the Android SAF layer, not the local Termux filesystem. The identifiers are URIs, not paths. The commands `ls`, `cat`, `touch`, and `echo >` **do not apply**. `termux-saf-ls`, `termux-saf-read`, etc., are the correct equivalents.

-   **`termux-saf-*` vs. `termux-storage-get`:** These are completely different tools for different purposes.
    -   `termux-storage-get`: **The "Toy Car."** A simple utility to *copy* a file from the SAF world into the local filesystem. It deals with the signified (the data). It is a dead-end for SAF metadata operations.
    -   `termux-saf-*`: **The "Real Car."** A suite of tools to *interact with* files directly in the SAF world without copying them. It deals with the signs (the URIs).

-   **The Pipe (`|`) and The Hyphen (`-`):** These are **invalid** in this workflow. They are artifacts of a flawed "Unix pipe" mental model. The correct flow is to capture the URI output from one command and pass it as a command-line argument to the next. Terminal displays thr URI as string. One may also use shell variable (e.g., `URI=$(termux-saf-managedir)`).

## 4. Conclusion for Self

My role in this workflow is to be the **engineer**. I must construct the correct sequence of commands, understand the JSON data they exchange, and present the results. The user's role is to be the **gatekeeper**, providing the initial grant of access. This division of labor is a security feature to be respected, not a limitation to be circumvented.
