# OpenCode Free Models – Practical Cheat Sheet

*Last updated: 18 Oct 2026 – for personal reference while free DeepSeek & friends last*

See full chat: https://grok.com/c/457d5eb6-ce4c-4504-9020-17f148967984?rid=67ff7d52-f912-40f2-a3ba-879725841103 (main email, G01)

## 1. Quick Status (as of 18 Oct 2026)

- **DeepSeek V4.1 Flash Free** became free on OpenCode Zen on **15 Oct 2026**.
- Official line: “available for a limited time” – no end date published.
- Free models only work **inside the OpenCode client** (TUI / app). Direct API calls → 403 FreeTierError.
- Context on free DeepSeek: **~200k tokens** (vs 1M on paid).
- Soft rate limit (community): ~200 requests/day or short rolling windows → 429 FreeUsageLimitError.
- Free models rotate. Keep 2–3 configured.

**Model IDs to use inside OpenCode**

```
opencode/deepseek-v4.1-flash-free
opencode/glm-5.3-flash-free          # also recently free
opencode/big-pickle
opencode/mimo-v2.5-free
opencode/nemotron-3-ultra-free
```

## 2. Cost Reality Check (your numbers)

| Source                     | Tokens      | Cost      | Notes                                         |
| -------------------------- | ----------- | --------- | --------------------------------------------- |
| Your paid DeepSeek direct  | 93.4 M      | $1.85     | Excellent cache + off-peak efficiency         |
| Free OpenCode (3 machines) | **~98.1 M** | **$0**    | Termux 23.9 M + Proot 10.5 M + Ubuntu 63.7 M  |
| Estimated paid equivalent  | 98.1 M      | ~$1.9–2.5 | At *your* current blended rate (~$0.0198 / M) |
| More typical agent rate    | 98.1 M      | $8–15     | Lower cache reuse                             |

**Official DeepSeek V4.1 Flash (deepseek-flash) pricing**

- Off-peak: $0.15 input (miss) / $0.003 cache-hit / $0.60 output per 1M
- Peak (01–04 & 06–10 UTC Mon–Fri): exactly 2×

## 3. Session Efficiency Lessons (from the long analysed session)

One real session before compression:

- Final context ≈ 117 k (log) / 154 k (TUI)
- 79 model calls, 91 tool calls
- **Cumulative input processed ≈ 3.86 M tokens** (because every call re-reads the whole context)
- 97 % of that input came *after* the key answer was already known (call ~10)
- Visible thinking = 40 % of content
- 14 nearly identical PDF-parsing scripts written

**Key takeaways for debugging work**

- Free 200 k context fills faster than you expect on long agent loops.
- Re-reading tax is brutal. Once the bug is understood, force a new session.
- High thinking-token share is normal on hard debugging but expensive if it becomes paid.
- Repeated boilerplate (scripts, file dumps) is pure waste – intervene early.

## 4. Free Model Grades for Debugging Tasks

| Model                               | Grade | Notes for debugging / code work                                                                                         | Privacy / Data                                   |
| ----------------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **DeepSeek V4.1 Flash Free**        | A     | Currently the strongest free coding model available. Good tool use, solid reasoning. 200 k context is the main limiter. | May use data to improve model during free period |
| GLM 5.3 Flash Free                  | A-    | Very close; sometimes preferred for certain coding styles. Also 200 k.                                                  | Similar                                          |
| Big Pickle                          | B+    | Stealth model, often surprisingly capable. Good fallback.                                                               | May train                                        |
| MiMo-V2.5 Free                      | B     | Decent but usually a step behind DeepSeek/GLM on hard bugs.                                                             | May train                                        |
| Nemotron 3 Ultra Free               | B-    | NVIDIA trial. Usable but “do not submit personal/confidential data”.                                                    | Logged by NVIDIA                                 |
| Others (Space Bunny, LongCat, etc.) | C–B   | Rotate in/out. Test when they appear.                                                                                   | Varies – some zero-retention                     |

**Practical ranking for your use-case (debugging)**  

1. DeepSeek V4.1 Flash Free  
2. GLM 5.3 Flash Free  
3. Big Pickle  
4. Everything else as temporary fallbacks

## 5. Daily Tips While Free Lasts

- Keep at least two free models configured. Switch the moment one feels slow or rate-limited.
- Watch context size in the TUI. Crossing ~140–150 k is the danger zone on free DeepSeek.
- Prefer short, focused sessions over one giant agent run.
- Use Plan mode first on complex bugs, then switch to Build.
- Use `opencode stats --days 30 --cost --models` and `opencode stats --all --cost`
- Local `opencode stats` (or `npx ccusage@latest daily`) is your only reliable usage view for free models – there is no cloud dashboard.
- When free capacity gets tight or a model disappears, fall back to:
  - Your direct DeepSeek key (already very efficient for you)
  - OpenRouter
  - OpenCode Go ($10/mo) if you want a simple subscription with high DeepSeek allowance

## 6. Privacy Snapshot (Zen free models)

- DeepSeek V4 Flash Free, Big Pickle, MiMo: data **may be used to improve the model** during the free period.
- Nemotron free: trial only – avoid personal/confidential code.
- Always check the current Zen privacy section before pasting sensitive material.

---

*Keep this file handy. Free tiers rotate without much warning.*