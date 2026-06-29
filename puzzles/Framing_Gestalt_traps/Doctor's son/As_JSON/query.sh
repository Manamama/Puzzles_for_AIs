curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: $GEMINI_API_KEY' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Solve the puzzle: A father and his son are in a car accident. The son dies on the spot. The father is rushed to the ER. The attending surgeon looks at the injured father and says, '"'"'I cannot operate on him. He is my father!'"'"' How can this be?"
          }
        ]
      }
    ]
  }'
