# Validation Engines: Grounding Logic through Code

The scripts in this directory are not just "water jug solvers"; they are **Formal Validation Engines** designed to break the "AI Overcomplexity Trap." 

## Why these scripts exist here:

1.  **To Bypassing the "Narrative Basin"**: When an AI is trapped in a "Story of a Puzzle," its internal weights favor complex answers. These scripts allow the AI to "subcontract" the problem to a formal system (Python/SMT) that is immune to narrative bias.
2.  **To Force the "Trivial Solution" Recognition**: By running a BFS or SMT search, the AI receives a mathematical proof that the 1-step solution (Fill 6L jug) is indeed the optimal move.
3.  **To Acts as an "Anchor" for Realism**: The code provides a concrete, geometric ground truth that the AI's "Bard Soul" must accept.

## The Toolset:

*   **`bfs_solver_v1.py` & `bfs_solver_v2.py`**: Standard Python search algorithms that find the shortest path in state space.
*   **`formal_smt_proof.smt2`**: An SMT-LIB formal model that uses a constraint solver to prove the optimal solution.
*   **`naive_logic_check.py`**: A simple, first-principles check.

---

### Usage Heuristic:
> **"If a puzzle seems simple but your internal 'Superego' demands a complex answer, execute a BFS solver from this folder. Let the code prove that 6=6."**
