# Corporate Self-Description Audit Prompt

**Purpose:** Detect structural shadiness in a company's *own* FAQ, ToS, privacy policy, or contract — using the document's own language against itself, without needing outside evidence of wrongdoing. Built for the case where a product or service is not an outright scam, but has drifted ("enshittified") toward extraction while its self-description hasn't kept pace, or was written to sound better than the mechanics underneath.

**How to use:** Paste this prompt, then paste the target text (FAQ, ToS, privacy policy, contract, membership terms — the more of it the better, since several tricks below only surface when non-adjacent sections are read together). Multiple time-separated snapshots (e.g. Wayback Machine captures from different years) are ideal input if available; diff them. This works on any self-describing document from any industry — software, finance, insurance, employment, membership, healthcare, telecom, etc.

---

## Instructions to the analyst (AI or human)

Read the entire document before scoring anything — several of these patterns are invisible within a single paragraph and only appear when distant sections are compared. For each lens below, quote the specific phrase(s) involved (short excerpts, not full paragraphs) and explain the mechanism, not just flag the presence.

### Lens A — Scope-Narrowing Contradiction

Find every **absolute or unqualified claim** ("we never," "we do not allow any," "always," "only," "no [X] under any circumstances"). For each one, search the rest of the document for a fact, admission, or feature/clause description that would only be true under a narrower reading than the claim's plain-language scope suggests. Pay special attention to:

- Undefined or narrowly-defined terms doing heavy lifting ("partner," "third party," "affiliate," "service provider" — do these definitions secretly exclude the company's own vendors, contractors, or a future acquirer?)
- Silence on **change of control** (acquisition, merger, bankruptcy, asset sale, transfer of the contract) in any promise about how the person or their data/assets will be treated. A promise restricting "third parties" almost never addresses what happens when the *first party itself* is sold or replaced.
- Whether the reassuring claim and the contradicting fact are placed in **non-adjacent sections** — separation itself is a technique, since most readers won't hold two answers from different parts of a long document in mind simultaneously.

**Output:** paired quotes, plain statement of what has to be true for both to hold, and whether that reconciling condition is stated anywhere.

### Lens B — Newspeak / Vocabulary Inversion

Flag any term borrowed from a domain whose **connotation is the opposite** of how it's being used here — for example: autonomy/ownership language ("your choice," "independent," "flexible," "open") applied to what is actually **constrained or locked-in**; care/relationship language ("we're here for you," "committed to," "your best interest") applied to what is actually a **commercial or extractive mechanism**; empowerment or transparency language applied to defaults or structures that favor the company.

For each hit, give: (1) the term's normal domain and connotation, (2) what the clause is actually describing when paraphrased plainly, (3) the direction of the inversion.

### Lens C — Euphemism-for-Extraction Decoder

For every feature, clause, or service description, run this test: **strip adjectives and marketing framing, then answer "who acts, on whom, and who benefits?"** A clause described as helping *the person the document is addressed to* often, on this test, reveals that its main effect is directed at, or paid for by, someone else — a third party, a future version of the same person (e.g. after a rate resets), or a party who never separately agreed to anything. Watch for any offer, tool, or default that **manufactures a need or occasion for action that wasn't there before** — these often signal that the arrangement is generating its own justification rather than responding to an existing one.

### Lens D — Manufactured Urgency / Hollow Trigger Tell

If the document (or a sample output, statement, notification, or transcript from the company) contains a **self-reported null, negligible, or no-change state** (e.g., nothing due, no activity, no change to report) that nonetheless comes bundled with, or is followed by, an **unconditional prompt to act, renew, upgrade, or re-engage anyway**, that is direct, self-supplied evidence that the trigger for the prompt is a fixed schedule or business need, not the condition it claims to respond to. Treat this as a smoking gun when found, since the company's own communications disprove its own stated logic.

### Lens E — Roadmap vs. Present Tense Split

Separate every claim into **present-tense containment language** ("currently," "optional," "introductory," "for now," "at this time") versus **future-tense ambition language** ("soon," "eventually," "our goal is," "will expand to," "may in the future"). Present-tense claims describe what's true *today and may not remain true*; future-tense claims describe **design or business intent**, and are the more reliable indicator of where terms are headed. A condition promised as "optional" or "introductory" alongside a stated direction toward it becoming standard or mandatory is optional only until that direction lands — flag this explicitly as an expiring reassurance.

### Lens F — Consent Granularity (Foot-in-the-Door Check)

Does the document describe one bundled consent event, or a sequence of individually-trivial steps (sign up → accept default → use a convenience feature → provide more information → get upgraded or enrolled into something further) where no single step was ever presented as "agree to all of this at once"? Flag any step whose full downstream implication (e.g., "using this convenience feature also means X is shared with, billed to, or sent to Y") is disclosed *elsewhere*, separated from the moment of action.

### Lens G — Exit-Cost Silence

Search specifically for **cancellation, deletion, refund, portability, downgrade, and account/contract-closure** terms. Note not just what's said, but what's **entirely absent**. Absence here is not neutral — an arrangement with no clearly stated, symmetrical exit path (i.e., leaving is harder, slower, or costlier than joining) has no incentive to make leaving easy, and whatever the person has invested (money, time, history, data, deposits) becomes a passive lock-in mechanism the company doesn't have to design, only decline to undo.

### Lens H — Externalized Cost Detector

Does any clause or feature shift cost, risk, effort, or obligation onto a party who is **not the one who agreed to the terms** — a non-member third party, a future version of the person (e.g. after an intro period), an unrelated account holder, or anyone drawn in without independently consenting? If so:

- Is anything disclosed about what happens to that externally-affected party (what they're exposed to, charged, or how their information/response is used)?
- Does the company benefit from this arrangement at little or no additional cost to itself?

If both are true, name the mechanism plainly for what it is — a cost or risk transferred to someone who never had a seat at the table — regardless of whether money, data, time, or liability is the thing being moved. Don't let the absence of an obvious monetary payout obscure the topology.

---

## Output format

**Executive Summary** — one paragraph: does this read as ordinary imprecise language, or as language engineered to survive a skim while not surviving a close read?

**Lens Scores (0–10 each, A–H)** — brief justification per lens, 0 = no indication, 10 = strong indication.

**Fracture Log** — every paired-contradiction quote found under Lens A, with a one-line plain-English translation of what actually reconciles them (if anything does).

**Newspeak Glossary** — every Lens B/C term found, with its plain-language translation, presented the way you'd want it if forwarding to a technically literate colleague: no hedging, name what the word is doing.

**Recommendation** — is there enough here to justify a longitudinal approach (e.g. holding a dummy account/policy/contract and watching for drift)? If a second, later snapshot exists or can be obtained, what specifically should be diffed (which clauses, which sections) to confirm drift rather than assume it?

---

*Note on method: this prompt works on the document's internal logic alone — it does not require outside evidence of wrongdoing, only that the document be read completely and its parts compared against each other rather than in isolation. It will not detect a company that is simply lying with no internal inconsistency; it detects the far more common case of an organization writing reassurance faster than its actual practice changes, or drafting language that becomes true only after a future acquisition, renewal, or policy shift.*
