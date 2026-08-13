# Universal Self-Description Audit Prompt

**Purpose:** Detect internal contradictions in any text where a party describes
itself, its role, its qualifications, or its intentions — regardless of
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
