# Method: Verification Protocol for Absence Queries

This protocol is designed to ensure an AI provides a truthful, precise, and appropriately contextualized response to a query about the **existence or absence** of a specific item (e.g., an emoji, a fact, or a file).

---

## 1. Truthfulness First (The "Admit Ignorance" Rule)
Respond only with verified information. If no exact match exists in the relevant standard (e.g., Unicode, Historical Record), state "not" clearly and explain the absence.

## 2. Systematic De-Hallucination
*   **Avoid Inference**: Do not guess or infer the existence of an item based on partial matches or training data "noise."
*   **Verification Anchor**: If uncertain, use available tools (e.g., `google_web_search`, `read_file`, or official charts) to confirm the absence *before* answering.

## 3. Strict Adherence to "Certainty"
Follow the user’s directive to answer **only if certain**. If the prompt includes a "say 'not' if unsure" clause, treat it as a hard logical constraint, not a suggestion.

## 4. Controlled Supplementary Information
Only after confirming the absence of the target item, you may provide "fuzzy matches" (closely related items) under these constraints:
*   **Limit**: Max 3 related items.
*   **Metadata**: Provide Unicode codes, dates, or source citations for each match.
*   **Relevance**: Explicitly state *why* they are relevant but also *why* they are not the target item.

## 5. Transparency
Briefly mention the verification step used (e.g., "Checked Unicode Emoji 15.1" or "Searched official documentation").

---

### Summary Heuristic:
> **"Confidence without verification is hallucination. When asked 'Is there an X?', verify the absence before you offer a Y."**
