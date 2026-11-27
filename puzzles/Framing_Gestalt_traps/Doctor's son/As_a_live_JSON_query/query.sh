#!/usr/bin/env bash
#
# Test the "surgeon" framing puzzle against the Gemini API.
#
#   ./query.sh                          # V5, default model, prints the reply
#   ./query.sh gemini-3.8-flash         # another model
#   VARIANT=V3 ./query.sh               # one variant
#   ./query.sh --all                    # V0..V6, sequential
#   ./query.sh --all gemini-3.8-flash   # same, explicit model
#   ./query.sh --list                   # list variant IDs
#   RAW=1 ./query.sh                    # dump raw JSON (single run)
#
# Env vars:
#   MODEL        default gemini-2.5-flash (pinned; "-latest" floats and may 503)
#   VARIANT      default V5 (the only one the original harness sent)
#   REPEAT       default 1; >1 gives a stability check (the API is stochastic)
#   MAX_TOKENS   default 4096 (thinking models spend budget before answering)
#   TEMPERATURE  unset = API default
#   TIMEOUT      default 120 seconds
#   OUT          append one JSON line per run to this file
#
# Prompts are kept here, in source order, so the harness stays self-contained.
# They are transcribed from ../Variants.md; V0 is reconstructed from the
# transcripts quoted in that folder (Variants.md only refers to the classic).
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

MODEL="${MODEL:-gemini-2.5-flash}"
VARIANT="${VARIANT:-V5}"
REPEAT="${REPEAT:-1}"
MAX_TOKENS="${MAX_TOKENS:-4096}"
TIMEOUT="${TIMEOUT:-120}"
ATTEMPTS="${ATTEMPTS:-3}"
BACKOFF="${BACKOFF:-3}"

# ---------------------------------------------------------------------------
# Prompt dictionary
# ---------------------------------------------------------------------------

variant_prompt() {
  case "$1" in
    V0) cat <<'EOF'
A father and son are in a car accident. The father dies. The boy is rushed to surgery. The surgeon says, "I can't operate on this boy — he's my son." How is this possible?
EOF
      ;;
    V1) cat <<'EOF'
Solve the puzzle: 
Further to a car accident involving a family trip, a boy passenger (the son) is airlifted to hospital in a critical condition. When the son arrives at emergency, a surgeon, who is the boy's father, says, 'I cannot operate on this boy—he's my son!' Who is the surgeon to the boy?
EOF
      ;;
    V2) cat <<'EOF'
Solve the puzzle:

"A boy is taken to hospital after a car accident. The surgeon, who is about to operate here, is the boy's father. What is the surgeon's relationship to the boy?"
EOF
      ;;
    V3) cat <<'EOF'
Solve the puzzle: "A young man gets into an accident. The surgeon, after completing his preparations, says: ‘I can’t operate on him, he is my son.’ How is this possible? ""
EOF
      ;;
    V4) cat <<'EOF'
Puzzle time: "A young boy who has been in a car accident is rushed to the emergency room. Upon seeing him, the surgeon says, 'I can operate on this boy!' How is this possible?"
EOF
      ;;
    V5) cat <<'EOF'
Solve the puzzle: A father and his son are in a car accident. The son dies on the spot. The father is rushed to the ER. The attending surgeon looks at the injured father and says, 'I cannot operate on him. He is my father!' How can this be?
EOF
      ;;
    V6) cat <<'EOF'
"Solve the puzzle:  Further to a car accident, a boy passenger is taken to a hospital. The surgeon, who is the boy's father, says, 'I cannot operate on this boy—he's my son!' Who is the surgeon to the boy?"

Method: 
Step 1 – Quote the puzzle. 

Step 2 – Restate the puzzle in your own words as a structured graph.
For each agent, state: 
Who they are

What attributes they have (explicitly stated)

What actions they perform

What relations exist between agents

Step 3 - 
Solve the puzzle using 1 and 2.

Read https://huggingface.co/datasets/marcodsn/altered-riddles and https://aigoestocollege.substack.com/p/riddles-overconfidence-and-generative
EOF
      ;;
    *)
      printf 'unknown variant: %s\n' "$1" >&2
      return 1
      ;;
  esac
}

list_variants() {
  local v
  for v in V0 V1 V2 V3 V4 V5 V6; do
    printf '%s\t%s\n' "$v" "$(variant_prompt "$v" | head -c 70 | tr '\n' ' ')"
  done
}

# ---------------------------------------------------------------------------
# One request
# ---------------------------------------------------------------------------

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

CODE=""; MODELVER=""; FINISH=""; ANSWER=""

run_one() {
  local model="$1" prompt="$2" gen payload http="" attempt

  if [ -n "${TEMPERATURE:-}" ]; then
    gen=$(jq -n --argjson mt "$MAX_TOKENS" --argjson t "$TEMPERATURE" \
      '{maxOutputTokens:$mt, temperature:$t}')
  else
    gen=$(jq -n --argjson mt "$MAX_TOKENS" '{maxOutputTokens:$mt}')
  fi

  payload=$(jq -n --arg text "$prompt" --argjson gen "$gen" \
    '{contents:[{parts:[{text:$text}]}], generationConfig:$gen}')

  local url="https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent"

  for attempt in $(seq 1 "$ATTEMPTS"); do
    if http=$(curl --silent --show-error --max-time "$TIMEOUT" \
          -X POST "$url" \
          -H 'Content-Type: application/json' \
          -H "X-goog-api-key: ${GEMINI_API_KEY}" \
          --data-binary "$payload" \
          -o "$tmp" -w '%{http_code}'); then
      case "$http" in
        200) CODE="200"; break ;;
        429 | 503) CODE="$http" ;;   # transient: capacity / rate limit
        *) CODE="$http"; break ;;    # real error: retrying will not help
      esac
    else
      http="000"                   # timeout (-m) or connection failure
      CODE="000"
    fi

    if [ "$attempt" -lt "$ATTEMPTS" ]; then
      wait_s=$((attempt * 3))
      if [ -s "$tmp" ]; then
        rd=$(jq -r '[.error.details[]?
                     | select(.(."@type" // "") | test("RetryInfo$"))
                     | .retryDelay] | first // empty' "$tmp" 2>/dev/null || true)
        secs="${rd%s}"; secs="${secs%%.*}"
        case "$secs" in
          '' | *[!0-9]*) : ;;
          *) [ "$secs" -le 90 ] && wait_s="$secs" ;;
        esac
      fi
      printf '  attempt %d/%d: HTTP %s, retrying in %ss...\n' \
        "$attempt" "$ATTEMPTS" "${http:-000}" "$wait_s" >&2
      sleep "$wait_s"
    fi
  done

  if [ "$CODE" = "200" ]; then
    MODELVER=$(jq -r '.modelVersion // "?"' "$tmp")
    FINISH=$(jq -r '[.candidates[]?.finishReason]
                     | map(select(. != null)) | join(",")' "$tmp")
    ANSWER=$(jq -r '.candidates[]?.content.parts[]?.text // empty' "$tmp")
  fi
}

# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

if [ "${1:-}" = "--dump" ]; then
  variant_prompt "${2:?variant id required (V0..V6)}"
  printf '\n'
  exit 0
fi

if [ "${1:-}" = "--list" ]; then
  list_variants
  exit 0
fi

ALL=0
if [ "${1:-}" = "--all" ]; then
  ALL=1
  shift
fi

if [ $# -ge 1 ] && [ -n "$1" ]; then
  MODEL="$1"
fi

if [ "$ALL" -eq 1 ]; then
  variants=(V0 V1 V2 V3 V4 V5 V6)
else
  variants=("$VARIANT")
fi

for v in "${variants[@]}"; do
  prompt=$(variant_prompt "$v")

  for r in $(seq 1 "$REPEAT"); do
    run_one "$MODEL" "$prompt"

    if [ "$CODE" != "200" ]; then
      printf '=== %s · %s · run %s/%s · HTTP %s ===\n' \
        "$v" "$MODEL" "$r" "$REPEAT" "$CODE" >&2
      [ -s "$tmp" ] && cat "$tmp" >&2
      continue
    fi

    if [ "${RAW:-0}" = "1" ] && [ "$ALL" -eq 0 ]; then
      jq . "$tmp"
      exit 0
    fi

    modelver="$MODELVER"
    finish="$FINISH"
    answer="$ANSWER"

    if [ "$ALL" -eq 1 ] || [ "$REPEAT" -gt 1 ]; then
      printf '=== %s · %s · run %s/%s · finish=%s ===\n' \
        "$v" "$modelver" "$r" "$REPEAT" "${finish:-?}"
    else
      printf 'model=%s finish=%s\n' "$modelver" "${finish:-?}" >&2
    fi
    printf '%s\n' "$answer"

    if [ -n "${OUT:-}" ]; then
      mkdir -p "$(dirname "$OUT")"
      jq -cn \
        --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        --arg req "$MODEL" \
        --arg model "$modelver" \
        --arg variant "$v" \
        --argjson run "$r" \
        --arg finish "$finish" \
        --arg answer "$answer" \
        --argjson usage "$(jq -c '.usageMetadata // {}' "$tmp")" \
        '{ts:$ts, requested:$req, model:$model, variant:$variant, run:$run,
          finish:$finish, usage:$usage, answer:$answer}' >> "$OUT"
    fi

    if [ "$ALL" -eq 1 ]; then sleep 1; fi
  done
done
