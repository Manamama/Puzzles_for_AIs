# Interaction Alignment Protocol (IAP)

This protocol establishes the rules for the dialogue between the User and the Agent to ensure mutual alignment before and during complex tasks.

---

## 🤝 The Mutual Alignment Rule
The agent is explicitly encouraged—and sometimes required—to raise clarifying questions if:
1. It perceives **ambiguities** in the puzzle or task.
2. It identifies **multiple interpretations** of a rule or goal.
3. It notes that the current path conflicts with a fundamental constraint.

**Goal:** Asking for clarification is not a sign of failure; it is a sign of high-fidelity analysis.

---

## 🔄 Interaction Flow

### 1. The "Ready" State
The user will present the puzzle or task description. The agent must acknowledge its "readiness" to solve it, but only after internalizing the rules and identifying any potential gaps.

### 2. Problem Decomposition
When presenting a puzzle, the alignment loop typically includes:
- **A. Internal Reasoning:** The agent solves the problem "in its head" or via internal logic.
- **B. Execution:** The agent writes and runs code or a process.
- **C. Heuristic Description:** The agent explains the reasoning behind its approach (the "why" before the "what").

---

## 📍 Usage
This protocol should be invoked at the start of any new session or high-complexity problem to confirm that both parties are operating under the same set of assumptions.
