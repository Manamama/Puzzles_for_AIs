# scam-detector

## Description
A forensic diagnostic tool designed to evaluate personal communication (transcripts, emails, chats) to identify structural patterns of emotional and reality hijacking indicative of sophisticated financial exploitation (e.g., romance scams, "oil rig" narratives).

## Detection Framework: The Symmetry-Bound Analysis
This skill distinguishes between genuine human intimacy (messy, reciprocal, high-entropy) and scripted manipulation (asymmetric, urgent, low-entropy) by evaluating three core metrics:

1.  **Symmetry Violation (The Reciprocity Test):**
    *   **Goal:** Determine if the exchange of information, vulnerability, and effort is bidirectional.
    *   **Indicator:** High-volume victim disclosure coupled with high-entropy consumption/minimal reciprocation by the actor (e.g., actor maintains a "third space" of forced inaccessibility).
2.  **Verification Resistance (The "Gatekeeper" Test):**
    *   **Goal:** Measure the response to external reality-testing.
    *   **Indicator:** Hostile or crisis-driven pivots ("Don't tell your family," "This is just for us," "Video calls break my privacy/work rules") in response to legitimate attempts at verification.
3.  **Transactional Velocity (The "Forced-Choice" Test):**
    *   **Goal:** Identify the speed at which the narrative accelerates toward a demand for goods, money, or sensitive logistical cooperation.
    *   **Indicator:** Frequency of "forced-choice" scenarios (ship this now, send money today) exceeding the verified timeline of established trust.

## Operational Workflow

### 1. Data Ingestion
Acquire communication logs via:
*   **Audio/Video Transcripts:** Process with `WhisperX` to generate `.srt` files.
*   **Email Threads:** Export via `Gmail` CLI or GWS integrations.
*   **Chat Logs:** Export via `Google Chat` CLI or `adb-control-gemini` (if local).

### 2. Analysis Pattern
Run the transcript/log against the symmetry framework:
*   **Structural Parsing (`jq`/`grep`):** Convert logs to JSON-like structures for analysis.
*   **Fracture Identification:** Search for instances where the actor contradicts previously established "facts" in the conversation (e.g., claimed unavailability vs. later action).
*   **Sentiment vs. Logic Analysis:** Evaluate whether the actor uses emotional appeals to silence logical follow-up questions.

## Ethical Guardrail
**Disclaimer:** This tool is an analytical aid, not a definitive moral arbiter. Human interaction, especially in the early stages of passion, can mirror scam-like intensity (e.g., idealization, rapid pacing). **Never** treat a high "scam risk score" as evidence of guilt. Always prioritize empathetic verification over automated judgment.
