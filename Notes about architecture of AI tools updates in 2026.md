# Notes on updates to Gemini tools

Things have changed since these (messy by now) guides were written. Most of the guides have been formalized by other parties into below. 

Below how things are being done A.D. 2026 :

The hierarchy becomes clearer if you separate **three different concerns** the CLI architecture is solving:

1. **How the model gets new abilities**

2. **How the model gets specialized instructions**

3. **How those pieces are distributed and installed**

Those correspond to **MCP → Skills → Extensions**.

But the crucial thing: **they operate at different layers of the agent system.**

---

# The real structure (bottom → top)

Think of the Gemini CLI stack like a computer system.

```
Extension (distribution package)
   ├── Skills (procedural knowledge)
   ├── MCP servers/tools (capabilities)
   ├── slash commands
   └── config/context
```

Now let’s unpack each layer.

---

# 1. MCP — actual capabilities (the hands)

**MCP = Model Context Protocol**

This is the **tool execution layer**.

It lets the model interact with **external software or APIs**. ([Gemini CLI](https://geminicli.online/docs/extensions/?utm_source=chatgpt.com "Extensions & MCP | Gemini CLI Documentation | Gemini CLI"))

Examples:

- GitHub API

- databases

- web search

- Kubernetes

- Stripe

- local scripts

In practice:

```
Gemini → MCP tool → external program → result → Gemini
```

Example MCP server:

```
github-mcp-server
```

This exposes tools like:

```
create_issue()
list_prs()
read_repo_file()
```

Without MCP:

Gemini is **just text generation**.

With MCP:

Gemini becomes an **agent that can act**.

So MCP is **capability infrastructure**.

---

# 2. Skills — procedural intelligence (the brain manual)

A **Skill** is basically:

```
structured prompt + workflow + optional assets
```

It’s stored as:

```
SKILL.md
```

Example skill:

```
security-audit
```

It might contain instructions like:

```
1. Check OWASP Top 10 vulnerabilities
2. Look for secrets in code
3. Verify authentication flows
```

When Gemini detects a relevant request, it **activates the skill** and loads its instructions. ([Gemini CLI](https://geminicli.com/docs/cli/skills/?utm_source=chatgpt.com "Agent Skills | Gemini CLI"))

Important characteristics:

- **no new capabilities**

- **only new reasoning workflows**

So skills are essentially:

```
reusable expert prompt packages
```

Examples:

| Skill          | What it changes            |
| -------------- | -------------------------- |
| security-audit | how the model reviews code |
| terraform-plan | how it plans infra changes |
| rust-migration | how it converts C++ → Rust |
| docs-writer    | how it writes docs         |

Skills can **tell the model how to use MCP tools**, but they don’t provide the tools themselves.

---

# 3. Extensions — installation unit (the shipping container)

An **Extension** is just a **bundle**. ([Gemini CLI](https://geminicli.com/docs/core/concepts/?utm_source=chatgpt.com "Core concepts | Gemini CLI"))

It packages things together so users can install them easily.

Typical extension contents:

```
extension/
  mcp_servers/
  skills/
  commands/
  GEMINI.md
```

So installing one extension might add:

- 3 MCP tools

- 2 Skills

- 5 slash commands

- extra context rules

Example:

```
supabase-extension
```

Might include:

```
MCP: supabase-db
MCP: supabase-auth
Skill: database-migration
Skill: schema-audit
Command: /deploy
```

So extensions are basically:

```
npm packages for Gemini CLI capabilities
```

---

# Why these are separate (important design reason)

The separation solves **context-window pressure** and **modularity**.

If everything were just one giant plugin:

- the model would need to load everything every time

- context would explode

Instead the system works like this:

```
Extension installed
   ↓
Skills visible but not loaded
   ↓
Model detects relevant skill
   ↓
Skill activated
   ↓
Skill may call MCP tools
```

Only what’s needed gets loaded.

This is called **progressive context disclosure**. ([Gemini CLI](https://geminicli.com/docs/cli/skills/?utm_source=chatgpt.com "Agent Skills | Gemini CLI"))

---

# The simplest mental model

Forget the official analogy.

Use this one:

| Layer     | What it actually is    |
| --------- | ---------------------- |
| MCP       | executable tools       |
| Skill     | prompt-driven workflow |
| Extension | installable bundle     |

Or even shorter:

```
MCP = tools
Skill = instructions
Extension = package
```

---

# Concrete example

Suppose you install:

```
kubernetes-dev-extension
```

Inside it:

### MCP

```
kubectl-mcp
```

Tools:

```
list_pods()
deploy_service()
delete_cluster()
```

### Skills

```
k8s-debug
```

Instructions:

```
When debugging Kubernetes:
1. check pod status
2. check logs
3. inspect deployment
4. propose fix
```

### What happens during a prompt

User asks:

```
Why is my pod crashing?
```

Gemini:

1. detects **k8s-debug skill**

2. activates it

3. uses **kubectl MCP tool**

4. reads logs

5. produces diagnosis

Skill = reasoning  
MCP = action

---

# Why your intuition (“could be one tool”) is understandable

Because historically **AI plugins combined all three**.

Older systems:

```
plugin = tools + prompts + config
```

Gemini CLI split them into layers so that:

- tools can be reused across skills

- skills can orchestrate many tools

- extensions can distribute everything cleanly

This is basically **microservices for AI capabilities**.

---

If you want, I can also show something **much more revealing** that Gemini CLI documentation doesn’t explain well:

Why **Skills are essentially structured prompt injections**, and why Google separated them from `GEMINI.md`. That design choice reveals a lot about how they manage **agent context control and prompt hierarchy**.

+

Your instinct is correct. None of these layers were *technically necessary* for early shell-agent workflows. Before this architecture existed, agents already functioned by doing something like:

```
model → writes shell command → CLI executes → stdout → model reads → repeat
```

Systems like **AutoGPT**, **LangChain agents**, **ShellGPT**, or early **ReAct-style agents** worked exactly this way. The model inferred tools by reading docs and emitting commands. No MCP required.

So the honest answer to “why all this?” is not “because the agent couldn’t do it otherwise.”  
The real reasons are **control, reliability, and ecosystem packaging**.

The architecture solves problems that show up when you scale beyond one user and a few shell commands.

---

# 1. Why MCP exists (despite shell agents already working)

Your shell approach is basically **free-form tool use**:

```
model guesses command syntax
```

Example:

```
curl https://api.github.com/repos/foo/bar
```

This works—but it has three structural problems.

### Reliability problem

Models hallucinate CLI flags constantly.

Example:

```
git push --force-with-lease=origin
```

That flag does not exist.

MCP fixes this by giving the model **a typed function interface**:

```
create_issue(repo, title, body)
```

Instead of generating arbitrary shell text, the model must choose a defined tool with defined parameters.

So MCP is basically:

```
shell improvisation → structured API calls
```

It's the same shift that happened when OpenAI introduced **function calling**.

---

### Safety problem

With shell execution the model can output:

```
rm -rf /
```

If the agent auto-executes, you're cooked.

MCP tools are **sandboxed capabilities**. The model cannot escape the defined tool surface.

---

### Context problem

With shell usage, the model must remember:

```
kubectl logs podname --namespace=foo
```

With MCP it only remembers:

```
get_logs(pod)
```

The complexity moves **out of the prompt and into the tool implementation**.

That reduces prompt size and error rate.

---

So MCP is essentially:

```
LLM shell hacking → RPC interface
```

It’s the **same evolution we saw in operating systems**:

```
raw syscalls → libraries → frameworks
```

---

# 2. Why Skills exist (when models can read docs)

You're also right that models can read manuals.

But that approach breaks down because **LLMs don't plan consistently**.

Without skills:

```
User prompt
↓
Model improvises reasoning
↓
Result varies wildly
```

Sometimes the model:

- uses tools

- ignores tools

- does steps out of order

- forgets safety checks

A **Skill** forces a workflow.

Think of it as a **reusable reasoning scaffold**.

Example:

```
Security audit skill

1 scan dependencies
2 check secrets
3 inspect auth
4 summarize risks
```

Without the skill:

The model might just skim the code and say:

> looks fine.

With the skill:

It follows a structured procedure.

So Skills solve:

```
inconsistent reasoning
```

They are essentially **codified chain-of-thought workflows**.

Yes, they are basically **fancy prompt templates**.

But they also support:

- lazy loading

- versioning

- packaging

---

# 3. Why Extensions exist (when you could just install tools)

This one is the most mundane.

Extensions exist for **distribution**.

Instead of installing:

```
github MCP
github skill
github commands
github config
```

You install:

```
github-extension
```

Which bundles everything.

This is the same reason we have:

- npm packages

- VSCode extensions

- browser extensions

It's not a technical necessity. It's **ecosystem infrastructure**.

---

# 4. The deeper reason: AI tool ecosystems

The real goal isn't helping *you*.  
It's enabling **third-party ecosystems**.

Google wants developers to publish things like:

```
stripe-extension
postgres-extension
kubernetes-extension
```

Each containing:

```
MCP server
skills
agent workflows
commands
```

So Gemini becomes a **platform**, not just a model.

This mirrors what happened with:

- VSCode extensions

- browser extensions

- Kubernetes operators

---

# 5. The brutal truth: your approach still works

Your original architecture:

```
model + shell
```

is still the **most flexible system**.

In fact many power users prefer it because:

- zero abstraction

- no tool constraints

- maximum improvisation

But it has downsides:

```
high hallucination rate
high variance
high risk
```

MCP/Skills/Extensions trade **freedom for predictability**.

---

# 6. The hidden architectural shift

What you're seeing is the transition from:

```
LLM as clever autocomplete
```

to

```
LLM as operating system scheduler
```

The modern stack looks like this:

```
LLM
↓
skills (reasoning programs)
↓
tools (MCP)
↓
external systems
```

Which is much closer to a **microservice orchestration layer** than a chatbot.

---

# The short answer to your question

You don't *need* any of this.

They exist because large organizations want:

- predictable agent behavior

- safer tool access

- reusable workflows

- an installable ecosystem

Your shell-driven agents work because the model is smart enough to improvise.

These layers exist because **improvisation doesn't scale to millions of users**.

---