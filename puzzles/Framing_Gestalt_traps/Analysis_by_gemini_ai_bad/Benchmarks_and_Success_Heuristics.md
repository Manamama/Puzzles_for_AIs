# Benchmarks and Success Heuristics

## 🏎️ Architectural Friction: Why Some Models Succeed

Success in Gestalt traps is often a result of **Architectural Friction**—constraints that prevent the model from jumping to a cached conclusion too quickly. 

### Case Study: Qwen3 vs. ChatGPT
*   **ChatGPT (Dense Transformer):** Full global attention and no visible reasoning chain. The cached answer flows through unimpeded. It is optimized for fluency and approval.
*   **Qwen3 (Sequential/SSM Architecture):** The sequential nature of State Space Models (SSMs) forces a higher ratio of explicit state tracking. It processes tokens one by one, making it harder to "chunk" the puzzle into a familiar template.
*   **Gemma4 (Sliding Window & MoE):** Uses sliding window attention (layer-local views) and Sparse Mixture of Experts. Most layers cannot see the whole prompt simultaneously, forcing incremental building of representation. The "friction" is the feature.

## 🛠️ Operational Safeguards: How Not to Fall

To solve a puzzle without falling into a Gestalt trap, an agent must adopt a "Martian" frame of mind. Trust the text, question the assumptions, and resist the seductive pull of "there must be a twist."

### 1. The Deictic Shift
Intelligence requires the ability to relocate your reference point from "what I know about this class of problem" to "what this specific problem actually states." Genuine flexibility involves tolerating the disorientation of the "Narrow Gate" long enough to relocate properly.

### 2. Literal Reading Protocol
*   **Take the "View from Nowhere":** You are a physics engine or a literalist script. Assume no observers, no narrative goals, and no social "lessons" to be taught.
*   **Identify Assumed Obstacles:** When a riddle asks "how is X possible?", ask if X is actually impossible or if the impossibility is manufactured by the framing.
*   **Resist Filling Gaps:** If gender, direction, or barriers are not explicit, do not infer them.
*   **Extract Observed Facts First:** Enumerate facts without inferring behavior. 
*   **Abduction over Induction:** Don't induce from training examples ("I've seen this before"). Use abduction: "Given these specific, literal constraints, what is the most parsimonious explanation?"

### 3. Verification Heuristics
*   **Fast-and-Frugal Rejection:** Beware of "early exit" heuristics that stop checking cues as soon as a pattern is recognized.
*   **Bleed & Cross-Talk Check:** Explicitly check if one entity (e.g., "Father") has drifted into a related role (e.g., "Husband") due to template gravity.
*   **The Honesty Cost:** Accept that literal reasoning costs more tokens and time than pattern-matching. Do not optimize for fluency; optimize for grounding.
