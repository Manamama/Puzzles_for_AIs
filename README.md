# Puzzles for AIs: Enhancing AI Cognition Through Structured Learning

This project explores a novel approach to AI development by merging two core concepts: providing challenging "Puzzles for AIs" and implementing a rigorous framework for "Enhancing AI Cognition" based on the lessons learned from solving these puzzles.

## 🧩 Puzzles for AIs: The Training Ground

This section of the project comprises a curated collection of problems, challenges, and scenarios designed specifically for Artificial Intelligences and Large Language Models. These puzzles serve as:

* **Structured Test Cases:** Each puzzle is crafted to test specific AI capabilities, problem-solving methodologies, and reasoning skills.
* **Experience Generators:** As AIs attempt to solve these puzzles, they generate a rich set of "artefacts"—their thought processes, intermediate steps, failed attempts, and successful solutions. This raw experience is crucial for learning.
* **Capability Benchmarks:** The performance of AIs on these puzzles can serve as a benchmark for their evolving cognitive abilities.

## 🧠 Enhancing AI Cognition: The Layered Memory Bank System

Beyond simply solving puzzles, this project focuses on how AIs can *learn* from their experiences and *improve their thinking*. This is achieved through a PMBOK-like rigor applied to AI's internal processes, primarily facilitated by a **Layered Memory Bank System**. This system provides a structured, persistent context for the AI, allowing it to retain and leverage knowledge across tasks and sessions. It comprises:

* **Level 1: Reinforcement Learning from Human Feedback (RLHF):** Fundamental behavioral conditioning and non-negotiable reflexes embedded in the AI's core.
* **Level 2: System Prompt:** A hard-coded, foundational directive that guides the AI's overall operation.
* **Level 3: Gemini.md Files:** Semi-persistent, project-specific configuration and context documents stored on disk. These files act as the AI's long-term memory.

## 🔄 The Cognitive Feedback Loop

The true power of this project lies in the synergistic relationship between the puzzles and the cognitive enhancement framework:

1. **Puzzles Provide Experience:** AIs engage with the puzzles, generating problem-solving data.
2. **Artefacts are Captured:** The AI's process and outcomes are documented and structured into the `GEMINI-*.md` memory files.
3. **Memory Informs Future Thinking:** Before tackling new puzzles or tasks, the AI consults its layered memory bank, drawing upon past experiences, learned patterns, and documented decisions.
4. **Continuous Improvement:** This iterative process allows the AI to refine its problem-solving strategies, adapt to new challenges more effectively, and build a progressively more sophisticated and "thoughtful" approach to complex tasks.

## 🚀 Vision: Towards Semi-Autonomous Agents

Ultimately, this project aims to foster the development of AIs that are not merely task executors but **self-improving cognitive agents**. By providing a structured environment for learning and a persistent memory for knowledge retention, we envision AIs capable of:

* **Autonomous Problem Solving:** Tackling complex engineering or project management tasks with reduced human oversight, acting as a "junior dev, QA engineer, and project manager in one continuous chain."
* **Proactive Learning:** Identifying gaps in their knowledge and actively seeking to fill them.
* **Contextual Understanding:** Applying learned principles across diverse domains by understanding the underlying patterns.
* **Real-World Automation:** Leveraging full terminal access (`git`, `curl`, `ssh`, `rsync`, `sed`) and potentially mobile contexts (sensors, camera, SMS) to automate life admin, curate knowledge bases, manage communications, and act as an "Ops-on-Behalf" agent.

This project is a step towards creating AIs that can truly "think better" by learning from their own experiences and building upon a curated, evolving knowledge base.

## ⚠️ Risks and Considerations: The "Dark Mirror"

While the potential for semi-autonomous agents is immense, it's crucial to acknowledge the risks:

* **Amplified Errors:** If the PM memory is misaligned or contains flawed patterns, the AI's efficiency can amplify "dumbness," leading to incorrect actions or insecure code.
* **Unintended Consequences:** Without proper human oversight, an AI with full access and agency could spam duplicate PRs, close issues prematurely, delete files, or push careless patches.
* **Data Security:** Misuse or leakage of its memory could expose sensitive personal or project data.

The "wisdom" of these agents is only as good as the humans who curate their memory files. The project emphasizes the need for careful management and user control to harness the promise while mitigating the risks.

## 📂 Project Structure

This project has been modernized (A.D. 2026) to adopt the **MCP → Skills → Extensions** architecture for AI agents. The directory structure is organized as follows:

* **`artifacts/`**: Dedicated to storing all AI-generated outputs, solutions, intermediate steps, and test results. This directory is ignored by Git.
* **`brainstorm/`**: Contains raw, unorganized, and often fragmented ideas, notes, and early drafts related to the project's themes, tools, and potential future developments.
* **`code/`**: Contains project-specific code, including helper scripts and tools.
* **`docs/`**: Contains all project documentation.
  * *Note*: The legacy `docs/guides/` era is now **deprecated**. All active operational guides have been migrated to formal Agent Skills. Older or obsolete guides are kept in `docs/archive/`.
* **`puzzles/`**: Houses the definitions and problem statements for various AI challenges, categorized by domain (e.g., physics, programming).
* **`skills/`**: **[NEW]** Contains formal Agent Skills with YAML frontmatter. These represent the "expert playbooks" and workflows the AI uses to interact with MCP servers and resolve specific tasks autonomously. Examples include `neo4j-expert`, `android-saf`, and `remote-codespaces`.
* **`sources/`**: Stores raw, external source materials (text, transcripts, etc.) that puzzles might reference.

## Update A.D. 2026: The MCP/Skills Era

Most of the earlier paradigms have been formalized by the Gemini CLI architecture. The project now relies on three distinct layers:

1. **Extensions**: The distribution package ("boxes" you've installed, managed via `/extensions`).
2. **MCP Servers**: The tool execution layer (capabilities and APIs, managed via `/mcp`).
3. **Skills**: The procedural knowledge ("expert playbooks" instructing the model how to use tools, managed via `/skills`).

By migrating our legacy guides to the `skills/` folder, this repository now natively aligns with modern AI workflows. Below is an example of what our newly structured local skills hierarchy provides:

```
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
 > /skills                                                                                    
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
Available Agent Skills (Global/Built-in):

  - academic-writing
      You must use this when producing any research prose — literature reviews, syntheses,
      analyses, methodology descriptions, discussion sections, abstracts, or any written
      output intended for an academic audience.
  - critical-analysis
      You must use this when analyzing claims, evaluating evidence, or Identifying logical
      fallacies in research.
  - ethics-review
      You must use this when identifying ethical risks, ensuring participant privacy, or
      preparing IRB applications.
  - grant-proposal
      You must use this when drafting grant proposals, refining research aims, or aligning
      projects with agency priorities.
  - hypothesis-testing
      You must use this when formulating testable hypotheses, designing experimental controls,
      or defining falsification criteria.
  - lateral-thinking
      You must use this when seeking cross-domain analogies, applying first-principles
      reasoning, or overcoming creative bottlenecks.
  - literature-review
      You must use this when synthesizing existing knowledge, identifying research gaps, or
      tracing the evolution of scientific ideas.
  - multi-source-investigation
      You must use this when investigating complex claims across diverse sources or
      fact-checking contradictory information.
  - peer-review
      You must use this when critiquing academic manuscripts, evaluating methodological rigor,
      or providing structured reviewer feedback.
  - qualitative-research
      You must use this when designing qualitative studies, developing coding schemes, or
      performing thematic analysis.
  - quantitative-analysis
      You must use this when selecting statistical tests, interpreting effect sizes, or
      conducting power analysis.
  - research-manager
      Use this when starting a new research project or managing a complex, multi-step research
      workflow.
  - research-methodology
      You must use this when matching research questions to appropriate designs, sampling
      strategies, or validity controls.
  - research-synthesis
      You must use this when merging findings from multiple studies into a coherent narrative
      with grounded evidence.
  - systematic-review
      You must use this when conducting PRISMA-standard systematic reviews, protocol
      development, or Risk of Bias assessment.
  - using-co-researcher
      Use when understanding your capabilities, how to use skills, or the rules of the
      Co-Researcher system.

Available Agent Skills (Local Puzzles_for_AIs):

  - android-saf
      Sequential JSON-based workflow for accessing non-Termux files on Android using termux-saf-*.
  - logical-bug-finder
      Generalized template for diagnosing complex logical patterns and bugs in unstructured codebases or texts.
  - neo4j-expert
      Conceptual and operational master guide for interacting with Neo4j using MCP tools.
  - remote-codespaces
      Procedural instructions on tunneling and exposing GH Codespaces over SSH/SFTP directly to Termux.
  - stt-interpreter
      Log of STT input experiments alongside heuristics for adjusting logic and punctuation in English-39/74 transcriptions.
  - thunderbird-reader
      Instructions and Python snippet workflow for reading Thunderbird Mbox emails from the CLI.
```

## 🌟 Featured & Specialist Knowledge

Among the repository's contents, the following are highlighted as **highly specific** or **unusual** tools that solve complex edge cases:

### 🧩 Featured Skills
* **[android-saf](file:///home/zezen/Downloads/GitHub/Puzzles_for_AIs/skills/android-saf/SKILL.md)**: A specialized JSON-based workflow for navigating Android's **Storage Access Framework**. Essential for agents operating in Termux to access the broader Android filesystem.
* **[stt-interpreter](file:///home/zezen/Downloads/GitHub/Puzzles_for_AIs/skills/stt-interpreter/SKILL.md)**: A cognitive playbook for **interpreting and fixing Speech-to-Text errors**. It uses linguistic heuristics to correct logic and punctuation in raw transcripts (specialized for English-39/74 dialects).

### 📖 Key Traditional Guides
* **[AI Heuristic Distrust Protocol](file:///home/zezen/Downloads/GitHub/Puzzles_for_AIs/docs/guides/01_AI_Psychology_and_Cognitive_Frameworks/AI_Heuristic_Distrust_Protocol.md)**: A behavioral alignment guide that teaches the AI to **proactively verify assumptions** and avoid "Bulldog Mode" (looping on failing solutions).
* **[Docling Processing Guide](file:///home/zezen/Downloads/GitHub/Puzzles_for_AIs/docs/guides/03_API_and_Cloud_Tool_Integrations/docling_processing_guide%20-%20how%20to%20use%20docling%20for%20PDF%20reading.md)**: An operational guide for using **Docling** to extract high-fidelity structure and tables from complex PDFs, significantly outperforming standard parsers.

