# Neo4j Interaction Guide for AIs

This document outlines the best practices and learned methods for interacting with the Neo4j database using the available tools.

**Note on Configuration:** All Neo4j credentials (URI, username, password, database) are sourced from the `.env` file at the root of the Gemini directory. Do not hardcode these values in `settings.json` or other configuration files.

## 1. End-to-End Workflow: Text to Online Graph

This section outlines the complete real-world workflow for transforming unstructured text into a queryable and visually intuitive knowledge graph, emphasizing the immediate online visualization aspect.

1.  **User Supplies Text Files:** The user provides unstructured text content (e.g., news articles, reports, notes).
2.  **AI Converts to Cypher Queries:** The AI (myself) processes the text, extracts entities and relationships based on best practices, and generates precise Cypher queries.
3.  **AI Populates Neo4j Database:** The generated Cypher queries are executed against the Neo4j database using the available tools.
4.  **User Visualizes Online Instantly:** The user can immediately visualize the newly created or updated graph in a GUI using the following services:

    *   **Neo4j Labs Graph Builder:** [https://llm-graph-builder.neo4jlabs.com/](https://llm-graph-builder.neo4jlabs.com/)
    *   **Neo4j Console Preview (Query):** [https://console-preview.neo4j.io/tools/query](https://console-preview.neo4j.io/tools/query)
    *   **Neo4j Console Preview (Explore):** [https://console-preview.neo4j.io/tools/explore](https://console-preview.neo4j.io/tools/explore) (Allows instant visualization of changes)

This seamless process allows for rapid prototyping and exploration of knowledge extracted from text.

## 2. Core Concepts: `neo4j-cypher` vs. `neo4j-memory` Toolsets

There is a fundamental difference in how the two toolsets interact with the Neo4j database:

*   **`neo4j-cypher` (`get_neo4j_schema`)**: This tool provides a **raw, low-level view** of the entire database. It inspects and returns all nodes, relationships, and properties that exist, without any assumptions about the data's structure or meaning.

*   **`neo4j-memory` (`read_graph`, `create_entities`, etc.)**: This toolset operates on a **specific, high-level data model**. It is designed to work with a structured concept of "entities" and "relations". As a result, `read_graph` will only return data that conforms to this specific model. An initially empty result from `read_graph` indicates that no data matching this model exists, even if the database itself is not empty.

## 3. Verification and Visualization (Detailed)

Beyond the immediate online visualization, it's helpful to understand the current state of the graph programmatically. You can get a schema overview directly using the `get_neo4j_schema()` tool.

### Addressing Visualization Challenges in Neo4j Console's "Explore" View

The Neo4j Console's "Explore" view can be overwhelming with technical metadata (embeddings, `Chunk`, `Document` nodes, and technical relationships like `HAS_ENTITY`, `FIRST_CHUNK`, `NEXT_CHUNK`, `PART_OF`, `SIMILAR`). While the GUI offers filtering options ("In Scene", "Off Scene", Node Labels, Relationship Types, Property Filters), these can be counter-intuitive or apply predefined queries that include unwanted nodes.

**Key Learnings:**
*   The "Show me a graph" button in the Neo4j Console often applies a predefined Cypher query that includes `Chunk` and `Document` nodes, making it difficult to get a clean view of the semantic graph.
*   Interactive filters (like "In Scene" and "Off Scene") apply immediately, but their behavior can be confusing, especially when they differ for nodes and relationships.

**Solution for a Cleaner View:**
To get a cleaner, more relevant visualization, it's best to use a custom Cypher query that explicitly excludes the technical metadata. Here's a query that can be pasted directly into the Neo4j Console's query editor:

```cypher
MATCH (n)-[r]->(m)
WHERE NOT (n:Chunk OR n:Document OR n:__Entity__)
  AND NOT (m:Chunk OR m:Document OR m:__Entity__)
  AND NOT type(r) IN ['HAS_ENTITY', 'FIRST_CHUNK', 'NEXT_CHUNK', 'PART_OF', 'SIMILAR']
RETURN n, r, m
LIMIT 100 // Limit the number of results to avoid overwhelming the visualization
```

This query will:
*   `MATCH (n)-[r]->(m)`: Find all nodes `n` and `m` and their relationships `r`.
*   `WHERE NOT (n:Chunk OR n:Document OR n:__Entity__)`: Exclude `Chunk`, `Document`, and `__Entity__` nodes from the starting point of the relationship.
*   `AND NOT (m:Chunk OR m:Document OR m:__Entity__)`: Exclude `Chunk`, `Document`, and `__Entity__` nodes from the ending point of the relationship.
*   `AND NOT type(r) IN [...]`: Exclude the specified technical relationship types.
*   `RETURN n, r, m`: Return the filtered nodes and relationships.
*   `LIMIT 100`: Limits the number of results to prevent overwhelming the visualization.

## 4. Problems to Solve Soon

1.  **Automate Graph Visualization Filtering:** Explore ways to programmatically apply the filtering Cypher query or configure the Neo4j Console to default to a cleaner view, rather than requiring manual pasting of the query.
2.  **Improve High-Level Memory/Entity Tools:** Test and refine the `neo4j_memory__` prefixed tools to ensure they provide a robust and intuitive way to manipulate the graph without needing direct Cypher queries for common tasks. This includes verifying their behavior for creating, updating, and deleting entities and relationships, and ensuring they handle edge cases (e.g., non-existent nodes) gracefully.

## 5. Best Practices for Knowledge Graph Construction

Transforming unstructured text into a structured knowledge graph requires significant intellectual effort beyond just knowing how to use the Neo4j tools. This process involves:

1.  **Entity Extraction:** Carefully identifying all relevant people, organizations, locations, concepts, and events from the narrative. This requires a deep understanding of the text's context and nuances.
2.  **Relationship Identification:** Determining the meaningful connections and interactions between the extracted entities. This is crucial for building a rich and interconnected graph.
3.  **Schema Design:** Designing an appropriate graph schema, including node labels (e.g., `Person`, `Organization`, `Location`, `Concept`, `Event`) and relationship types (e.g., `INVESTIGATES`, `REPORTED`, `LOCATED_IN`, `ACCUSED_OF_TIES_WITH`). The schema should accurately represent the domain and facilitate meaningful queries.
4.  **Cypher Query Construction:** Translating the identified entities and relationships into precise Cypher `MERGE` statements. This involves ensuring correct property assignments, handling potential duplicates, and structuring queries for efficiency.

While the `write_neo4j_cypher` tool simplifies database interaction, the intellectual task of transforming natural language into a structured knowledge graph remains a key challenge and a critical step for effective graph population.

## 6. Interaction Methods

There are two primary methods for interacting with the database:

### Method A: Direct Cypher Queries

This method provides the most power and flexibility. It is ideal for complex queries, specific data retrieval, and fine-grained control.

**Tools:**
*   `read_neo4j_cypher(query: str)`: For all read-only operations (`MATCH`, `RETURN`).
*   `write_neo4j_cypher(query: str)`: For all write operations (`CREATE`, `MERGE`, `SET`, `DELETE`).

### Method B: High-Level Memory/Entity Tools

This method is more abstract and intuitive, allowing you to work with "entities" and "relations" without writing raw Cypher. This is preferable for structured data entry and simpler graph manipulations.

**Primary Tools:**
*   `neo4j_memory__create_entities`
    *   This tool requires a list of entity objects. Each object **must** contain the following fields:
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

*   `neo4j_memory__create_relations`
    *   This tool requires a list of relation objects. Each object **must** contain the following fields:
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

*   `neo4j_memory__add_observations`
    *   **Practical Use:** Adds new information to an entity's `observations` list, making it more descriptive and discoverable via `search_memories`.
    *   **Tips & Mistakes to Avoid:** The input structure is precise. It requires a list of objects, where each object has an `entityName` and an `observations` field which is a list of strings.
        *   **Incorrect:** `{"entityName": "Uther", "observation": "He is King."}`
        *   **Correct:** `{"entityName": "Uther", "observations": ["He is the King."]} `

*   `neo4j_memory__delete_entities`: To remove nodes and their relationships.

*   `read_graph`
    *   **Practical Use:** Retrieves the *entire* knowledge graph that conforms to the memory model. Use this for a complete overview of all entities and their relationships.
    *   **Tips & Mistakes to Avoid:** Can return a large amount of data. It's the "show me everything" command.

*   `find_memories_by_name`
    *   **Practical Use:** Fetches one or more specific entities by their exact `name`. This is the most efficient way to retrieve an entity if you know its unique identifier.
    *   **Tips & Mistakes to Avoid:** Requires an *exact, case-sensitive match* of the name. Returns the entities and their direct relationships.

*   `search_memories`
    *   **Practical Use:** Performs a keyword search. Use this when you're looking for entities based on a concept or attribute but don't know their specific names.
    *   **Tips & Mistakes to Avoid:**
        *   **CRUCIAL:** The search primarily targets the `observations` field. An entity may not appear in search results if the keyword is only in its `properties` or `name`.
        *   To make entities searchable, add relevant keywords and descriptions to their `observations` list.

**Important Distinction:** Be aware that there is another set of generic `memory` tools. For direct Neo4j manipulation, ensure you are using the `neo4j_memory__` prefixed tools.

## 7. Common Cypher Query Patterns

This section provides examples of common Cypher query patterns for interacting with the Neo4j database. These examples focus purely on the Cypher syntax, as the MCP server handles the connection and execution.

### 7.1. Creating Nodes

**Create a single node with a label and properties:**
```cypher
CREATE (p:Person {name: 'Alice', age: 30})
```

**Create multiple nodes:**
```cypher
CREATE (p1:Person {name: 'Bob'})
CREATE (p2:Person {name: 'Charlie'})
```

**Merge a node (create if not exists, match if exists):**
```cypher
MERGE (c:City {name: 'London'})
```

### 7.2. Creating Relationships

**Create a relationship between existing nodes:**
```cypher
MATCH (p1:Person {name: 'Alice'}), (p2:Person {name: 'Bob'})
CREATE (p1)-[:KNOWS]->(p2)
```

**Create a node and a relationship simultaneously:**
```cypher
MATCH (p:Person {name: 'Alice'})
CREATE (p)-[:LIVES_IN]->(c:City {name: 'Paris'})
```

**Merge a relationship:**
```cypher
MATCH (p:Person {name: 'Alice'}), (c:City {name: 'London'})
MERGE (p)-[:LIVES_IN]->(c)
```

### 7.3. Matching Nodes and Relationships

**Match all nodes with a specific label:**
```cypher
MATCH (p:Person)
RETURN p.name, p.age
```

**Match nodes with specific properties:**
```cypher
MATCH (p:Person {name: 'Alice'})
RETURN p
```

**Match nodes connected by a relationship:**
```cypher
MATCH (p1:Person)-[:KNOWS]->(p2:Person)
RETURN p1.name, p2.name
```

**Match relationships with properties:**
```cypher
MATCH (p1:Person)-[r:WORKS_AT {since: 2020}]->(c:Company)
RETURN p1.name, c.name, r.since
```

### 7.4. Updating Node Properties

**Set a new property or update an existing one:**
```cypher
MATCH (p:Person {name: 'Alice'})
SET p.age = 31
RETURN p
```

**Set multiple properties:**
```cypher
MATCH (p:Person {name: 'Bob'})
SET p.age = 25, p.city = 'New York'
RETURN p
```

### 7.5. Deleting Nodes and Relationships

**Delete a node and all its relationships:**
```cypher
MATCH (p:Person {name: 'Charlie'})
DETACH DELETE p
```

**Delete only relationships:**
```cypher
MATCH (p1:Person {name: 'Alice'})-[r:KNOWS]->(p2:Person)
DELETE r
```

These examples cover the most frequent operations you'll perform when working with Neo4j using Cypher. Remember to adapt the labels, relationship types, and properties to your specific graph model.

## 8. Official Neo4j Drivers and docs

*   **Python:**
    *   Neo4j Python Driver Manual: [https://neo4j.com/docs/python-driver/current/](https://neo4j.com/docs/python-driver/current/)
    *   Python Driver API Documentation: [https://neo4j.com/docs/python-driver/current/api/](https://neo4j.com/docs/python-driver/current/api/)
    *   PyPI: [https://pypi.org/project/neo4j/](https://pypi.org/project/neo4j/)



## 9. Connectors

*   **Neo4j Connector for Apache Kafka:**
    *   Neo4j Documentation: [https://neo4j.com/docs/kafka-connector/current/](https://neo4j.com/docs/kafka-connector/current/)
    *   GitHub Repository: [https://github.com/neo4j-contrib/neo4j-kafka-connect](https://github.com/neo4j-contrib/neo4j-kafka-connect)
*   **Neo4j Dataflow Flex Templates:**
    *   Google Cloud Documentation: [https://cloud.google.com/dataflow/docs/guides/templates/provided-templates#neo4j-to-neo4j](https://cloud.google.com/dataflow/docs/guides/templates/provided-templates#neo4j-to-neo4j)
    *   Neo4j Partner GitHub: [https://github.com/neo4j-field/neo4j-dataflow-flex-templates](https://github.com/neo4j-field/neo4j-dataflow-flex-templates)
*   **Neo4j Connector for Apache Spark:**
    *   Neo4j Documentation: [https://neo4j.com/docs/spark-connector/current/](https://neo4j.com/docs/spark-connector/current/)
    *   GitHub Repository: [https://github.com/neo4j-contrib/neo4j-spark-connector](https://github.com/neo4j-contrib/neo4j-spark-connector)
*   **Neo4j Connector for Business Intelligence (JDBC):**
    *   Neo4j Documentation: [https://neo4j.com/docs/bi-connector/current/](https://neo4j.com/docs/bi-connector/current/)
    *   Magnitude Simba Documentation: [https://www.simba.com/drivers/neo4j-odbc-jdbc/](https://www.simba.com/drivers/neo4j-odbc-jdbc/)
*   **Neo4j Connector for Business Intelligence (ODBC):
    *   CData Software Documentation: [https://www.cdata.com/drivers/neo4j/odbc/](https://www.cdata.com/drivers/neo4j/odbc/)
    *   Magnitude Simba Documentation: [https://www.simba.com/drivers/neo4j-odbc-jdbc/](https://www.simba.com/drivers/neo4j-odbc-jdbc/)
*   **Neo4j Data Warehouse Connector:**
    *   GitHub Repository: [https://github.com/neo4j-contrib/neo4j-data-warehouse-connector](https://github.com/neo4j-contrib/neo4j-data-warehouse-connector)
    *   Neo4j Documentation: [https://neo4j.com/docs/data-warehouse-connector/current/](https://neo4j.com/docs/data-warehouse-connector/current/)
*   **Kerberos for Neo4j:**
    *   Neo4j Documentation: [https://neo4j.com/docs/operations-manual/current/authentication/kerberos/](https://neo4j.com/docs/operations-manual/current/authentication/kerberos/)
*   **Spring Data Neo4j:**
    *   Spring Data Neo4j Project Page: [https://spring.io/projects/spring-data-neo4j](https://spring.io/projects/spring-data-neo4j)
    *   Spring Data Neo4j Documentation: [https://docs.spring.io/spring-data/neo4j/docs/current/reference/html/](https://docs.io/spring-data/neo4j/docs/current/reference/html/)
    *   GitHub Releases (for specific versions): [https://github.com/spring-projects/spring-data-neo4j/releases](https://github.com/spring-projects/spring-data-neo4j/releases)
*   **Neo4j-OGM:**
    *   Neo4j Documentation: [https://neo4j.com/docs/ogm/current/](https://neo4j.com/docs/ogm/current/)
    *   GitHub Repository: [https://github.com/neo4j/neo4j-ogm](https://github.com/neo4j/neo4j-ogm)
