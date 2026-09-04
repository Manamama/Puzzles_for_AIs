Keywords: valence ratio, substitution invariance (deconstruction). 

## Version 1

**Ref:** [source link / document / article text]

**Task:** Perform a two-step source-criticism analysis on the above reference to identify whether it constructs a prejudicial impression through technically true claims (paltering / character-assassination-via-true-claims pattern).

**Step 1 — Rhetorical Device Identification (Critical Discourse Analysis)**
Identify and annotate instances of:
- Lexical choice (loaded vs. neutral word selection)
- Passive voicing (agency obscured — "is described as," "has been linked to")
- Nominalization (actions turned into abstract nouns, stripping actor/context)
- Presupposition (claims smuggled in as background fact rather than asserted)
- Attribution structure (who is quoted/cited, in what order, with what framing)

For each instance, quote the phrase (briefly), name the device, and state what impression it creates versus what it literally asserts.

**Step 2 — Structural Absence / Gap Analysis**
Using the source's own genre conventions as the baseline (what would a comparable entry/article normally include), identify what is *absent*:
- Missing self-defense or right-of-reply content
- Missing funding/interest/provenance disclosure
- Missing audience or context framing
- Any other information a neutral treatment of the subject would typically carry

Cross-reference against van Dijk's "ideological square": is negative Other-information emphasized while positive Other-information and negative Self/Us-information are de-emphasized or omitted?

**Output:** A summary distinguishing (a) what is factually asserted, (b) what impression is engineered through device + omission, and (c) the delta between the two — i.e., the prejudicial effect achieved without any single false statement.

---

## Version 2
Template: Hatchet-Job / Cartoonization Detection

Ref: [source link / document / article text]

Task: Determine whether the subject's portrayal has been flattened into a cartoonish "baddie" via framing choices — independent of whether the individual factual claims are true — by running the following checks on the text's internal shape.

Step 1 — Rhetorical Device ID (as before: passive voicing, nominalization, unattributed aggregation, presupposition)

Step 2 — Structural Absence (as before: what genre convention would include that's missing — self-reply, funding, ordinary biographical connective tissue)

Step 3 — Flattening / Cartoonization Index (new)

Score the text on each axis. This step is self-contained — it reads the internal shape of the prose and does not require auditing the cited sources.

AxisCartoonish signatureEarned-portrait signatureIdentity vs. act framingSubject defined as a category ("is a propagandist")Subject described via specific dated acts ("in video X, claimed Y")Vagueness-to-specificity ratioBlanket aggregate claims ("widely accused," "spread propaganda")Concrete, named, dated incidentsVerdict placementVerdict stated before evidence (label-first)Verdict emerges from accumulated specific fact (evidence-first)Totalizing modifiers"Widely," "always," "notorious for," "never"Scoped, quantified, attributed claimsNarrative continuityJump-cut from label to accusation, no ordinary biographical connective tissuePerson moves through time; bad acts sit inside an ordinary life-narrative 

Output:

Per-axis score (cartoonish / mixed / earned)

Valence ratio: proportion of negative-valence vs. neutral/positive-valence content in the passage, computed from the text as given (not from the cited sources — that audit is a separate, harder task)

Overall verdict: does the shape of the framing (not the truth of the claims) produce a flattened, categorical "baddie" impression disproportionate to the specificity of what's actually shown?

 

## Lighter version
Template: Rhetorical/Evidentiary Proportionality Check

Ref: [article]

State the subject's evidentiary status in one line (convicted / adjudicated / widely and multiply corroborated / vs. accused / disputed / single-sourced / litigated).

From the article: list rhetorical-commitment devices actually present (front-loading, occupational lexical choice, guilt-by-association clustering, absent self-reply, hedged-but-stacked attribution).

Judgment: does device density exceed what the stated evidentiary status would justify? State the mismatch directly, don't simulate it.



## ChatGPT's proposal:

 
Reference: [article]

Step 1 – Evidentiary calibration

State the evidentiary status actually supported by the article's claims about the subject, using the suggested labels:

convicted

judicially established

officially determined

multiply independently corroborated

single-source

allegation

disputed

speculative

Explain why this label fits.

Step 2 – Observable commitment devices

List the rhetorical commitment devices from the article, quoting the relevant text for each. 

Consider devices:

front-loading

guilt-by-association clustering

occupational or identity labeling

cumulative allegation stacking

hedged attribution with cumulative effect

omission of contemporaneous rebuttal or self-reply

asymmetric specificity

ordering that privileges accusations before context

presupposition in wording

emotionally loaded lexical choice


Step 3 – Proportionality

Considering Step 1, would a neutral reference work ordinarily employ this level of rhetorical commitment?

Answer:

proportionate

mildly overcommitted

substantially overcommitted

undercommitted

Explain which observed devices create that assessment.

Step 4 – Counterfactual check

If every factual proposition remained unchanged, what minimal editorial changes would reduce rhetorical commitment while preserving all information?

Mention changes of ordering, attribution, wording, balance, or context.

Step 5 – Final assessment

For example: 
'The article presents evidence whose strength is [status], while its rhetoric commits the reader to an impression that is [equal to / somewhat stronger than / much stronger than] that evidence alone would justify.' 

 

## Shorter: even cleaner prompt is:

For the following article:

Classify the strongest evidentiary status actually established.

Identify only textual features that increase rhetorical commitment. Quote each.

Estimate whether the article's rhetorical commitment is lower than, proportional to, or greater than the evidentiary commitment.

Explain the mismatch exclusively from observable textual structure, not inferred author intent.

I particularly like "observable textual structure, not inferred author intent." It disciplines the analysis.

One additional refinement that I think would make the protocol significantly more robust is to require the model to identify commitment sinks as well as commitment amplifiers. For example:

Identify any textual features that reduce rhetorical commitment (e.g., explicit uncertainty, prompt presentation of rebuttal, careful attribution, balancing context, limiting language).

Then the model is effectively computing a balance:

Commitment amplifiers versus commitment attenuators.

That guards against a common failure mode where the analysis notices every accusatory feature but ignores genuine editorial restraint. It also aligns well with your underlying goal: not to detect negativity, but to detect disproportionate rhetorical commitment relative to evidentiary support. If an article contains strong accusations but also prominently presents uncertainty, competing evidence, and the subject's response, the protocol should naturally recognize that the rhetoric has been tempered rather than merely amplified.



  