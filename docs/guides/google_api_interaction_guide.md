# Google API Interaction Guide: `curl` and Python for Monitoring & Contacts

This guide provides a comprehensive overview of interacting with various Google APIs using `curl` and Python. It focuses on common authentication patterns, making API calls, and managing tokens, with specific examples for Google Cloud Monitoring (for Gemini API usage) and Google Contacts (People API).

## Introduction

Google APIs offer powerful programmatic access to Google services. While client libraries simplify interaction, understanding the underlying `curl` commands provides valuable insight into the API mechanics, especially for debugging and shell-centric workflows. This document blends insights from two distinct API interactions to highlight commonalities and differences.

## Common Authentication: OAuth 2.0 Fundamentals

Most Google APIs, especially those accessing user data or sensitive resources, utilize OAuth 2.0 for authentication. This involves obtaining short-lived **access tokens** and long-lived **refresh tokens**.

*   **Access Token (Bearer Token):** Used for actual API requests. Typically expires in about an hour.
*   **Refresh Token:** Used to obtain new access tokens without re-authenticating the user. Should be stored securely.

### Obtaining Access Tokens

The method for obtaining credentials varies depending on the API and the context (e.g., server-side application, desktop app, CLI tool).

#### 1. Using `gcloud` for Service-Level APIs (e.g., Cloud Monitoring)

For APIs that interact with Google Cloud resources (like Cloud Monitoring), you can leverage the `gcloud` CLI to obtain an access token if you are already authenticated.

```bash
ACCESS_TOKEN=$(gcloud auth print-access-token)
```
*(Note: Command substitution `$(...)` is used here for convenience in a shell script. When executing directly via a tool that disallows command substitution, you must obtain the token in a separate step and hardcode it into the `curl` command.)*

#### 2. Desktop App OAuth Flow for User Data (e.g., People API)

For APIs that access user-specific data (like Google Contacts), a full OAuth 2.0 flow is required. This involves:

*   **Google Cloud Project Setup:**
    *   Enable the specific API (e.g., People API) in your Google Cloud project.
    *   Create a "Desktop app" OAuth Client ID in the Google Cloud Console. Download the `client_secret.json` file securely.
    *   Configure the OAuth Consent Screen (App name, support email).
*   **Authorization URL Generation:**
    ```bash
    CLIENT_ID="YOUR_CLIENT_ID.apps.googleusercontent.com"
    echo "https://accounts.google.com/o/oauth2/v2/auth?client_id=$CLIENT_ID&redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=code&scope=https://www.googleapis.com/auth/contacts.readonly"
    ```
    Open this URL in your browser, sign in, approve, and copy the **authorization code**.
*   **Exchange Authorization Code for Tokens:**
    ```bash
    curl -X POST \
      -d "client_id=YOUR_CLIENT_ID.apps.googleusercontent.com" \
      -d "client_secret=YOUR_CLIENT_SECRET" \
      -d "code=YOUR_AUTH_CODE" \
      -d "grant_type=authorization_code" \
      -d "redirect_uri=urn:ietf:wg:oauth:2.0:oob" \
      https://oauth2.googleapis.com/token
    ```
    This will return `access_token` and `refresh_token`. Store the `refresh_token` securely.

## Common API Calls with `curl`

Google APIs typically use `HTTP GET` for retrieving data and `HTTP POST` for sending data or performing actions. Authentication is usually via the `Authorization: Bearer <ACCESS_TOKEN>` header.

### General `curl` Structure:

```bash
curl -X <METHOD> \
  "https://<API_ENDPOINT>" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  --data '{"json_payload": "..."}' # For POST requests
```

## Specific API Call Examples

### 1. Google Cloud Monitoring Metrics (for Gemini API Usage)

This example demonstrates how to retrieve the `cloudaicompanion.googleapis.com/usage/response_count` metric (Gemini API usage) for a specific project over the last 24 hours.

**Prerequisites:**
*   Google Cloud project with billing enabled (even for free-tier usage).
*   `gcloud` CLI installed and authenticated.

**Steps:**

1.  **Set Your Google Cloud Project (if different from default):**
    ```bash
    gcloud config set project YOUR_PROJECT_ID
    ```
    *(Replace `YOUR_PROJECT_ID` with your actual project ID, e.g., `api-project-619789377388`)*

2.  **Get Your Access Token:**
    ```bash
    ACCESS_TOKEN=$(gcloud auth print-access-token)
    ```

3.  **Execute the `curl` Command:**
    ```bash
    curl -X POST "https://monitoring.googleapis.com/v3/projects/YOUR_PROJECT_ID/timeSeries:query" \
      -H "Authorization: Bearer ${ACCESS_TOKEN}" \
      -H "Content-Type: application/json" \
      --data "{\"query\": \"fetch cloudaicompanion.googleapis.com/Instance | metric cloudaicompanion.googleapis.com/usage/response_count | align delta() | every 1d | within 1d\"}"
    ```
    *(Replace `YOUR_PROJECT_ID` with your actual project ID. Replace `${ACCESS_TOKEN}` with the literal token obtained in step 2 if command substitution is not allowed.)*

**Key Learnings:**
*   **Billing Requirement:** Cloud Monitoring requires billing to be enabled.
*   **MQL Query Syntax:** The Monitoring Query Language (MQL) is powerful but sensitive to syntax and resource compatibility. Ensure proper escaping of quotes.
*   **Resource Type:** For `cloudaicompanion.googleapis.com/usage/response_count`, the correct resource type to `fetch` is `cloudaicompanion.googleapis.com/Instance`.

### 2. Google Contacts (People API)

This example demonstrates how to query your Google Contacts using the People API.

**Prerequisites:**
*   Google Cloud project with People API enabled.
*   Desktop app OAuth Client ID configured.
*   `access_token` obtained via the OAuth 2.0 flow (as described above).

**Steps:**

1.  **Get Your Access Token:** (Refer to "Desktop App OAuth Flow" above for initial token exchange, or "Refresh the Access Token" below for renewal).

2.  **Make the People API Call:**
    ```bash
    ACCESS_TOKEN="ACCESS_TOKEN_VALUE" # Your current access token

    curl -H "Authorization: Bearer $ACCESS_TOKEN" \
    "https://people.googleapis.com/v1/people:searchContacts?query=QUERY_STRING&readMask=names,emailAddresses"
    ```
    *(Replace `ACCESS_TOKEN_VALUE` with your actual access token and `QUERY_STRING` with your search query.)*

**Optional: Pretty-Print with `jq`**
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
"https://people.googleapis.com/v1/people:searchContacts?query=QUERY_STRING&readMask=names,emailAddresses" | jq .
```
*(Install `jq` if needed: `sudo apt-get install jq`)*

## Token Management

Access tokens expire. You'll need to refresh them using your refresh token.

### Refresh the Access Token When It Expires

```bash
curl -X POST \
  -d "client_id=YOUR_CLIENT_ID.apps.googleusercontent.com" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "refresh_token=REFRESH_TOKEN_VALUE" \
  -d "grant_type=refresh_token" \
  https://oauth2.googleapis.com/token
```

## Python Automation

For more robust and automated interactions, especially with token management, Python client libraries are highly recommended.

### Example: Automate People API with Python

```python
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# JSON creds you used:
CLIENT_SECRET_FILE = "~/Downloads/Desktop_app_client_secret_....apps.googleusercontent.com.json" # Update with your actual path
TOKEN_PATH = "~/Downloads/token.json" # Path to store tokens

SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]

def get_creds():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0) # or flow.run_console() for console-based auth
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds

def main():
    creds = get_creds()
    service = build("people", "v1", credentials=creds)
    results = service.people().searchContacts(
        query="QUERY_STRING", # Replace with your query
        readMask="names,emailAddresses"
    ).execute()

    for r in results.get("results", []):
        p = r["person"]
        name = p.get("names", [{}])[0].get("displayName", "N/A")
        print(f"Name: {name}")
        for e in p.get("emailAddresses", []):
            print(f"Email: {e.get('value')}")

if __name__ == "__main__":
    main()
```
*(Install dependencies: `pip install google-api-python-client google-auth-oauthlib`)*

## Key Takeaways

*   **No "Simple" API Key for Sensitive Data:** For user-sensitive data like contacts, a full OAuth 2.0 flow is mandatory. There's no simple API key.
*   **Complexity is Deliberate:** Google intentionally adds friction to APIs accessing sensitive user data due to historical abuse, privacy concerns, and regulatory compliance.
*   **Token Management is Crucial:** Access tokens are short-lived; refresh tokens are essential for seamless automation but can be revoked.
*   **Billing for Monitoring:** Google Cloud Monitoring requires billing to be enabled, even for free-tier usage.
*   **Python for Robustness:** While `curl` is great for quick tests, Python client libraries offer more robust error handling, token management, and overall maintainability for complex interactions.
