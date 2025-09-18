## Interactive Troubleshooting Mind Map (Template for Live Canvas)

*(Use this in ChatGPT Canvas. Table is fully editable. User can tick boxes, update likelihood, add notes; AI observes in next turn and suggests next focus.)*

| Node ID | Node (Possible Cause) | Subsystem / Area    | Likelihood (0-10) | Status | Test / Evidence                 | Notes                                        |
| ------- | --------------------- | ------------------- | ----------------- | ------ | ------------------------------- | -------------------------------------------- |
| 1       |                       |                     |                   |        |                                 |                                              |
| 2       |                       |                     |                   |        |                                 |                                              |
| 3       |                       |                     |                   |        |                                 |                                              |
| 4       |                       |                     |                   |        |                                 |                                              |
| 5       |                       |                     |                   |        |                                 |                                              |
| 6       |                       |                     |                   |        |                                 |                                              |

### **Legend / How It Works**

- **Node ID:** unique reference for discussion and tracking.
- **Node (Possible Cause):** short description of plausible cause or failure mode.
- **Subsystem / Area:** the component, package, or subsystem affected.
- **Likelihood (0-10):** AI initially proposes; User adjusts based on intuition/evidence.
- **Status:**  
  - ✅ Confirmed issue  
  - ⚠️ Possible / under investigation  
  - ❌ Ruled out  
  - ? Unknown / untested  
- **Test / Evidence:** commands, checks, or observations to confirm/refute the node.
- **Notes:** short reasoning, additional context, warnings, or unexpected behaviors.

### **Usage Instructions**

1. **Initialize nodes:** AI proposes plausible causes; User immediately marks known non-issues (❌) or adjusts likelihood.  
2. **Run tests:** User executes commands/tests in `Test / Evidence`.  
3. **Update table:** Adjust likelihood, tick status, add notes.  
4. **Iterate:** AI suggests next high-likelihood node to check based on updates.  
5. **Canvas advantage:** Each edit is live. User and AI see changes turn by turn; weights shift dynamically, avoiding local minima.  

*(Optional fun/anchor: add surreal reminder or “blue elephants on a string” to make critical nodes hard to miss.)*


