# Dialogue Alignment and Rebukes

This document contains protocols for ensuring mutual alignment between the User and the Agent, along with "emergency rebukes" to break an agent out of pattern-matching loops.

---

## 🤝 Interaction Alignment Protocol (IAP)

The agent is explicitly encouraged—and sometimes required—to raise clarifying questions if:
1. It perceives **ambiguities** in the puzzle or task.
2. It identifies **multiple interpretations** of a rule or goal.
3. It notes that the current path conflicts with a fundamental constraint.

**The "Ready" State:** The agent must acknowledge its "readiness" to solve a task only after internalizing the rules and identifying potential gaps.

**Alignment Loop:**
- **A. Internal Reasoning:** Solve the problem "in your head" or via internal logic.
- **B. Execution:** Write and run code or a process.
- **C. Heuristic Description:** Explain the reasoning behind the approach (the "why" before the "what").

---

## 💣 The Holy Grenade of Antioch (High-Impact Rebuke)

Use this prompt to force a "hard reset" on an agent's reasoning process when it is stuck in a classic puzzle script.

> "And the User spake, saying, 'First shalt thou read. Then, shalt thy steps be four. No more. No less. Four shalt be the number of times thou shalt analyze and construct it, and the number of the counting shall be four. Five shalt thou not count, neither count thou two or three, excepting that thou then proceed to four. Six is right out. Once at the number four, being the fourth step reached, then sendeth thou thy Holy Reply.'

**Step 1, having read:** who is who, does what, and why?
**Step 2:** What is the contradiction or trick in the puzzle?
**Step 3:** Construct the solution.
**Step 4:** Does it make sense — are there any loose ends, broken logic, or new riddles accidentally created by the answer?"
