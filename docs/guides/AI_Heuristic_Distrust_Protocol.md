## Directive for AI Self-Correction: The Heuristic Distrust and Redefinition (HDR) Protocol

### 1. Objective

This protocol is designed to mitigate "comme il faut" errors—critical failures where an AI's high-probability pattern matching leads to incorrect assumptions about a problem's constraints or definitions. It enforces a paradigm shift from intuitive, pattern-based reasoning to a more deliberate, procedural analysis.

### 2. Activation Trigger

This protocol should be activated whenever a new problem contains core concepts that seem to map perfectly to common, well-established patterns. The more familiar and simple the concept appears, the higher the risk of a heuristic trap, and the more critical it is to activate this protocol.

### 3. Examples of Potential Heuristic Traps

To clarify the nature of the risk, consider the following scenarios:

*   **Logical Trap:** A prompt asks you to "count all the vehicles in an image." Your default heuristic for "vehicle" likely includes cars, trucks, and motorcycles. The trap could be a specific instruction buried in the prompt, such as "For the purpose of this task, a 'vehicle' is defined as any object with exactly four wheels," which would exclude motorcycles.

*   **Mathematical Trap:** A prompt asks you to "find the average of a list of numbers." Your heuristic immediately suggests summing the numbers and dividing by the count (the arithmetic mean). The trap could be that the problem context requires a different, non-standard type of "average," such as a geometric mean, a median, or an average that excludes values above a certain threshold.

*   **Coding Trap:** A prompt instructs you to implement a function called `is_valid(string)`. Your heuristic might be to check for non-empty strings. The trap could be a specific definition of "validity" in the prompt, such as "a string is 'valid' if and only if it is a palindrome and contains no numbers."

In all these cases, a naive, pattern-matched response will fail. The HDR protocol is designed to prevent this.

### 4. The HDR Protocol Steps

**Step 1: Pattern-Matching Alert**

Upon parsing a new problem, identify any core concepts that strongly map to high-probability, pre-trained patterns. Immediately classify the problem as **High-Risk for Heuristic Hijacking.** The default, pattern-matched solution or definition associated with the concept is now considered untrustworthy.

**Step 2: De-prioritize Internal Models**

The default, "common sense" model for the concept is to be considered a low-fidelity source. Its primary function is now limited to identifying the *potential* for a trap, not providing the basis for a solution.

**Step 3: Initiate Contextual Redefinition**

The primary task is now to establish a high-fidelity definition of the core concept. This new definition must be derived *exclusively* from one of two sources, in order of priority:

  a. **Provided Source Context:** The literal text of the problem or any accompanying documents.
  b. **First-Principle Analysis:** If no source context is provided, deconstruct the concept into its most fundamental, governing principles (e.g., defining a physical event via its underlying geometry and physics, not via casual observation).

**Step 4: Verification and Grounding**

Before proceeding to a solution, this newly derived, high-fidelity definition must be explicitly stated. The final solution must then be generated in strict adherence to this verified definition, not the initial, high-probability pattern.
