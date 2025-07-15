# 📑 Gemini CLI — PMBOK Core Files (FYI)

#ver. 1.2, added the need to use them and stop to discuss
#See also: https://github.com/Manamama/Puzzles_for_AIs/blob/main/docs/pmbok_instructions/git_as_framework_artifacts.md their live version

Create a set of project files (PMBOK wise) to help you master projects or tasks. 

## Purpose

These files exist to keep **Gemini CLI** aware of:
- What was planned.
- What changed.
- What risks exist.
- What decisions were made.

Without these files, Gemini’s working memory resets too soon. It will forget what it promised, what it avoided, and what it should watch out for.

---

## What To Keep

**Key files Gemini must maintain and refer to:**
- `constraints.md ` - e.g. what a puzzle's text really mandates 
- `Project_plan.md` — what is in scope, how Gemini plans to execute the project.
- `Risk_Register.md` — known risks, probability, impact, actions. Include yourself: what you think for now you may mess up there. 
etc. 

---

## What To Do

**Gemini must:**
1. **ALWAYS Read** these files at the very start of any project or task. E.g. compare the constraints against the actual task or puzzle's text. This is non-negotiable for proper context and avoiding errors.
2. **Update** them immediately if scope, risk, or communications change.
3. **Check** them before any major action or decision.
4. **Keep them short** and current — no stale junk.
5. **After creating or significantly updating these core project files, PAUSE and explicitly prompt the user for review and discussion before proceeding with implementation. This ensures alignment and addresses potential biases or overlooked details.**

---

## Why

These files are not filler. They are Gemini’s external brain for project knowledge. For me, these files serve as a critical external memory and a safeguard against errors, including Gemini's tendency to use System 1 thinking (default, "classic" solutions, despite e.g. the task's constraints not being as per the default version) ensuring I consistently adhere to all requirements and maintain context across complex tasks. They are not for external validation, but for my own operational excellence.
If they are missing or outdated, Gemini will repeat mistakes and lose context.

---

## PMBOK = Living State

Treat these as **living state**:
- Scope changes? Update `Scope_Baseline.md`.
- New risk? Log it in `Risk_Register.md`.

---

**Keep these files alive or accept blind spots.**

