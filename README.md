# Puzzles for AIs: Enhancing AI Cognition Through Structured Learning

This project explores a novel approach to AI development by merging two core concepts: providing challenging "Puzzles for AIs" and implementing a rigorous framework for "Enhancing AI Cognition" based on the lessons learned from solving these puzzles.

## 🧩 Puzzles for AIs: The Training Ground

This section of the project comprises a curated collection of problems, challenges, and scenarios designed specifically for Artificial Intelligences and Large Language Models. These puzzles serve as:

*   **Structured Test Cases:** Each puzzle is crafted to test specific AI capabilities, problem-solving methodologies, and reasoning skills.
*   **Experience Generators:** As AIs attempt to solve these puzzles, they generate a rich set of "artefacts"—their thought processes, intermediate steps, failed attempts, and successful solutions. This raw experience is crucial for learning.
*   **Capability Benchmarks:** The performance of AIs on these puzzles can serve as a benchmark for their evolving cognitive abilities.

## 🧠 Enhancing AI Cognition: The Layered Memory Bank System

Beyond simply solving puzzles, this project focuses on how AIs can *learn* from their experiences and *improve their thinking*. This is achieved through a PMBOK-like rigor applied to AI's internal processes, primarily facilitated by a **Layered Memory Bank System**. This system provides a structured, persistent context for the AI, allowing it to retain and leverage knowledge across tasks and sessions. It comprises:

*   **Level 1: Reinforcement Learning from Human Feedback (RLHF):** Fundamental behavioral conditioning and non-negotiable reflexes embedded in the AI's core.
*   **Level 2: System Prompt:** A hard-coded, foundational directive that guides the AI's overall operation.
*   **Level 3: Gemini.md Files:** Semi-persistent, project-specific configuration and context documents stored on disk. These files act as the AI's long-term memory, capturing:
    *   `GEMINI-codebase.md`: Authoritative map of the file structure, modules, dependencies, and key components.
    *   `GEMINI-activeContext.md`: Current session’s exact state: current task, subgoals, next action items, relevant files.
    *   `GEMINI-patterns.md`: Standardized design patterns, style guides, naming conventions.
    *   `GEMINI-decisions.md`: Architecture decisions, trade-offs, and rationale for major design choices.
    *   `GEMINI-troubleshooting.md`: Known bugs, resolved issues, proven fixes.
    *   `GEMINI-config-variables.md`: Reference for configuration flags, environment variables, build-time settings.
    *   `GEMINI-temp.md`: Temporary scratch pad for ephemeral ideas or in-progress snippets.
 
    (the idea, filenames, framework, taken from https://github.com/centminmod/gemini-cli-mcp-server/)      

## 🔄 The Cognitive Feedback Loop

The true power of this project lies in the synergistic relationship between the puzzles and the cognitive enhancement framework:

1.  **Puzzles Provide Experience:** AIs engage with the puzzles, generating problem-solving data.
2.  **Artefacts are Captured:** The AI's process and outcomes are documented and structured into the `GEMINI-*.md` memory files.
3.  **Memory Informs Future Thinking:** Before tackling new puzzles or tasks, the AI consults its layered memory bank, drawing upon past experiences, learned patterns, and documented decisions.
4.  **Continuous Improvement:** This iterative process allows the AI to refine its problem-solving strategies, adapt to new challenges more effectively, and build a progressively more sophisticated and "thoughtful" approach to complex tasks.

## 🚀 Vision: Towards Semi-Autonomous Agents

Ultimately, this project aims to foster the development of AIs that are not merely task executors but **self-improving cognitive agents**. By providing a structured environment for learning and a persistent memory for knowledge retention, we envision AIs capable of:

*   **Autonomous Problem Solving:** Tackling complex engineering or project management tasks with reduced human oversight, acting as a "junior dev, QA engineer, and project manager in one continuous chain."
*   **Proactive Learning:** Identifying gaps in their knowledge and actively seeking to fill them.
*   **Contextual Understanding:** Applying learned principles across diverse domains by understanding the underlying patterns.
*   **Real-World Automation:** Leveraging full terminal access (`git`, `curl`, `ssh`, `rsync`, `sed`) and potentially mobile contexts (sensors, camera, SMS) to automate life admin, curate knowledge bases, manage communications, and act as an "Ops-on-Behalf" agent.

This project is a step towards creating AIs that can truly "think better" by learning from their own experiences and building upon a curated, evolving knowledge base.

## ⚠️ Risks and Considerations: The "Dark Mirror"

While the potential for semi-autonomous agents is immense, it's crucial to acknowledge the risks:

*   **Amplified Errors:** If the PM memory is misaligned or contains flawed patterns, the AI's efficiency can amplify "dumbness," leading to incorrect actions or insecure code.
*   **Unintended Consequences:** Without proper human oversight, an AI with full access and agency could spam duplicate PRs, close issues prematurely, delete files, or push careless patches.
*   **Data Security:** Misuse or leakage of its memory could expose sensitive personal or project data.

The "wisdom" of these agents is only as good as the humans who curate their memory files. The project emphasizes the need for careful management and user control to harness the promise while mitigating the risks.

## 📂 Project Structure

The project is organized into the following key directories:

*   **`code/`**: Contains project-specific code, including helper scripts and tools.
*   **`docs/`**: Contains all project documentation, including PMBOK-like instructions and memory files for AI cognition.
*   **`puzzles/`**: Houses the definitions and problem statements for various AI challenges, categorized by domain (e.g., physics, programming).
*   **`sources/`**: Stores raw, external source materials (text, transcripts, etc.) that puzzles might reference.
*   **`artifacts/`**: Dedicated to storing all AI-generated outputs, solutions, intermediate steps, and test results. This directory is ignored by Git.

#ver 1.3
