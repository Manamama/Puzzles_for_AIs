# Gemini CLI Shortcuts

This file lists the keyboard shortcuts available in the Gemini CLI, as found in the project's documentation.

## Command-Line Shortcuts

These shortcuts are entered as commands in the CLI.

| Shortcut | Alternative | Source File |
| :--- | :--- | :--- |
| `/help` | `/?` | `commands.md` |
| `/quit` | `/exit` | `commands.md` |

## Gemini CLI Keyboard Shortcuts

These shortcuts are specific to the Gemini CLI or have behavior defined by it.

| Shortcut | Action | Source File(s) |
| :--- | :--- | :--- |
| `Ctrl+T` | Toggle tool descriptions | `commands.md, index.md` |
| `Shift+Tab` | Cycle through autocomplete | `index.md` |

---
## Default Bash Keyboard Shortcuts

These are common keyboard shortcuts for the Bash shell, some of which are also used by the Gemini CLI.

### Navigation
| Shortcut | Action |
| :--- | :--- |
| `Ctrl+A` | Move to the beginning of the line. |
| `Ctrl+E` | Move to the end of the line. |
| `Ctrl+F` | Move forward one character. |
| `Ctrl+B` | Move backward one character. |
| `Alt+F` | Move forward one word. |
| `Alt+B` | Move backward one word. |

### Editing
| Shortcut | Action |
| :--- | :--- |
| `Ctrl+D` | Delete the character under the cursor. In Gemini CLI, exits the shell if the line is empty. |
| `Ctrl+H` | Delete the character before the cursor (Backspace). |
| `Ctrl+W` | Cut the word before the cursor. |
| `Ctrl+K` | Cut from the cursor to the end of the line. |
| `Ctrl+U` | Cut from the cursor to the beginning of the line. |
| `Ctrl+Y` | Paste the last cut text. |
| `Alt+T` | Swap the current word with the previous one. |
| `Alt+U` | Uppercase the current word. |
| `Alt+L` | Lowercase the current word. |
| `Alt+C` | Capitalize the current word. |
| `Ctrl+_` | Undo the last command. |

### History
| Shortcut | Action |
| :--- | :--- |
| `Ctrl+P` | Fetch the previous command from history (Up Arrow). |
| `Ctrl+N` | Fetch the next command from history (Down Arrow). |
| `Ctrl+R` | Search history backward. |
| `Tab` | Autocomplete commands and file paths. |

### Process Control
| Shortcut | Action |
| :--- | :--- |
| `Ctrl+C` | Interrupt the current process or exit the CLI. |
| `Ctrl+Z` | Suspend the current CLI process. |
| `Ctrl+L` | Clear the screen. |

---

## Sources

*   [`commands.md`](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md)
*   [`index.md`](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/index.md)


#ver. 1.2
