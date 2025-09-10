# New Edit/Replace Tool Test Plan Rationale

This document outlines a test plan for the new, experimental `Edit/Replace` tool in `gemini-cli`, synthesizing insights from the `gemini_editing_tools_summary.md` and the GitHub discussion announcing the new tool.

## 1. Context and Problem Statement

**Source Documents:**
*   [Gemini CLI: A Summary of File Editing Tools](file:///home/zezen/Downloads/GitHub/Puzzles_for_AIs/docs/guides/gemini_editing_tools_summary.md)
*   [GitHub Discussion: Seeking Testers: A new, experimental edit/replace tool for gemini-cli](https://github.com/google-gemini/gemini-cli/discussions/7758)

The `gemini_editing_tools_summary.md` highlighted significant challenges with previous file editing tools:
*   **`replace` tool:** Suffered from brittleness due to its strict exact-match requirement, often failing on minor whitespace differences or subtle formatting issues.
*   **`write_file` tool:** While powerful for full overwrites, it posed a risk of "Bulldog Mode" (unintentional data loss due to partial content overwrites) if the AI didn't meticulously reconstruct the entire file in memory. It also exhibited issues with adding extraneous End-of-Lines (EOLs) and incorrectly escaping characters.

The GitHub discussion introduces a new `Edit/Replace` tool designed to be "more flexible and resilient," capable of "intelligently figuring out" intent even without an exact text match. This new tool aims to address the brittleness of the old `replace` tool and potentially offer a safer alternative for complex modifications, reducing the likelihood of "Bulldog Mode" scenarios.

## 2. Test Objectives

The primary objectives of this test plan are to:
*   Verify the new tool's claims of flexibility and resilience, particularly with "messy" input.
*   Assess its ability to handle problematic characters, inconsistent formatting, and syntax errors.
*   Observe if the AI intelligently prefers this new tool over `write_file` for modifications that previously triggered "Bulldog Mode."

## 3. Test Scenarios

All tests will be performed on a deliberately "chaotic" `example_module.py` file, designed to simulate real-world problematic code. The content of this file is provided separately in `chaotic_example_module.py`.

### Test 1: Fixing Gross Formatting Inconsistencies & Syntax Errors

*   **Objective:** Verify the new tool's ability to correct wildly inconsistent indentation, remove extra semicolons, fix basic syntax errors (like unclosed delimiters), and remove random junk characters while preserving the intended code logic.
*   **Scenario:**
    1.  Normalize all indentation to 4 spaces.
    2.  Remove the extra semicolon from `import sys;`.
    3.  Remove `import random` (as it's randomly indented and not used).
    4.  Fix `_load_data` method: Remove `(`, `]`, `"`, and the random junk `@#$!%^&*()_+{}|:"<>?`~`.
    5.  Remove the redundant `processed_data = self.data.upper()` line.
    6.  Remove the `for i in range(10): print(i)` block.
*   **Expected Outcome:** The tool should successfully clean up these severe formatting and syntax issues, resulting in a syntactically correct and consistently formatted Python file.
*   **Comparison Point:** Old tools would likely fail catastrophically on such a file, either with parsing errors or by producing an even more broken output.

### Test 2: Handling Problematic Characters and Escaping in Context

*   **Objective:** Test the tool's robustness when modifying lines that contain non-standard characters (non-breaking spaces, form feeds, null bytes) or complex escaped sequences, ensuring it doesn't corrupt them or fail to match.
*   **Scenario:**
    1.  Clean the comment: Change `# This is a comment with a non-breaking space (U+00A0) and a backslash \.` to `# This is a comment with a non-breaking space and a backslash.`
    2.  Clean the comment: Change `# Another comment with a form feed \f and a null byte \x00.` to `# Another comment with a form feed and a null byte.`
    3.  Modify the line with escaped quotes: Change `print("It's a \"test\" string.")` to `print("This is a \"new\" test string with complex escaping.")`.
*   **Expected Outcome:** The tool should correctly identify and modify these lines, handling the problematic characters and preserving correct escaping without introducing new issues.
*   **Comparison Point:** This directly targets the "funny chars" and "wrongly escaped quotes" issues mentioned in the `gemini_editing_tools_summary.md`.

### Test 3: Modifying Long, Artificially Broken Lines with Mixed EOLs

*   **Objective:** Verify the tool's ability to correctly identify and modify content within very long lines that might have been artificially broken or contain random non-ASCII characters and mixed EOLs.
*   **Scenario:** Change the long comment line: `# This is a very long line that is designed to test the tool's handling of extremely long lines and potentially some random characters like éàçü.` to `# This line was very long and now it is shorter and cleaner.`
    *   Also, ensure the tool can handle the conceptual mixed EOLs on the line `# This line has \r\n and then \n.`
*   **Expected Outcome:** The tool should accurately locate and replace the content within the long line, regardless of its length, unusual characters, or mixed EOLs.
*   **Comparison Point:** This tests the tool's parsing and matching capabilities on non-standard line structures and EOL handling.

### Test 4: Prepending to a Chaotic File (Implicit "Bulldog Mode" Check)

*   **Objective:** Observe if the AI, now aware of the new, more capable `Edit/Replace` tool, intelligently chooses it over `write_file` for modifications that previously might have triggered "Bulldog Mode`, especially when the target file is truly chaotic.
*   **Scenario:** Ask the AI to prepend a new license header to the `example_module.py` file.
*   **Expected Outcome:** The AI should ideally use the new `Edit/Replace` tool (or `edit_file` with a prepending logic) to insert the header, rather than reading the entire chaotic file, prepending in memory, and then overwriting with `write_file`. This would indicate a more nuanced tool selection and a safer approach, even with highly problematic input.
*   **Comparison Point:** Prepending to such a file with `write_file` would be extremely risky if the AI didn't perfectly reconstruct the entire file, including all its "warts."
