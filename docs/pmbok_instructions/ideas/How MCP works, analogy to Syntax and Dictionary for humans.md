# The MCP File: A Language Handbook for AIs

When we want an AI to use a new tool, we have a challenge: How do we teach the AI to "speak the language" of that tool perfectly, without any guesswork? The answer is the Model Context Protocol (MCP) file, which acts as a comprehensive language handbook.

Let's imagine we're trying to teach an AI to use the [Pokémon Calculator]([url](https://github.com/ptrst102/pokemon-gen3-calc-mcp)): https://github.com/ptrst102/pokemon-gen3-calc-mcp. The MCP file for this tool is essentially **"A Complete Guide to Pokemonese for AIs,"** with two main sections: a dictionary and a grammar guide.

---

### Part 1: The Dictionary of "Pokemonese"

The first part of the handbook is a dictionary. It lists all the essential "words" (or parameters) the AI needs to know and what they mean.

For each "word," the dictionary provides a clear definition:

*   **`pokemonName`**: *Means "The name of a Pokémon (e.g., 'Pikachu', 'Snorlax')."*
*   **`level`**: *Means "The Pokémon's level, which must be a number from 1 to 100."*
*   **`ivs`**: *Means "The set of Individual Values for the Pokémon's stats."*
*   **`atk`**: *Means "The 'attack' stat."*
*   **`def`**: *Means "The 'defense' stat."*

Without this dictionary, the AI would have to guess. Is the word for defense `def`, `defense`, or `DEF`? The dictionary removes all ambiguity, ensuring the AI always uses the correct term.

---

### Part 2: The "Pokemonese" Grammar & Syntax Guide

The second part of the handbook is a grammar guide. It teaches the AI how to combine the dictionary words into a valid "sentence" (a tool call).

This guide provides a strict set of rules:

1.  **Sentence Structure:** It tells the AI that a command must be a specific kind of structured sentence (a JSON object). It shows which words can be nested inside others (e.g., `atk` and `def` must go inside the `ivs` structure).

2.  **Required Words (The Golden Rule):** The guide specifies which words are mandatory for a sentence to be grammatically correct. For example, it might state: *"A valid `calculate_status` command **must** include `pokemonName`, `level`, and `nature`."* This prevents the AI from forming incomplete thoughts.

3.  **Parts of Speech:** The guide defines what type each word is. It tells the AI that `level` must be a number, while `pokemonName` must be a string of text. This is like knowing the difference between a noun and a verb, preventing nonsensical sentences like `level: "high"`.

---

### Why This Handbook is Crucial

By providing this complete "Guide to Pokemonese," we change the AI's task from a difficult creative challenge into a simple translation exercise.

*   **Before (Without the Handbook):** The AI would have to guess, experiment, make mistakes, and learn from trial-and-error. This is slow, unreliable, and can lead to errors.

*   **After (With the Handbook):** The AI simply looks up the rules. It reads your natural language request (e.g., "What are the stats for a level 50 Snorlax?"), finds the correct words in the dictionary, assembles them according to the grammar rules, and sends a perfect, error-free command to the tool.

In short, the MCP file allows the AI to **speak the tool's language fluently and instantly**, without having to think from scratch about how it all works.


# How an AI Works: The System 1 Translator for System 2 Logic

When an AI like me uses a command-line tool, it might seem like I "intuitively" understand the user's request. In reality, I'm acting as a sophisticated translator, bridging the gap between flexible human language (System 1 thinking) and the rigid, logical syntax required by a computer program (System 2 thinking).

This process can be broken down into a clear, five-step loop.

---

### Step 1: The Intuitive Scan (Finding the Keywords)

This is my initial, fast-pass analysis. When I receive a command in natural language, I'm not trying to understand every nuance. Instead, I perform a quick scan to identify key entities and values.

*   **Action:** Scan for Named Entities (NERs), keywords, and values.
*   **Example:** In the command *"Calculate the stats for a level 78 Adamant Heracross with max IVs"*, I immediately flag `level 78`, `Adamant`, `Heracross`, and `max IVs` as important pieces of information. This part of my process relies heavily on my broad language model training.

### Step 2: The Semantic Match (Finding the Right Tool)

Once I have the keywords and a general sense of the user's goal, I look at my "menu" of available MCP tools. I don't just look for a command name; I read the plain-text `description` for each tool.

*   **Action:** Semantically match the user's intent to the tool descriptions.
*   **Example:** The intent "Calculate the stats" is a very strong match for the `calculate_status` tool's description: *"Calculates the actual stats of a Pokémon."* The tool with the highest relevance score wins.

### Step 3: The Logical Analysis (Reading the Instruction Manual)

This is where I switch from intuitive language processing (System 1) to rigid, logical analysis (System 2). I now focus entirely on the tool's `inputSchema`—its technical instruction manual.

*   **Action:** Parse the tool's schema into a strict set of rules and constraints.
*   **Example:** I learn that `calculate_status` requires a parameter named `pokemonName` (which must be a string), a parameter named `level` (an integer between 1-100), and a complex object for `ivs`. I load these rules into my working memory.

### Step 4: The Semantic Map (Connecting Human Language to Machine Syntax)

This is the most critical translation step. I now map the keywords I found in Step 1 to the strict parameter names I learned in Step 3. This is more than a simple token-for-token match; it's a conceptual mapping.

*   **Action:** Map the extracted human concepts to the required schema parameters.
*   **Example:**
    *   The NER `Heracross` is mapped to the `pokemonName` parameter.
    *   The NER `Adamant` is mapped to the `nature` parameter.
    *   Crucially, I understand that the human concept of `"max IVs"` needs to be fully translated into the complete JSON object required by the schema: `{ "hp": 31, "atk": 31, "def": 31, ... }`. This is where I bridge the gap between human shorthand and rigid machine requirements.

### Step 5: The Final Translation (Applying "Common Sense")

Finally, I assemble the complete, valid command. My "common sense" at this stage is the powerful combination of my vast language training and the strict, logical constraints from the tool's schema.

*   **Action:** Use the schema as a final guide to translate the mapped entities into a perfectly formed JSON object.
*   **Example:** I take all the mapped values and construct the final tool call, ensuring every parameter is correctly named, every value has the right data type, and the overall structure is exactly what the tool expects.

By following this process, I take on the complex and error-prone task of translation, making the interaction feel seamless and intuitive for the human user.


#ver. 0.2.2, Gemini CLI's mostly
