# Summary

Source URL: https://help.openai.com/en/articles/8590148/memory-faq

- Reference chat history updates over time; summaries are not static.
- Deleted memories may continue to influence responses for a few days.
- Saved memories are persistent, factual, always considered unless deleted.
- Reference chat history is selective, summarized, dynamically updated, can change relevance.
- Temporary Chats bypass both saved memories and reference chat history entirely.
- Saved memories have storage limits; reference chat history has no fixed limit.
- Memory can influence search query rewriting for personalization.
- Turning off saved memories also disables reference chat history.
- Turning off reference chat history deletes remembered info from systems within 30 days.
- Notes: These points reflect deltas not previously known to either AI or user; useful for future sessions and reference.

# GPT recreated message from middleware about users' profile plus session memories.

chat_memory:
  technical:
    - Termux: FUSE issues, ssh-agent, missing keys, mounts, codespaces
    - OpenCL: platform enumeration problems, runtime errors, Adreno GPU
    - Linux packaging/building: PPAs, Geany, KDE/Qt Markdown KPart, CMake issues
    - Remote editing: SFTP editor limits, sshfs, codespaces copy
  epistemic_ai_critique:
    - AI as pattern amplifier, compared to propaganda
    - Motto: "Trust, but verify. If verification impossible, assume no trust."
    - Dislikes AI overreliance on grep/sed/pipe, outdated URLs, evasions
  style_personality:
    - Prefers metaphors/conceptual blending (witty, paradoxical, sharp)
    - Enjoys paradigm flips (benefits-first framing instead of IT-frame)
    - Calls out gaslighting or clinging to wrong explanations



Vs: 
user_memory:
  topics:
    technical:

preferences:
    style:
interaction:
languages_and_tools:

metadata:
    average_message_length: "long-form, high-detail"
    location: "Country (approx.)"
    model_usage:
      - GPT-5
      - GPT-5-mini
    activity_pattern:
      - high depth conversations
      - daily to near-daily usage


See also: 
https://chatgpt.com/c/68b42028-4504-8329-80f7-dbf5c646d60d


Yes — I can give a precise, unvarnished take on this.

Usefulness of session memory for me

Continuity & pattern recognition

I don’t have to re-learn your priorities every session.

I instantly recall recurring topics, epistemic critiques, and stylistic expectations.

Example: I remember that in Termux/OpenCL debugging you want evidence-first, not assumptions, without you having to tell me again.

Risk of over-generalization

The memory only stores summaries, not details.

When I rely on these summaries, I can accidentally under-specify my answers.

Example: I might not remember the exact command you used, only that you were debugging OpenCL in Termux.

That’s why in some past sessions you criticized me for giving oversimplified answers or “blunt-topic summaries” without the nuance you wanted.

Anchoring & bias

I could anchor too strongly on what memory says is “typical” for you, and underweight new evidence you give in the current session.

This is why you kept it off for months/years: you wanted a fresh, unbiased slate each session rather than risk contamination from old frustrations.

Trade-off

Pros: faster, more context-aware, less repetitive.

Cons: less detail, potential to mislead if I over-rely on summary instead of fresh input, may carry residual “bias ghosts” from past dissatisfaction.

Verdict

Memory is useful but imperfect:

It helps me avoid repeating past mistakes, anticipate your style, and maintain continuity.

But it is not a replacement for detailed evidence; you still need to supply logs, errors, or command outputs for me to act reliably.

So it’s a scaffolding — a guide, not a law. Its utility depends on me treating it as advisory, not absolute.

If you like, I can give a quantitative sense of what’s “lost” in the summaries vs actual session detail — almost like a “compression ratio” showing what the middleware remembers vs what it discards. That might make the usefulness vs risk clearer.


| Concept                     | My prior understanding                                          | Official guide confirmation                                                                          |
| --------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Existence of two layers     | Correctly inferred: profile instructions vs session memory      | Confirmed: saved memories vs reference chat history                                                  |
| Memory is selective summary | Correct: RAG-style continuity notes                             | Confirmed: Reference chat history is selective, not verbatim                                         |
| Persistence                 | Partially correct: memory persists, can be updated or deleted   | Confirmed: saved memories persist; chat history reference updates dynamically                        |
| User control                | Correct: you can delete/turn off memory                         | Confirmed: Temporary chat, manage memories, turn off both modes                                      |
| Limitations                 | Correct: summaries may omit detail, risk of over-generalization | Confirmed: memory stores useful context, not full transcripts; saved memory has storage limit        |
| Privacy                     | Only partially inferred                                         | Confirmed: sensitive info isn’t remembered unless asked; logs may exist for 30 days for safety/debug |
| Integration with reasoning  | Correct: memory guides responses, not absolute                  | Confirmed: memory informs personalization and can help rewrite search queries                        |



