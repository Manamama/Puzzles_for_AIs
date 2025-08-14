# Guide: Searching Documents in User Embeddings

This guide outlines the process for searching documents within your `user_docs_embeddings` collection.

## How to Search

To find documents related to a specific topic or content, I will perform a semantic search using the `llm similar` command.

**My Internal Process:**

1.  **Confirm Search Scope:** I will first confirm with you the specific topic you are interested in ("X") and that you wish to search within your `/home/zezen/Documents` directory.

2.  **Execute Search:** I will execute the `llm similar` command, providing your search query and requesting up to 20 top results.
    *   **Command Example (Internal Map):**
        ```bash
        llm similar user_docs_embeddings -c "Your search query here" -n 20
        ```
        *   `"Your search query here"`: This will be replaced with your actual search term.
        *   `-n 20`: I will retrieve the top 20 most relevant documents.

3.  **Process and Discuss Results:** I will internally process the results from the search. Instead of showing you raw output, I will discuss the key findings and the types of documents that were most relevant to your query.

4.  **Content Retrieval (Sanity Check):** If you wish to view the full content of any of the identified documents, I can retrieve it for you.
    *   **Tool Usage (Internal Map):**
        ```python
        default_api.read_file(absolute_path="/home/zezen/Documents/<relative_path_of_document>")
        ```
        *   `<relative_path_of_document>`: This will be replaced with the specific path of the document you want to read.

5.  **Refine Search (If Needed):** If the initial results are not what you expected, we can refine your search query and repeat the process.

