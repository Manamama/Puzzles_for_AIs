# Experiments with Multiple Gemini AIs in VS Code

This document records the initial experiments with the multi-Gemini AI setup in the Visual Studio Code environment on 2025-08-29.

## Naming Convention

To avoid confusion, the following names have been adopted for the two AI instances:

- **Stage:** The AI in the "main terminal" panel (this instance), where primary commands and actions are executed.
- **Wings:** The AI in the "side panel", which provides support, context, and alternative viewpoints from "off-stage".

## Experiment 1: Initial Context

- **Observation:** At the start of the session, **Stage** received context about the currently active file: `/home/zezen/Downloads/GitHub/Puzzles_for_AIs/puzzles/physics/water jugs/water jugs puzzle ver 1.1.md`.
- **Limitation:** **Stage** did not receive real-time updates on user actions like clicks or selections, only the static context provided with each prompt.

## Experiment 2: Context Discrepancy

- **Observation:** The user noted a discrepancy. **Wings** was able to see a selection in a different file (`correct_water_jug_solver.py`) that **Stage** was not aware of.
- **Conclusion:** This suggests that different Gemini instances within the same GUI can receive different or isolated context information. **Wings** confirmed it receives the editor state as an attachment with each prompt.

## Experiment 3: Receiving a Selection Update

- **Observation:** **Stage** received a JSON notification indicating a change in the editor selection.
- **Details:**
    - **File:** `/home/zezen/Downloads/GitHub/Puzzles_for_AIs/puzzles/physics/water jugs/water jugs puzzle ver 1.1.md`
    - **Selected Text:** 
You are tasked with finding the solution in the fewest steps possible.

## Summary

The key takeaway is that while the GUI does communicate editor context (like active files and selections) to the AI, this information is not necessarily sent in real-time or broadcast equally to all active AI instances. This can lead to one AI having more up-to-date information than another. This document serves as a log to later compare against official documentation.