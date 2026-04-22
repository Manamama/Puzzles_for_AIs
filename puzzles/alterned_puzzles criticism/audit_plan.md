# Project Plan: Martian Audit of Altered Riddles



version 1.1 

## Objective

To perform a rigorous logical and structural audit of the `alterned_puzzles_fixed.json` dataset using the **Universal Martian Analysis Protocol (v3.1)**. The goal is to identify "wobbly" or "incoherent" puzzles where the altered constraints conflict with the underlying logical skeleton or rely on unstated physical assumptions.

## Source Artifacts

1. **`alterned_puzzles_fixed.json`**: The primary dataset containing 701 altered riddles. It comes from https://huggingface.co/datasets/marcodsn/altered-riddles 
2. **`logic_traps_for_llms.txt`**: A subset of high-bias "Identity Traps" (System 1 vs. System 2 tests) [? is it ready now]
3. **Martian Protocols**:
   
   *   `Martian AI protocol, short.md`
   
   *   `Martian_Analysis_Protocol_long.md`

## Methodology: The Martian Filter

For each puzzle selected for audit, we will apply the following "Strict Analytical Discipline":

### Phase 1: Structural Filtering (The Inventory)

* **Step 0a: Literal Inventory:** Strip all "Riddle Genre" expectations. What is physically and logically present?
* **Step 0c: Ambiguity Check:** Identify "Ghost Constraints" (Category B assumptions) like infinite space or uniform rate that are not explicitly in the text.
* **Rule 3 Analysis:** Determine if the "Linguistic Costume" (the riddle) matches the "Logical Skeleton" (the answer).

### Phase 2: The Incoherence Detection

We will specifically flag "Not Even Wrong" puzzles that fall into these categories:

* **The Semantic Chimera:** Puzzles that join two unrelated ontological categories (e.g., a letter of the alphabet and a black hole) with a simple "and."
* **The Scalar/Vector Violation:** Puzzles that treat intrinsic physical properties (like mass or weight) as being dependent on direction or intent without a mechanism.
* **The Tautological Collapse:** "Surgeon/Father" style puzzles where the answer is explicitly stated in the premise, making any other answer a textual violation rather than a "trick."

### Phase 3: Documentation and Consequence (Step 6)

* Document the "Logical Autopsy" for the most egregious failures.
* Propose "Improved Martian Versions" (similar to the Ver 4.2 Clothesline puzzle) that are logically airtight.
* Prepare a formal critique for the dataset authors explaining where the AI "reasoning" is actually superior to the "cliché" answer.

## Initial Audit Candidates

* **alt_0478**: The "Atheist Singularity" (E + Density).
* **alt_0551**: The "Directional Hammer" (Heavy/Not Heavy).
* **alt_0677**: The "Chlorophyll-free Cereal" (Botany failure).
* **alt_0715**: The "Steel Nut" (Tautological check).
* **alt_0733**: The "Atheist Priest" (Contradictory role).

---

*Plan drafted by Gemini CLI under Martian AI Heuristics.*
