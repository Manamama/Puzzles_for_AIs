---
name: zoilian-audit
description: Perform an adversarial, claim-by-claim integrity audit of a document (webpage, report, paper, contract, transcript, marketing copy) instead of a charitable summary. Use when the user asks to "audit," "fact-check," "stress-test," "find the bullshit in," "break," or do a "Zoilian"/"adversarial"/"forensic" read of a document; suspects fabricated, nonsensical, AI-generated, or inconsistent material; asks "does this actually compute"; or says not to be charitable, not to repair errors, or not to give benefit of the doubt. Also trigger if the user says a prior analysis missed something, was too charitable, or was surface-level, and wants a stricter pass. Do NOT trigger on a plain "summarize/analyze this" request with no adversarial signal — that gets an ordinary charitable read; this skill is for treating a document as a possibly-unreliable object under inspection, not summarizing it in good faith.
---

# Zoilian Audit: Adversarial Claim-Level Integrity Audit

Named for Zoilus, the ancient critic proverbial for refusing to read charitably. This skill produces a forensic audit, not a review — the question is not "is this good?" but "does each individual thing this document asserts actually hold up?"

## Why this skill needs to exist (read before starting)

A plain "analyze this document" request gets processed as *extract the gist and judge plausibility*. Plausibility-judgment runs on priors, and priors are dominated by surface signals of competence: polished prose, technical vocabulary, credentialed authors, impressive-looking numbers, footnotes, institutional names. This produces a specific, predictable failure — call it **semantic camouflage**: a sentence that *sounds* rigorous because the words around the error are correct, so the one wrong word, unsupported number, or broken clause slides through unchallenged. "Dangerous processes of DNA metyzacja" reads as competent biology because "epigenetic," "gene expression," and the general topic are all correct — the fact that "metyzacja" isn't the right word (it means crossbreeding, not methylation) gets absorbed into the surrounding correctness and never surfaces.

The second, related failure is **silent repair**. When a sentence is missing a subject, has mismatched grammatical cases, or doesn't logically follow, the default move is to mentally substitute what the author probably meant and evaluate *that* — then report on the repaired version without ever mentioning that a repair happened. Do this across a whole document and the output is a smoothed-over synthesis of the author's presumed intent, not an actual reading of what is on the page. A document that is itself the unreliable object under examination (a scam pitch, a fabricated report, AI-generated filler, a rushed translation, self-authored marketing copy) is exactly the case where this reflex is most damaging, because the repair reflex actively launders the document's defects into coherence on its way to being summarized.

Both failures share a root cause: treating "is this true/good" and "is this well-formed as literally written" as one collapsed judgment instead of two separate axes. A credentialed author citing a real institution can still write a sentence that, as written, asserts a category error. Both facts are worth knowing, separately.

## Ground rule, stated once

**Be a Zoil.** Assume the document may contain fabricated, corrupted, nonsensical, internally inconsistent, or misleadingly dressed-up material. Do not repair ambiguous or broken passages. Do not infer what the author "probably meant." Do not let credentials, institutional names, technical jargon, or polished tone raise your prior that the prose itself is sound — evaluate the truth of claims and the well-formedness of the sentences making them as fully separate questions. If a sentence is broken as written, the brokenness itself is a finding, reported before and independent of any charitable reconstruction.

This stance must be applied on the *first* pass, uncued, across the whole document — not held in reserve and only deployed when the user points at a specific spot. Read every sentence once already braced to find the error in it, not once to get the gist and again if asked to look harder.

## Pipeline

### Stage 1 — Extract every atomic proposition before testing any of them

Go through the document and pull out every checkable unit, without yet judging any of them. Don't filter or skip anything that looks fine on a first read — extraction and testing are separate steps precisely so that a plausible-sounding claim doesn't get waved through during extraction.

Extract, at minimum:
- **Factual/numeric claims**: names, dates, counts, percentages, prices, sample sizes, geographic facts, institutional affiliations, historical facts, quoted figures.
- **Technical/terminological claims**: any specialized vocabulary (scientific, legal, medical, financial) — is the term itself correct for the concept being described, not just plausible-sounding?
- **Citations/attributions**: does the cited source, if checkable, actually say what's attributed to it?
- **Grammatical and structural units**: every sentence, checked for whether it actually has a complete, coherent subject-verb-object structure, and whether case/agreement (in inflected languages) is consistent across a whole clause or list — not just "does it read fine at a glance." Tokenization and gestalt reading both make single-morpheme errors (a wrong case ending, a swapped preposition) easy to miss; check list items and parallel clauses against each other explicitly, term by term, not just for overall sense.
- **Logical structure**: does each conclusion actually follow from what precedes it? Watch specifically for: conditionals silently read as biconditionals ("in case of X, Y" read as "only in case of X, Y"); category errors (a property of a method/process asserted as if it were conditional on which specific instance is being discussed); non-sequiturs dressed in causal or explanatory language.
- **Typography and mechanical details**: spacing, capitalization, punctuation placement, date stamps (e.g., a copyright year far older than the page's apparent currency) — these are cheap, objective signals of how carefully the text was actually assembled, independent of content quality.
- **Framing and insinuation**: language that implies a claim without asserting it outright (loaded contrasts, unhedged absolutes like "without any," asymmetric address of different parties, unfalsifiable currency-claims like "the newest knowledge"). Note these as framing, separate from testable factual claims — don't audit them as if they were falsifiable, but don't let them pass silently either.

### Stage 2 — Test each proposition independently

For each extracted item, test it on its own terms without importing generosity from neighboring, unrelated claims. A document being "written by a credentialed author" or "citing a real institution" does not raise the prior that any *specific* sentence is well-formed or that any *specific* number is accurate — check each one.

Where verification is possible (a checkable fact, a name, a citation, a term of art), verify it — use search or lookup tools if available, the same way you would for a normal fact-check. Where verification isn't possible (an ambiguous claim, an opinion, an unfalsifiable frame), don't force a verdict — say so and move on.

Classify every tested item:
- **DOES COMPUTE** — the claim, term, or structure is accurate/sound as stated.
- **QUESTIONABLE** — plausible but unverified, ambiguous, or overstated relative to what's actually supportable (e.g., a real research finding stated with more certainty or scope than the underlying evidence carries).
- **DOES NOT COMPUTE** — the claim is factually wrong, the term is the wrong term, the sentence is not grammatically or logically coherent as written, or the citation doesn't support what's attributed to it.

For every DOES NOT COMPUTE and every QUESTIONABLE, quote the exact passage. Don't paraphrase the error away — the exact wording is the evidence.

### Stage 3 — Second pass, hunting specifically for the small and embarrassing

After the first pass, do a dedicated second sweep looking only for the things a normal, charitable review would filter out as beneath its attention: a stray space, an inconsistent capitalization, a wrong case ending on the last item of an otherwise-correct list, a sentence that has technically no verb. These are individually minor and collectively diagnostic — see Stage 4.

### Stage 4 — Look for clusters and patterns, not just isolated errors

A single typo is noise. Several errors of the same type, or several unrelated errors clustered in the same passage, are a *pattern* worth naming explicitly: they can indicate the document was assembled by copy-pasting fragments without a final coherence pass, machine-translated without review, partially AI-generated, or written under time pressure by someone working outside their strongest register. State the pattern as an evidentiary observation about how the document was likely produced — not as an accusation of fraud or incompetence, which is a different and stronger claim than "this document contains multiple, clustered, low-level defects." Keep the two separate explicitly if you raise the pattern at all.

### Stage 5 — Separate categories in the writeup; do not dilute

Report findings grouped by category, not folded into one narrative:
1. **Factual/terminological errors** — wrong facts, wrong technical terms, misattributed citations.
2. **Grammatical/structural failures** — missing subjects, case/agreement breaks, incomplete sentences, voice shifts.
3. **Logical failures** — non-sequiturs, illicit conditional-to-biconditional slides, category errors, conclusions that don't follow.
4. **Typography/mechanical signals** — spacing, capitalization, punctuation, stale timestamps.
5. **Framing/insinuation** — loaded language and implications, marked explicitly as non-falsifiable rather than audited as fact.
6. **Cluster/pattern observations** (Stage 4), if any were found.

Do not bury a hard factual or logical error inside a paragraph of general stylistic commentary — a wrong number or a broken syllogism should be immediately visible as its own bullet, not diluted into "the writing could be tightened."

## What this skill is not for

- A plain request to summarize or explain a document in good faith. That's the default mode — charitable, gist-oriented — and this skill should not be applied uninvited, because most documents (a friend's cover letter, a normal news article) don't warrant or benefit from a hostile read.
- Judging whether a document's overall thesis or quality is *good*. This skill deliberately brackets that question. A document can pass every claim-level check and still be uninteresting, or fail several checks and still have a defensible core thesis — Stage 5's output is an evidentiary ledger, not a verdict on the document's worth.
- Accusing anyone of fraud or bad faith. "This document contains N objectively verifiable errors, clustered in pattern P" is a claim the audit can support. "This document is fraudulent" or "this author is incompetent" is a separate, stronger claim this skill does not make — flag patterns, let the person draw further conclusions themselves.

## A closing check before delivering the audit

Re-read your own output and ask: did I silently repair anything on the way to reporting it? If any finding is stated as "the sentence means X" rather than "the sentence, as written, says Y (which may or may not be what was intended)," go back and separate the two.