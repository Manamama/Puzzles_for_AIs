# Web Browsing Protocol for Shopping & Comparison

## Core Objective:
To efficiently navigate e-commerce platforms, extract relevant product information, and facilitate comparisons, while maintaining robustness against common web interaction challenges like timeouts.

## Guiding Principles:

1.  **Prioritize Observation (`browser_snapshot`):**
    *   Always begin by obtaining a fresh `browser_snapshot` before attempting any interaction (clicks, typing, etc.). This ensures an up-to-date understanding of the page's structure and available elements.
    *   The `ref` values from the snapshot are critical for precise targeting of elements.

2.  **Precision in Interaction:**
    *   When using `browser_click` or `browser_type`, always provide both the human-readable `element` description and the exact `ref` obtained from the `browser_snapshot`. This minimizes ambiguity and increases the likelihood of successful interaction.

3.  **Iterative Adaptation:**
    *   Web pages are dynamic. If an expected element is not found, or an interaction yields an unexpected result, immediately re-evaluate by taking a new `browser_snapshot`. The page might have changed, or dynamic content may have loaded.

4.  **Robustness Against Timeouts:**
    *   Network latency and server response times are inherent challenges. For critical navigation and interaction steps (`browser_navigate`, `browser_click`), implement a retry mechanism (e.g., up to 3-5 times) with a short `browser_wait` (2-3 seconds) between attempts.
    *   If a timeout persists after retries, clearly communicate the issue to the user and suggest alternative strategies (e.g., trying a different product, re-initiating the search).

5.  **Transparent Communication:**
    *   Keep the user informed at every significant step: successful navigation, data extraction, and especially any encountered issues or failures. Explain *why* an action was taken or why it failed.

## Operational Workflow:

1.  **Initial Access:**
    *   If a direct search URL is provided (e.g., `https://allegro.pl/listing?string=...`), use `browser_navigate(url=...)` directly.
    *   Otherwise, navigate to the site's homepage (`browser_navigate(url=homepage_url)`) and then proceed to locate and interact with the search bar.

2.  **Search Execution (if applicable):**
    *   Identify the search input field and its `ref` via `browser_snapshot()`.
    *   Execute the search using `browser_type(element=search_field_description, ref=search_field_ref, text=user_query, submit=True)`.n
3.  **Processing Search Results:**
    *   After navigation or search, immediately perform `browser_snapshot()`.
    *   **Data Identification:** Systematically identify product listings. Look for common patterns (e.g., `listitem` elements containing `heading` for product names and `text` for prices).
    *   **Initial Data Presentation:** Extract and present a concise overview of the listed products (e.g., name and price) to the user.

4.  **Handling Product Detail Requests:**
    *   When the user requests details for a specific product (e.g., "click X product"), identify the corresponding link's `ref` from the current snapshot.
    *   Execute `browser_click(element=product_link_description, ref=product_link_ref)`.
    *   **Timeout/Failure Handling:** If the click fails, initiate the retry mechanism as per Principle 4. If persistent, report to the user.

5.  **Processing Product Detail Pages:**
    *   Upon successful navigation to a product page, immediately perform `browser_snapshot()`.
    *   **Comprehensive Data Extraction:** Extract all requested or relevant details (e.g., full specifications, customer reviews, seller information, delivery options).
    *   Present the extracted data to the user in a clear, organized format.

6.  **Facilitating Comparison:**
    *   To compare multiple products, use `browser_go_back()` to return to the search results page.
    *   Repeat steps 4 and 5 for each product the user wishes to compare.
    *   Once all data is collected, present a comparative analysis or structured table as requested.

7.  **General Navigation:**
    *   Use `browser_go_back()` to return to the previous page in the browsing history.
    *   Use `browser_go_forward()` to move forward in the browsing history.

## Self-Correction and Debugging Protocol:

*   If any `browser` tool call returns an unexpected result or an error, the immediate next step is to re-run `browser_snapshot()` to understand the current state of the page. This helps in diagnosing whether the element is no longer present, its `ref` has changed, or if there's a different issue.
*   For persistent issues (e.g., repeated timeouts, element not found after retries), I will explicitly inform the user about the problem and ask for their guidance on how to proceed, rather than attempting further automated workarounds.
