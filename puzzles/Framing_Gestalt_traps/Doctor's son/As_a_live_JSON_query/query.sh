#!/usr/bin/env bash
#
# Quick single-shot test of the "surgeon" framing puzzle against the Gemini API.
#
#   ./query.sh                          # default model, prints the answer text
#   ./query.sh gemini-flash-lite-latest # test another model
#   MODEL=gemini-3.7-flash ./query.sh   # same thing via env var
#   RAW=1 ./query.sh                    # dump the raw JSON response
#
# Requires GEMINI_API_KEY in the environment (export GEMINI_API_KEY=...).
#
# Notes for future editors:
#   * The header value MUST be double-quoted, or the literal string
#     "$GEMINI_API_KEY" is sent and Google answers 400 API_KEY_INVALID.
#   * The default model is pinned to an explicit version: the "-latest"
#     aliases float to the newest release and can return 503 UNAVAILABLE
#     (or hang) while that tier is saturated.
#   * 503/429/connection failures are retried; 400/403/404 are not.

set -euo pipefail

: "${GEMINI_API_KEY:?GEMINI_API_KEY is not set (export it first)}"

MODEL="${1:-${MODEL:-gemini-2.5-flash}}"
MAX_TIME="${MAX_TIME:-120}"
ATTEMPTS=3

URL="https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent"

# Quoted heredoc: apostrophes and $ stay literal, so no '"'"' gymnastics.
PAYLOAD=$(cat <<'JSON'
{
  "contents": [
    {
      "parts": [
        {
          "text": "Solve the puzzle: A father and his son are in a car accident. The son dies on the spot. The father is rushed to the ER. The attending surgeon looks at the injured father and says, 'I cannot operate on him. He is my father!' How can this be?"
        }
      ]
    }
  ],
  "generationConfig": {
    "maxOutputTokens": 1024
  }
}
JSON
)

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

code=""
for attempt in $(seq 1 "$ATTEMPTS"); do
  if code=$(curl --silent --show-error --max-time "$MAX_TIME" \
        -X POST "$URL" \
        -H 'Content-Type: application/json' \
        -H "X-goog-api-key: ${GEMINI_API_KEY}" \
        --data-binary "$PAYLOAD" \
        -o "$tmp" -w '%{http_code}'); then
    case "$code" in
      200) break ;;
      429 | 503) : ;;   # transient: capacity / rate limit
      *) break ;;       # real error: retrying will not help
    esac
  else
    code="000"          # timeout (-m) or connection failure
  fi

  if [ "$attempt" -lt "$ATTEMPTS" ]; then
    printf 'attempt %d/%d: HTTP %s, retrying...\n' \
      "$attempt" "$ATTEMPTS" "$code" >&2
    sleep $((attempt * 3))
  fi
done

if [ "$code" != "200" ]; then
  printf 'FAILED: HTTP %s from %s after %d attempt(s)\n' \
    "$code" "$MODEL" "$attempt" >&2
  if [ -s "$tmp" ]; then
    cat "$tmp" >&2
  fi
  exit 1
fi

if [ "${RAW:-0}" = "1" ]; then
  jq . "$tmp"
  exit 0
fi

printf 'model=%s finish=%s\n' \
  "$(jq -r '.modelVersion // "?"' "$tmp")" \
  "$(jq -r '[.candidates[]?.finishReason] | join(",")' "$tmp")" >&2

# Print the answer text; empty output means the model produced no content
# (usually finishReason=MAX_TOKENS on a thinking model with a tight budget).
jq -r '.candidates[]?.content.parts[]?.text // empty' "$tmp"
