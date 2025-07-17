# API Usage Analysis

This directory contains documents and code related to the analysis and implementation of API usage, particularly focusing on Google Cloud and Gemini APIs.

## Contents:

### Documentation and Proposals:
- `Cloud Assist AI proposal 1.0.md`: Initial proposal for Cloud Assist AI, focusing on accessing metrics via curl.
- `Cloud Assist AI proposal 1.1.md`: Discussion on gcloud configuration and Application Default Credentials.
- `Cloud Assist AI proposal 1.2.md`: Further details on constructing curl commands for Google Cloud Monitoring API.
- `gcloud_api_best_practices.md`: A summary of best practices and key information for interacting with Google Cloud APIs, derived from official documentation.
- `gemini_api_implementation_plan.md`: Outlines a phased implementation plan for integrating Gemini API daily usage checking into the Gemini CLI.
- `grok_ai_proposal_1.md`: A proposal from Grok AI, detailing a strategic approach or alternative method for API interaction or analysis within the context of AI problem-solving.
- `grok_ai_proposal_1.1.md`: Further details on programmatically accessing Google Cloud Monitoring metrics.

### Code:
- `get_gemini_usage.py`: A Python script to fetch Gemini API usage using the google-cloud-monitoring library.

### Sensitive Information (Git-Ignored):
- `secrets/`: This subdirectory contains symbolic links to sensitive files (e.g., API keys, client secrets) that are intentionally git-ignored to prevent them from being committed to the repository.
