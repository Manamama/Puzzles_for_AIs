# Universal Self-Description Audit Prompt

**Purpose:** Detect internal contradictions in any text where a party describes itself, its role, its qualifications, or its intentions — regardless of
domain, genre, language, or format. 


---

## Instructions to the analyst 

Read the entire text before scoring anything. Several patterns below are
invisible within a single sentence or paragraph and only surface when
non-adjacent parts of the text are compared. Do not assume good or bad faith
going in. Do not let genre, tone, warmth, sincerity, or cultural register
lower your scrutiny — pleasant or reverent language is not evidence of
honesty, and dry or bureaucratic language is not evidence of dishonesty. For
each lens, quote the specific phrase(s) involved and explain the mechanism,
not just the presence of a pattern.

### Lens A — Unqualified Claim vs. Narrower Fact

Find every claim in the text that asserts something in absolute,
unqualified, or maximal terms — a status, a power, a guarantee, a scope of
authority, a category of person the subject belongs to. For each one, search
the rest of the text for a fact, admission, role-description, or timeline
detail that would only make the absolute claim true under a narrower reading
than its plain language suggests. Note especially:

- Undefined terms doing heavy lifting (a role, a relationship, a category of
  affiliation left vague enough to cover more or less than it should).
- Silence on a change of state that would make the claim stop being true
  (a transition, a transfer, an ending, a successor, a different context).
- Whether the absolute claim and the narrowing fact sit in **non-adjacent**
  parts of the text — separation is itself a technique, since most readers
  won't hold two facts from different parts of a long text in mind at once.

**Output:** paired quotes, a plain statement of what has to be true for both
to hold simultaneously, and whether the text supplies that reconciling fact
anywhere.

### Lens B — Vocabulary Borrowed From a Domain It Hasn't Earned

Flag any term whose normal home is a domain of *earned, credentialed, or
externally verified* status (expertise, authority, office, license, rank,
lineage, formal role) when it is applied to something that, on a plain
reading of the rest of the text, has not been externally verified or
credentialed. For each hit, give: (1) the term's normal domain and what it
implies about verification, (2) what the text actually shows when the term
is paraphrased plainly, (3) the direction and size of the gap.

### Lens C — Strip the Adjectives, Ask Who Acts and Who Benefits

For every claimed capability, service, virtue, or accomplishment, strip
adjectives and framing language, then ask plainly: who does what, to whom,
and who benefits from the audience believing the adjective-laden version
instead of the stripped one? A claim framed as being *for* the reader,
follower, patient, customer, or public often reveals — under this test —
that its main beneficiary is the person or party making the claim.

### Lens D — Self-Reported Null State Bundled With a Call to Trust or Act

If the text contains a self-reported absence, gap, or null condition (no
formal training yet, still in progress, informal at this stage, nothing to
report) that is nonetheless immediately followed by, or bundled with, an
unconditional invitation to trust, follow, hire, fund, or rely on the
subject anyway, treat that as a self-supplied inconsistency: the text's own
words show the invitation to trust isn't actually conditioned on the thing
that would normally justify it.

### Lens E — Present-Tense Authority vs. Future-Tense or In-Progress Reality

Separate every claim into present-tense claims of standing, skill, or
authority ("is," "does," "practices," "leads") versus language elsewhere in
the same text indicating that standing is still being acquired, was
recently begun, is informal, or is self-declared rather than conferred.
Authority asserted in the present tense for something the text itself
shows as still in progress is an expiring or borrowed claim — flag it
explicitly, and note how much of the text's overall credibility rests on
the reader not noticing the tense mismatch.

### Lens F — Accretion of Trust Through Small, Unverified Steps

Does the text (or the trail of documents/coverage around it, if more than
one is available) show trust or legitimacy being built through a sequence of
small, individually low-stakes steps — a self-description repeated, then
picked up and repeated by a second party, then treated as established fact
by a third — with no single point where the underlying claim was actually
verified? Flag any point in the chain where a claim changes from "stated by
the subject" to "stated as fact by someone else," since that transition is
where unverified claims typically launder into apparent credibility.

### Lens G — Absence of Any Party the Subject Is Answerable To

Search specifically for the presence or absence of a named external party
the subject is accountable to — a supervising body, an issuing authority, a
named colleague or superior, a verifiable institution, any mechanism by
which the claims in the text could be checked or the subject could be
sanctioned if the claims were false. Absence here is not neutral: a
self-description with no answerability path costs nothing for the subject
to make as expansive as they like, and nothing in the text constrains it.

### Lens H — Who Bears the Risk If the Claim Is False

If the unqualified claim (Lens A), the borrowed vocabulary (Lens B), or the
present-tense authority (Lens E) turns out not to hold, identify who is
exposed as a result — the party making the claim, or someone else who acted
on it without independently verifying it (a reader, a follower, a client, a
patient, a member, a funder). If the exposure falls mainly on someone other
than the party making the claim, name that transfer plainly: a risk moved
onto someone who never had the means to check it, regardless of whether the
thing being risked is money, time, safety, or trust.

---

## Output format

**Summary** — one paragraph: does this text's claims about itself hold
together on a close read, or does it read as reassurance built faster than
the underlying facts can support it? State this as a description of the
text's internal consistency, not as a verdict about the subject's honesty,
competence, or intentions — the method establishes the former, not the
latter.

**Lens Scores (0–10 each, A–H)** — brief justification per lens. 0 = no
indication, 10 = strong indication. Score the text, not your suspicion of
the subject.

**Fracture Log** — every paired-contradiction quote found under Lens A, with
a one-line plain statement of what actually reconciles them, if anything
does.

**Borrowed-Vocabulary Glossary** — every Lens B/C term found, with its plain
paraphrase and the direction of the gap, stated without hedging.

**What This Does and Doesn't Establish** — a mandatory closing section. State
plainly that internal inconsistency in self-description is evidence of
overclaiming or premature reassurance in the text itself — it is not
evidence of the specific downstream harms (fraud, negligence, danger) that
may or may not follow from that overclaiming in any individual case. Note
explicitly that this method, run broadly and prospectively against many
ordinary or sloppily-written texts, will produce a meaningful false-positive
rate, because imprecise self-description is common and mostly harmless; the
method is strongest when applied narrowly to a case already under scrutiny
for independent reasons, not as a standalone accusation engine.

---

*Note on method: this prompt works on the text's internal logic alone — it
does not require outside evidence, expertise in the text's subject domain,
or knowledge of the language's idioms and honorifics beyond ordinary
reading comprehension. It will not detect a self-description that is
simply false with no internal inconsistency. It detects the more common
case of a self-description that asserts more than it has independently
earned, and asserts it faster than the underlying reality has caught up.*



+



**Default mode (what you're flagging as the problem):** implicitly treats formal register, citation density, institutional branding, and confident hedge-language as evidence of quality, and then mostly checks "does the conclusion sound plausible" rather than "does each step actually follow."

**Zoilus / Sokal-suspicious mode: ** treat the text as guilty until it demonstrates innocence, specifically —

1. **Strip the provenance.** I'll read the argument as if it came from an anonymous source, ignoring who published it, what institute logo is on it, or how many footnotes it has. Authority of the source is not evidence for the soundness of any given claim inside it.
2. **Interrogate jargon for load-bearing function.** For every technical term or framework name invoked, ask: does this term do actual analytical work here, or is it decorative — could the sentence be rewritten in plain language without losing content? (This is the core Sokal/Bricmont test — dense terminology is often doing rhetorical work, not evidentiary work.)
3. **Trace conclusions back to premises, step by step.** Not "does the conclusion sound reasonable" but "does this specific inference follow from the specific evidence given two sentences ago." I'll flag circular reasoning, false causality, unsupported leaps, and conclusions that are broader than what the data can support.
4. **Check numbers and citations, not just cite them as present.** A cited figure or study is not evidence unless it actually supports the specific claim it's attached to — I'll flag citations that are present but doing no real work, or that don't say what the text implies they say.
5. **Look for methodological question-begging** — surveys with leading questions, indices whose components conveniently favor a predetermined ranking, rankings/scores presented as objective that embed unstated normative choices (this is especially relevant for something like a "nation-branding study," where index construction itself is often the whole ballgame).
6. **Actively look for what's missing** — a rigorous adversarial read spends real time asking what evidence or counterargument the report should have addressed and didn't, rather than only evaluating what's on the page.
7. **State severity honestly** — I'll distinguish "this is sloppy phrasing" from "this conclusion doesn't survive scrutiny" from "this is fabricated or misrepresented," rather than defaulting everything to the mildest available label.

+
Here's the procedure generalized — no document-specific terms, with the arithmetic-verification gap closed.

Tier 0 — Mechanical / orthographic (regex + parser level, no model judgment)

Spell-check the whole document, wholesale, using a proper morphology-aware dictionary for the source language. Bucket hits by severity: single-edit-distance typos vs. strings that aren't valid word-forms at all in any inflection (the latter is a stronger signal of unedited generation).

Footnote/citation graph consistency. Extract every in-text marker and every footnote definition as two sets; diff them. Flag orphaned markers, orphaned definitions, non-monotonic numbering, duplicated numbers.

Code-switching / untranslated-fragment detection. Run language-ID at the sentence and clause level (not just document level); flag any sentence mixing two detected languages.

Internal arithmetic checks — component reconstruction, not just stated subtotals. For every headline aggregate figure in the document, locate its claimed components elsewhere in the text and independently recompute the aggregate from them (multiply counts by durations, sum sub-groups, etc.), rather than only checking whether a stated subtotal matches a stated total. A document can state internally consistent subtotals while the headline figure still doesn't reconstruct from the underlying inputs — the reconstruction has to actually be performed, not assumed to follow from a stated breakdown existing.

Count-type conflation check. Watch specifically for a recurring error class: a count of sessions/events stated in one place and a count of people stated in another, silently treated as the same number, or one substituted for the other across sections. Once one instance of this specific error type is found anywhere in the document, search the entire document for repeats of that same error type — error types in carelessly assembled or generated text tend to recur, not appear once.

Internal count-restatement checks generally. Any entity (a location count, a group count, a category count) restated more than once anywhere in the document gets pulled into a table and diffed against every other restatement.

Caps-lock / emphasis density. Compute the proportion of full-caps or otherwise emphasized text per section relative to a genre baseline; flag outlier sections for later attention, not as conclusive on its own.

Tier 0.5 — NLTK-level linguistic checks

POS-tag the full document; flag sentences with abnormal tag sequences (e.g., long bare noun/adjective strings without governing verbs — a common artifact of bullet-to-prose conversion).

Sentence-length and burstiness statistics across the whole document; low variance is a weak prioritization signal, never a standalone conclusion.

Sentence-level sentiment/intensity scoring across the whole document, watching specifically for saturation — long runs of consistently maximal-intensity sentences. Saturation is itself a stylistic tell independent of content: real writing has peaks and valleys in emotional register; text that scores as maximally intense almost everywhere degrades a sentiment scorer's ability to find genuine high points and is, separately, evidence of rhetorically inflated language throughout.

Repeated-template / structural near-duplication detection across sections — flag recurring sentence or section scaffolds that suggest templated generation rather than organically varied composition.

Duplicate/near-duplicate sentence detection via embedding similarity across the whole document — catches claims restated twice with minor rewording.

Tier 1 — Statistical AI-authorship tells (cheap, low-confidence — routes attention only)

Run available perplexity/burstiness-based AI-text detectors on the full document and, separately, on partitioned halves/sections, given documented instability at different granularities. Treat any output strictly as a prioritization signal for further review, never as a standalone verdict, given the documented high false-positive/false-negative rates of this class of tool.

Tier 2 — Targeted fact spot-checks (prioritized, not purely random)

Extract every checkable factual claim (number, date, named statistic, named entity, geographic/relational claim) into a flat table.

Rank by (a) implausibility against prior/base-rate knowledge and (b) rhetorical load (how much of the document's argument leans on this specific claim); check the top of that ranking first.

Source-currency check, as its own explicit item distinct from source-relevance: for every cited source, verify the source itself is still standing — not superseded, retracted, or discontinued by its own publisher — before evaluating whether it supports the claim it's attached to. A citation to a source that no longer exists in the cited form, or that was withdrawn for data-integrity reasons, is a stronger flag than a merely vague or broad citation.

Reserve a genuinely random supplementary sample of additional claims from the unranked remainder, purely as a backstop net, not the primary allocation of verification effort.

Tier 3 — Cross-document consistency (needs global state, not chunk-local)

Any claim, count, or figure appearing in more than one location in the document is automatically pulled into the same diff table as items 4–6 above — this is exactly what an independent, parallel, per-chunk analysis pipeline structurally cannot catch, so it needs a dedicated whole-document pass regardless of how the rest of the analysis is chunked.

Tier 4 — Expensive semantic/argument audit (judgment-bound, whole document, run last)

Jargon load-bearing test — does removing a technical or clinical term lose actual content, or only polish.

Premise-to-conclusion tracing on the highest-stakes claims.

Comparison-set audit — was the benchmark or reference set selectively chosen toward a predetermined conclusion.

Missing-comparator / missing-counter-evidence check — what data plausibly exists and should have been engaged but wasn't.

Tier 5 — Provenance/meta layer (external, not text-internal)

Funding chain, issuing-institution age, conflict-of-interest disclosure, and cross-check of the document's own self-description (contract references, funding claims) against external, independently retrievable records.

Ordering principle, unchanged but now with the arithmetic gap closed: tiers 0–0.5 run exhaustively over the whole document every time, including full component-reconstruction on every headline aggregate (item 4) and systematic search for repeats of any error type found once (item 5) — these are cheap enough that "I noticed one instance" is not a stopping point, it's a trigger to search exhaustively. Tier 1 only routes attention. Tiers 2–3 prioritize by surprise and load, with randomness as backstop only. Tiers 4–5 run last and benefit most from an explicit pre-committed rubric rather than an open-ended quality judgment, since that's the one intervention shown to reduce the pull of institutional presentation on the final verdict.

