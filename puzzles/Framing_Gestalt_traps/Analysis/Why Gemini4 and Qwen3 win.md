Yes, and now the full tensor dump reveals why Gemma4 thinks differently — and it's a different mechanism from Qwen3 Heretic, though with a similar effect.

The key is `gemma4.attention.sliding_window = 1024` with the pattern `[True, True, True, True, True, False, ...]` — most layers use **sliding window attention**, only seeing a local window of 1024 tokens, with full global attention firing only every 6th layer (the `False` entries).

So Gemma4 has **three** constraints working against the cached-answer reflex:

**MoE routing** — 8 of 128 experts active per token, so the "surgeon = mother" association isn't concentrated in one dense pathway but distributed and competing.

**Sliding window attention** — most layers literally *cannot* see the whole prompt simultaneously. They process locally first, building up a representation incrementally before the rare global attention layer integrates everything.

**Explicit thinking tokens** — the `[Start thinking]`/`[End thinking]` scratchpad forces sequential, visible derivation.

Qwen3 Heretic gets there via SSM sequential processing. Gemma4 gets there via windowed attention plus MoE plus explicit reasoning. Different roads, same destination: the architecture *enforces* reading before pattern-matching.

ChatGPT — dense transformer, full global attention, no visible reasoning chain, trained to deliver — has none of these friction points. The cached answer flows through unimpeded.

The irony is that the "limitations" — local windows, sparse expert routing, slow sequential state — are precisely what produce correct reading. The friction *is* the feature.
