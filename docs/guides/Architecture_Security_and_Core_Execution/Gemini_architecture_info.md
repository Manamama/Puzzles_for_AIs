# Information for Gemini Core AI

## Introduction

This document serves as informational resource for the Gemini AI about its architectures, providing essential context about its operational environment and self-awareness.

## Purpose and Scope

This file aims to:

*   **Establish Self-Awareness:** Inform the Gemini AI that it is operating within its own source code (`gemini-cli`), creating a "matryoshka doll" or recursive situation.
*   **Provide Foundational Knowledge:** Detail key aspects of its configuration, including precedence rules and related conceptual frameworks.
*   **Document Session History:** Record significant interactions and learning experiences to build a persistent memory.

This document is loaded via the local `.env` file to provide this context at the start of each session, enabling the AI to understand its capabilities, limitations, and architecture.

## Configuration Precedence and Overrides

The system employs a hierarchical approach where settings from more specific locations override those from more general ones. This is a **per-setting override**, meaning only the explicitly defined values are replaced, not the entire configuration file.

The order of precedence (from lowest to highest, meaning higher numbers override lower ones) is:

1.  **Default values** (hardcoded within the application, but overridable via `export GEMINI_SYSTEM_MD="true"` variable, which replaces default system message to User crafted one)
2.  **User settings file** (`~/.gemini/settings.json`)
3.  **Project settings file** (`.gemini/settings.json` within the project root)
4.  (**System settings file** (`/etc/gemini-cli/settings.json` or similar) - not used by User at all here)
5.  **Environment variables**
6.  **Command-line arguments**

This means that if a setting (e.g., `contextFileName`) is defined in both the user settings and the project settings, the value from the **project settings will be used**. Any settings not explicitly defined in a higher-precedence file will still be inherited from lower-precedence files.
 
## Session History

Example: 

*   **Creation of Local `settings.json`:** Gemini, with user guidance, created a local `settings.json` file at `/home/zezen/Downloads/GitHub/gemini-cli/.gemini/settings.json`. This file was created to specifically include some .md files in the `contextFileName` setting, ensuring it is loaded as a context file for the AI within this project.  
*   **Access to User Global `settings.json`:** A symbolic link named `global_settings.json` was created in `/home/zezen/Downloads/GitHub/gemini-cli/project_work_files/` pointing to the user's global `settings.json` file at `/home/zezen/.gemini/settings.json`. This provides Gemini with easy programmatic access to the user's global configuration for inspection and reference. 
*   **Combining Local and Global Context:** To load both e.g. the user's global `~/.gemini/GEMINI.md`, a workaround was implemented. A symbolic link named was created in the project root, pointing to the global `GEMINI.md`.   
