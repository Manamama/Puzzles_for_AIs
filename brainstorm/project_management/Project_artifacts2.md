#Ver. 2.0

# 🧭 AI Coding Project Strategy Tracker

---

## 📁 File Structure Overview

```
ai-strategy-tracker/
├── PROJECT_PLAN.md
├── RISK_REGISTER.md
├── ASSUMPTIONS.md
├── DECISION_LOG.md
└── TEST_MODULES/          # Optional subfolder for variant code snippets
```

---

## 📄 `PROJECT_PLAN.md`

```markdown
# Project Plan

## Objective
Brief 1–2 sentence description of the system or function to be developed.

## Success Criteria
- Functional goals (e.g. "produces correct spiral")
- Aesthetic or emergent criteria (e.g. "preserves whitespace")
- Efficiency/clarity expectations

## Scope Boundaries
- What will *not* be handled (e.g. performance optimizations)
- Versions not targeted (e.g. even-sized grids)
```

---

## ⚠️ `RISK_REGISTER.md`

```markdown
# Risk Register

| ID  | Risk Description                          | Type      | Mitigation Plan                        | Status   |
|-----|--------------------------------------------|-----------|----------------------------------------|----------|
| R1  | Logic may overfill grid                   | Logic     | Fork growth rule; limit tiles filled   | Active   |
| R2  | Spiral halts prematurely on boundary hit  | Behavior  | Test 3 variants of boundary handler    | Active   |
| R3  | Output aesthetics unclear                 | Design    | Compare visual diffs with target       | Mitigated|
```

---

## 🌱 `ASSUMPTIONS.md`

```markdown
# Assumptions Log

- A1: Starting tile is at (n//2, n//2)
- A2: ~50% fill = floor(n² / 2) + 1
- A3: Movement follows R→D→L→U
- A4: Tile state changes are only made on in-bound positions

Note: Any invalidated assumption must be re-evaluated in decisions.
```

---

## 🔁 `DECISION_LOG.md`

```markdown
# Decision Log

## [2025-06-28]

### Spiral Step Growth Rule
- Tried Variant A: +1 after every turn ✅ worked
- Tried Variant B: +1 every 2 turns ❌ too dense
- Will continue with A for future refinements

### Termination Condition
- Forked 3 boundary handlers (return / continue / no check)
- Variant A produced clean result, avoiding infinite loops
```

---

## 📁 `TEST_MODULES/`

*Optional folder where code variants (snippets or files) are stored for quick A/B testing.*

Example contents:
```
TEST_MODULES/
├── step_growth_variant_A.py
├── boundary_handler_variant_B.py
```

These are called from minimal test harnesses or visual diff tools.

---

## 📌 How to Use This System

1. **Start with `PROJECT_PLAN.md`** — clarify what the AI is solving.
2. **Fill in `ASSUMPTIONS.md`** — capture logic defaults *before coding*.
3. **Log all uncertainties in `RISK_REGISTER.md`** — review before execution.
4. **Use `DECISION_LOG.md`** to track every tested branch or hypothesis.
5. **Optionally use `TEST_MODULES/`** to hold isolated experiments.
6. **Update these files live** during code session (Gemini can use `os.write()` etc.).
7. **Review logs before each iteration** to avoid forgotten branches or assumptions.

---

> Think of these as a cognitive prosthetic: a persistent thread through non-linear exploration. A good tracker’s job is not just to list the known fragile spots, but to promote fresh surprises into named risks immediately when they sting you.

It’s the same thing as “incident → root cause → new risk → new branch.”
