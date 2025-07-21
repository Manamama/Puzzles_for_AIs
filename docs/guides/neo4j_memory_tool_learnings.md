# Neo4j Toolset Discoveries

This document outlines the key learnings and syntax requirements for using the `neo4j-cypher` and `neo4j-memory` toolsets.

## `neo4j-cypher` vs. `neo4j-memory`

There is a fundamental difference in how the two toolsets interact with the Neo4j database:

*   **`neo4j-cypher` (`get_neo4j_schema`)**: This tool provides a **raw, low-level view** of the entire database. It inspects and returns all nodes, relationships, and properties that exist, without any assumptions about the data's structure or meaning.

*   **`neo4j-memory` (`read_graph`, `create_entities`, etc.)**: This toolset operates on a **specific, high-level data model**. It is designed to work with a structured concept of "entities" and "relations". As a result, `read_graph` will only return data that conforms to this specific model. An initially empty result from `read_graph` indicates that no data matching this model exists, even if the database itself is not empty.

## `neo4j-memory` Tool Syntax & Usage

To successfully use the `neo4j-memory` tools, the input data must follow a strict schema.

### Creating Data

#### `create_entities`
This tool requires a list of entity objects. Each object **must** contain the following fields:
*   `name` (string): A unique identifier for the entity.
*   `type` (string): The category or classification of the entity (e.g., "Person", "Location").
*   `observations` (list): A list of observations related to the entity. **This field is mandatory, even if it is an empty list (`[]`)**.
*   `properties` (dict, optional): A dictionary for any additional, unstructured attributes.

**Example:**
```json
[
  {
    "name": "Arthur",
    "type": "Person",
    "properties": { "title": "Sir" },
    "observations": []
  }
]
```

#### `create_relations`
This tool requires a list of relation objects. Each object **must** contain the following fields:
*   `source` (string): The `name` of the entity where the relationship originates.
*   `target` (string): The `name` of the entity where the relationship terminates.
*   `relationType` (string): The name or type of the relationship (e.g., "SERVES", "LOVES").

**Example:**
```json
[
  {
    "source": "Arthur",
    "target": "Uther",
    "relationType": "SERVES"
  }
]
```

### Reading & Searching Data

#### `read_graph`
*   **Practical Use:** Retrieves the *entire* knowledge graph that conforms to the memory model. Use this for a complete overview of all entities and their relationships.
*   **Tips & Mistakes to Avoid:** Can return a large amount of data. It's the "show me everything" command.

#### `find_memories_by_name`
*   **Practical Use:** Fetches one or more specific entities by their exact `name`. This is the most efficient way to retrieve an entity if you know its unique identifier.
*   **Tips & Mistakes to Avoid:** Requires an *exact, case-sensitive match* of the name. Returns the entities and their direct relationships.

#### `search_memories`
*   **Practical Use:** Performs a keyword search. Use this when you're looking for entities based on a concept or attribute but don't know their specific names.
*   **Tips & Mistakes to Avoid:**
    *   **CRUCIAL:** The search primarily targets the `observations` field. An entity may not appear in search results if the keyword is only in its `properties` or `name`.
    *   To make entities searchable, add relevant keywords and descriptions to their `observations` list.

### Updating Data

#### `add_observations`
*   **Practical Use:** Adds new information to an entity's `observations` list, making it more descriptive and discoverable via `search_memories`.
*   **Tips & Mistakes to Avoid:** The input structure is precise. It requires a list of objects, where each object has an `entityName` and an `observations` field which is a list of strings.
    *   **Incorrect:** `{"entityName": "Uther", "observation": "He is King."}`
    *   **Correct:** `{"entityName": "Uther", "observations": ["He is the King."]} `
```