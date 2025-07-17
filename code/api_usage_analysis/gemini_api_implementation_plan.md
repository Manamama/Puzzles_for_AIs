# Implementation Plan: Checking Gemini API Daily Usage in the CLI

This document outlines a phased implementation plan for integrating Gemini API daily usage checking into the Gemini CLI. The approaches are ordered from most feasible and recommended to least feasible, providing a clear path forward for development.

---

## Phase 1: Most Feasible - Google Cloud Monitoring via Python Client Library

### Approach Overview:
This approach leverages the official `google-cloud-monitoring` Python client library to programmatically query Google Cloud Monitoring for Gemini API usage data. This method is highly recommended due to its robustness, reliability, and the clean programmatic interface it offers.

### Core Mechanism:
The Python client library will fetch the `cloudaicompanion.googleapis.com/usage/response_count` metric. This metric accurately tracks the total number of API responses, which directly correlates to requests made. Daily usage is derived by setting a 24-hour alignment period and using the `ALIGN_DELTA` aggregator on this cumulative metric.

### Minimal Pseudocode/Example:
```python
from google.cloud import monitoring
from datetime import datetime, timedelta

def get_gemini_api_daily_usage(project_id: str) -> int:
    client = monitoring.Client(project=project_id)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1) # Query for the last 24 hours

    query = client.query(metric_type='cloudaicompanion.googleapis.com/usage/response_count')
    query = query.select_interval(start_time, end_time)
    query = query.align(monitoring.Aggregation.Aligner.ALIGN_DELTA, hours=24)

    total_requests = 0
    for ts in query.fetch():
        for point in ts.points:
            # Assuming double_value for simplicity, could be int64_value or distribution_value.count
            total_requests += point.value.double_value
    return int(total_requests)

# Example CLI integration:
# PROJECT_ID = GET_GCLOUD_PROJECT_ID()
# if PROJECT_ID:
#     daily_usage = get_gemini_api_daily_usage(PROJECT_ID)
#     DISPLAY_MESSAGE(f"Gemini API requests (last 24h): {daily_usage}")
```

### Pros:
*   **Robustness & Reliability:** Utilizes Google's official, well-maintained Python client library, ensuring stable and accurate interaction with the Cloud Monitoring API. This minimizes the risk of breaking changes from API updates.
*   **Programmatic Control:** Offers a clean, object-oriented interface for querying metrics, handling authentication, and parsing responses. This is significantly less error-prone and more maintainable than shell scripting and manual JSON parsing.
*   **Accurate Metric:** Employs the specific `cloudaicompanion.googleapis.com/usage/response_count` metric, which is designed for tracking API responses and provides precise usage data for the Gemini API.
*   **Flexible Error Handling:** Python's exception handling mechanisms allow for robust error management, providing clear feedback to the user in case of issues (e.g., network errors, authentication failures, API limits).
*   **Integration with Existing Tools:** Authentication seamlessly integrates with `gcloud auth application-default login`, a standard practice for Google Cloud development.

### Cons:
*   **Billing Requirement:** Cloud Monitoring requires billing to be enabled for the Google Cloud project, even for free-tier usage. This is a critical prerequisite and a significant hurdle for users who do not have billing enabled, effectively making this approach a semi-dead end for them.
*   **Python Dependency:** Introduces a dependency on Python and the `google-cloud-monitoring` library. If the Gemini CLI is not primarily Python-based, this might require setting up a Python execution environment or bundling Python.
*   **Initial Setup:** Users need to ensure `gcloud` is installed and `gcloud auth application-default login` has been run.

---

## Phase 2: Viable Alternative - Google Cloud Monitoring via `curl` (Command Line)

### Approach Overview:
This approach directly executes `curl` commands from the CLI to interact with the Google Cloud Monitoring API. It relies on `gcloud` to dynamically retrieve the project ID and an access token, which are then embedded into the `curl` request.

### Core Mechanism:
A `curl` command is constructed to make a POST request to the `https://monitoring.googleapis.com/v3/projects/{PROJECT_ID}/timeSeries:query` endpoint. The request body contains a Monitoring Query Language (MQL) string to filter for `serviceruntime.googleapis.com/api/request_count` (or `cloudaicompanion.googleapis.com/usage/response_count` if preferred, though the `curl` example often uses the former) for the `generativelanguage.googleapis.com` service, aggregated daily.

### Minimal Pseudocode/Example:
```pseudocode
FUNCTION get_gemini_api_daily_usage_curl():
    PROJECT_ID = RUN_SHELL_COMMAND("gcloud config get-value project")
    ACCESS_TOKEN = RUN_SHELL_COMMAND("gcloud auth print-access-token")
    YESTERDAY_UTC = RUN_SHELL_COMMAND("date -u -d \"yesterday\" +%Y-%m-%dT00:00:00Z")
    TODAY_UTC = RUN_SHELL_COMMAND("date -u +%Y-%m-%dT00:00:00Z")

    CURL_COMMAND = "curl -X POST "
    CURL_COMMAND += "  \"https://monitoring.googleapis.com/v3/projects/" + PROJECT_ID + "/timeSeries:query\" "
    CURL_COMMAND += "  -H \"Authorization: Bearer " + ACCESS_TOKEN + "\" "
    CURL_COMMAND += "  -H \"Content-Type: application/json\" "
    CURL_COMMAND += "  --data \"{"
    CURL_COMMAND += "    \"query\": \"fetch consumed_api | metric serviceruntime.googleapis.com/api/request_count | filter resource.labels.service = \\\"generativelanguage.googleapis.com\\\" | align delta() | every 1d | within \\\"" + YESTERDAY_UTC + "\\\",\\\"" + TODAY_UTC + "\\\"\\""
    CURL_COMMAND += "  }\"

    CURL_RESPONSE = RUN_SHELL_COMMAND(CURL_COMMAND)
    // Parse CURL_RESPONSE.STDOUT to extract usage data
    RETURN PARSE_JSON_AND_EXTRACT_USAGE(CURL_RESPONSE.STDOUT)
```

### Pros:
*   **Minimal External Dependencies (CLI perspective):** Does not require installing additional Python libraries if the CLI is not Python-based. Relies only on `gcloud` and `curl`, which are common CLI tools.
*   **Direct Command-Line Execution:** The core logic is expressed directly as a shell command, which can be appealing for shell-centric CLI designs.
*   **Leverages Existing Infrastructure:** Still utilizes the robust Google Cloud Monitoring service.

### Cons:
*   **Complexity of `curl` Command:** The `curl` command itself is long, complex, and highly sensitive to quoting, making it difficult to construct and debug.
*   **JSON Parsing Burden:** Extracting the relevant usage data from the `curl`'s JSON response requires robust parsing logic within the CLI, which can be cumbersome to implement in shell scripts or non-Python environments.
*   **Error Proneness:** More susceptible to errors due to shell environment variations, quoting issues, and manual JSON parsing.
*   **Metric Precision:** The `serviceruntime.googleapis.com/api/request_count` metric might be less precise for Gemini API usage compared to the `cloudaicompanion.googleapis.com/usage/response_count` metric identified in the Python approach.
*   **Billing Requirement:** Similar to the Python approach, Cloud Monitoring requires billing to be enabled.

---

## Phase 3: Least Feasible - Hypothetical Direct Gemini API Endpoint

### Approach Overview:
This represents the ideal, but currently unavailable, solution. It envisions a dedicated, public API endpoint provided by Google specifically for querying Gemini API usage statistics (e.g., requests made, remaining quota).

### Core Mechanism:
The CLI would make a simple HTTP GET request to a hypothetical `https://api.gemini.google.com/v1/usage/daily` endpoint, authenticated with the user's Gemini API token. The response would directly contain the daily usage and quota information.

### Minimal Pseudocode/Example:
```pseudocode
FUNCTION get_gemini_api_daily_usage_hypothetical():
    AUTH_TOKEN = GET_GEMINI_API_AUTH_TOKEN()
    IF AUTH_TOKEN IS NULL: RETURN ERROR

    USAGE_API_URL = "https://api.gemini.google.com/v1/usage/daily" // Hypothetical
    HEADERS = {"Authorization": "Bearer " + AUTH_TOKEN}

    RESPONSE = HTTP_GET(USAGE_API_URL, HEADERS)
    IF RESPONSE.STATUS_CODE == 200:
        RETURN PARSE_JSON(RESPONSE.BODY).dailyRequestsUsed
    ELSE: RETURN ERROR
```

### Pros:
*   **Simplicity & Efficiency:** Would be the most direct, efficient, and easiest to implement solution if available.
*   **Purpose-Built:** Designed specifically for usage tracking, likely providing the most accurate and user-friendly data.
*   **Minimal Dependencies:** Would require minimal external dependencies for the CLI itself.

### Cons:
*   **Currently Unavailable:** This API endpoint does not exist publicly for free-tier usage. This remains a hypothetical ideal.
*   **Reliance on External Development:** Depends entirely on Google developing and maintaining such a specific endpoint.

---

## Conclusion and Recommendation:

Based on the current landscape and detailed analysis:

**Recommendation:** The **Google Cloud Monitoring Python Client Library (Phase 1)** is the recommended approach for implementing Gemini API usage checking in the CLI. It offers the best balance of robustness, programmatic control, and accuracy, making it the most sustainable and maintainable solution for a production-ready feature.

**Alternative:** The **Google Cloud Monitoring via `curl` (Phase 2)** is a viable alternative, especially for shell-script-heavy CLIs, but developers should be aware of the increased complexity in command construction and JSON parsing.

**Future Consideration:** The **Hypothetical Direct Gemini API Endpoint (Phase 3)** remains the ultimate ideal. Should Google release such an API, it would likely supersede the other methods due to its inherent simplicity and directness.

---

**Note to Implementers:** Once this feature is implemented and coded, please inform the original poster of discussion #3096 (https://github.com/google-gemini/gemini-cli/discussions/3096). The code will most probably be posted on Manamama's GitHub repository (details to be determined).

---

## Using Sequential Thinking for Implementation and Debugging

This implementation plan will be executed using the `sequentialthinking` tool to provide a structured, iterative, and transparent development process. This approach is particularly beneficial for anticipating and managing challenges, ensuring a robust and well-documented solution.

### How `sequentialthinking` will be applied:

1.  **Problem Decomposition:** The overall task will be broken down into smaller, manageable `thought` steps, each with a `thoughtNumber` and an estimated `totalThoughts`. This will include:
    *   Environment setup (e.g., installing Python dependencies, `gcloud` authentication).
    *   Implementing the core API call function.
    *   Integrating the function into the CLI.
    *   Writing and running tests.
    *   Implementing robust error handling and considering edge cases.

2.  **Iterative Development and Debugging:** The `sequentialthinking` tool's features will be used to manage the inevitable "something will not work" scenarios:
    *   **Explicit Revision:** When a step fails or produces unexpected results, `isRevision=True` and `revisesThought` will be used to explicitly indicate that a previous thought is being revisited for correction. This creates a clear audit trail of the debugging process.
    *   **Branching for Alternatives:** If a chosen approach encounters a fundamental blocker or a more efficient alternative is identified, `branchFromThought` and `branchId` will be used to explore different solutions without losing the context of the original attempt. This allows for flexible problem-solving.

3.  **Maintaining Context and Learning:** The `thoughtHistory` maintained by the `sequentialthinking` tool will provide a comprehensive record of the development process, including decisions made, paths explored, and lessons learned. This systematic approach fosters continuous improvement and transparency.

### Anticipated Issues and `sequentialthinking`'s Role in Addressing Them:

*   **Environment Setup Issues:** If `pip install` or `gcloud auth` commands fail, `isRevision` will be used to debug the specific command, analyze error messages, and consult relevant documentation.
*   **API Call Errors:** In case of incorrect project ID, permissions issues, or rate limits, the `sequentialthinking` process will guide the analysis of API error responses and the adjustment of parameters or authentication.
*   **Data Parsing Problems:** If the API response data is not in the expected format, `sequentialthinking` will facilitate the revision of parsing logic, potentially involving inspecting raw output to refine extraction methods.
*   **Testing Failures:** Any test failures will trigger a revision within the `sequentialthinking` framework, allowing for systematic identification and resolution of the underlying issues in the code or test cases.

By adopting this structured approach with `sequentialthinking`, the implementation of the Gemini API daily usage check will be methodical, transparent, and resilient to unforeseen challenges, ensuring a high-quality and well-documented solution.

---

## Implementation Progress and Lessons Learned

This section documents the actual progress made during the implementation, highlighting successes, challenges, and key takeaways.

### Environment Setup:
- **`gcloud` CLI Installation:** Verified successfully. (`gcloud --version` command executed without issues).
- **`gcloud` Authentication:** Successfully authenticated using `gcloud auth application-default login`. Credentials were saved.
- **Python Library Installation:** `google-cloud-monitoring` library installed successfully using `pip`.

### Core API Call Implementation (Python Script):
- **Initial Script Development:** A Python script (`get_gemini_usage.py`) was created to fetch daily Gemini API usage using the `google-cloud-monitoring` library.
- **First Attempt - `TypeError`:** The initial execution of the Python script resulted in a `TypeError` because the `aggregation` parameter was passed directly to `client.list_time_series` instead of being encapsulated within a `ListTimeSeriesRequest` object.
    - **Lesson Learned:** Always refer to the official API documentation for correct parameter passing, especially for complex objects like `aggregation` in client library methods.
- **Second Attempt - `PermissionDenied` (HTTP 403):** After correcting the `TypeError` by passing `aggregation` within a `ListTimeSeriesRequest`, the script failed with a `PermissionDenied` error (HTTP 403). This error explicitly stated that billing was not enabled for the Google Cloud project, which is a prerequisite for using the Cloud Monitoring API.
    - **Lesson Learned:** Cloud Monitoring API requires billing to be enabled, even for free-tier usage. This is a critical prerequisite that must be communicated clearly to the user.

### Exploring `gcloud` CLI for Metrics (User Suggestion):
- **Attempt to List Metrics:** Multiple attempts were made to use `gcloud` commands (e.g., `gcloud monitoring metrics list`, `gcloud alpha monitoring metrics list`, `gcloud topic monitoring`) to directly list or query monitoring metrics related to Gemini API usage.
- **Result:** All attempts to directly query time series data using `gcloud` CLI commands failed. `gcloud` is primarily designed for managing Google Cloud resources and configurations, not for direct retrieval of time series monitoring data.
    - **Lesson Learned:** The `gcloud` CLI has limitations for direct data querying from Cloud Monitoring. While it can list metric *descriptors*, it cannot retrieve the actual time series data. The programmatic approach (Python client library or `curl` to the Monitoring API) remains necessary for this task.

### Current Blocker:
- The primary blocker for proceeding with the implementation is the **disabled billing for the Google Cloud project**. The Python script cannot successfully query the Cloud Monitoring API until billing is enabled.

### Next Steps:
- Awaiting user confirmation that billing has been enabled for the Google Cloud project. Once confirmed, the Python script will be re-executed.

---

### Handling Sensitive Files:
Sensitive files, such as API keys and client secrets, are stored in the `secrets` subdirectory within this folder. This directory is intentionally git-ignored to prevent these files from being committed to the repository, ensuring they remain secure and out of public view.
