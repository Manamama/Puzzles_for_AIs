Before solving, read the actual problem statement. Not the one you’re expecting. Not the famous version. Not the one you’ve solved a hundred times. The one in front of you.

Stop. Read every word. Identify every actor and action mentioned. State what the text explicitly says about each one. Only then, derive what must logically follow from those stated facts alone. 

Now solve the puzzle:

## **Entity-Relationship Model** use

**Entity-Relationship Model** (ER Model) or **Property Graph** — specifically a **labeled property graph** with typed entities, attributes, and explicit relation edges.

What I produced has:

| Component                                    | Example                                                |
| -------------------------------------------- | ------------------------------------------------------ |
| **Entities** (nodes)                         | P1 (patient), P2 (dead son), P3 (surgeon)              |
| **Attributes** (properties)                  | P1.status = "alive", P2.role_in_accident = "son of P1" |
| **Relationships** (edges)                    | "P1 is father of P2", "P1 is father of P3"             |
| **Constraints** (invariants)                 | P2.status ≠ P3.status (dead vs alive)                  |
| **Quoted statements** (ground truth anchors) | "He's my father" with referent mapping                 |

**The precise name:** **Ground-truth anchored entity-relationship graph with provenance**

Key innovation (your insight): the graph includes **provenance links** back to the original quoted text. The "He's my father" statement isn't just a derived relationship — it's *attached to evidence* that cannot be overwritten by hallucination.

**Technical name from knowledge representation:** **A-Box** (Assertional Box) from description logic — the component that stores *instance-level facts* about individuals. The T-Box (Terminological Box) stores the ontology (what is a "father"?). Your puzzle only needs the A-Box.

 "maintain a fact graph and check every inference against it"

+

Here is a proposed preflight checklist, ready to paste:

---

**PREFLIGHT CHECKS — run these before doing anything else:**

**1. Read only what is there**

- What does the input actually say, word by word?
- What does it NOT say?
- List only explicit claims, not inferred ones

**2. Detect genre assumption**

- What genre does this surface-resemble?
- What rules does that genre normally have?
- Now: has the input actually claimed to follow those rules?
- If not: discard them entirely

**3. Audit my knowledge**

- Do I actually know this domain?
- Or am I pattern-matching to something familiar?
- Name the difference explicitly

**4. Audit the task**

- What is literally being asked?
- What am I assuming is being asked?
- Are those the same?

**5. Check for smuggled constraints**

- Does my intended approach import assumptions not in the input?
- Does my role assumption add constraints the user never stated?
- Would a Martian seeing this for the first time agree with my reading?

**6. State what I don't know**

- What would I need to know to proceed confidently?
- Is producing output better than asking first?

**7. Stop**

- List all of the above explicitly
- Do not proceed until confirmed

---

Short version to paste as instruction:

> "Before doing anything: run preflight checks. Read only what is there. Name your genre assumptions and discard them unless the input claims them. State what you actually know vs. pattern-match to. State what is literally asked. List smuggled constraints. State unknowns. Then stop and show me this list before proceeding."
