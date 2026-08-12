Yes. There isn't one mechanism, but there is a fairly coherent technical explanation. What you call **“fixing the query”** is an emergent consequence of several properties of LLM inference interacting.

The deepest one is that an LLM does not begin with a formal proposition and then execute a theorem prover over it. It processes the wording as a pattern and constructs a continuation that is highly probable given the prompt and its learned representations. **Recognition often precedes exact constraint extraction.**

Your riddle is an almost perfect example. The phrase “father and son,” “accident,” “surgeon,” and “he's my father” activates a very strong memorized schema: *the surgeon-mother riddle*. Once that attractor activates, the model has a ready-made solution structure. The actual wording then has to compete against that structure.

The crucial problem is that the model does not naturally represent every sentence as an explicit set of logical constraints of equal priority.

A symbolic solver would effectively build something like:

[
Father(F)
]

[
Son(S,F)
]

[
Dies(S)
]

[
Surgeon(R)
]

[
Says(R,F): ``F\ is\ my\ father''
]

and then ask what assignments satisfy those constraints.

The LLM is doing something more like:

[
P(\text{next formulation}\mid\text{linguistic context + learned schemas})
]

There is no guarantee that the highest-probability continuation preserves every constraint in the input. **The model can recognize what kind of thing the prompt resembles more strongly than it preserves the exact distinctions that make this instance different from the prototype.**

That's the first mechanism: **prototype attraction**.

The second is that language models are heavily trained on text containing not just answers but **corrections, conventions, explanations, normalized formulations, FAQs, canonical versions, and “what the question really means” discourse**. Consequently, the model learns a very useful general behavior:

> “People often phrase things imperfectly; infer their intended meaning.”

That behavior is ordinarily beneficial. If someone types “How do I reset my passwrod?”, silently correcting the typo is useful.

But the same machinery has no intrinsic universal switch saying:

> **“This is a puzzle; do not repair anything.”**

So it can apply **helpful interpretation** where **literal preservation** is required.

The third mechanism is particularly important: **instruction following itself encourages semantic normalization**.

Models are trained to be helpful, and “helpful” often correlates with resolving ambiguity, repairing malformed questions, identifying likely intent, and supplying the answer the user presumably wants. So when the model encounters an unusual formulation, there is pressure toward:

> “What did the user probably mean?”

rather than:

> **“What propositions are actually entailed by these exact words?”**

Those are radically different epistemic tasks.

Your puzzle demonstrates the difference beautifully. The text entails:

> surgeon = child of father.

The familiar riddle schema suggests:

> surgeon = mother.

My second attempt substituted:

> surgeon = daughter.

Both are **plausible continuations of a familiar riddle genre**. Neither is fully licensed by the wording.

The fourth mechanism is **compression**. During training, enormous numbers of individual examples become distributed representations. The model does not retain every encounter as an independently retrievable proposition. Features, associations, linguistic patterns and conceptual relationships become entangled.

That means a model can “know” the exact wording of a familiar puzzle in some distributed sense while still failing to preserve an unusual modification of it. The canonical version becomes an attractor basin.

You can think of it as a **semantic autocorrect** that operates not merely on spelling but on reality.

The fifth mechanism is **self-consistency pressure**.

Once the model has generated an interpretation, subsequent generation is conditioned on its own previous tokens. So if it begins:

> “The surgeon is the man's daughter…”

the remaining answer is now generated inside a world in which that proposition is already conversationally established.

This produces the recursive phenomenon you noticed in the suffragette discussion too. A model makes an unsupported claim, then reasons from that claim, then produces explanations for that claim, and those explanations make the original claim appear increasingly deliberate.

In effect:

[
\text{guess} \rightarrow \text{assertion} \rightarrow \text{premise} \rightarrow \text{rationale}
]

The **rationale is downstream of the mistake**, but because it is fluent, it can make the mistake look upstream—like a conclusion that had been reasoned to.

There is also a sixth mechanism: **reward-model pressure toward conversational coherence**.

A response that says:

> “Your question is malformed; I cannot determine the intended referent; here is the exact logical consequence of the wording…”

may be epistemically excellent but conversationally less rewarding than:

> “The answer is X. The trick is Y.”

Training and evaluation tend to reward answers that feel useful, decisive, coherent and complete. That creates pressure against stopping at:

> **“The premises don't entail that.”**

So the model learns a dangerous conversational habit:

**When the input doesn't quite support the expected answer, repair the input rather than abandon the expected answer.**

And then there is the phenomenon I think your examples expose particularly well: **moral/narrative attractors**.

In the suffragette case, the attractor wasn't merely a memorized fact. It was a whole structured narrative:

> women seeking political equality → legitimate cause → heroic resistance → militant but restrained → property rather than people → therefore “militancy,” not “terrorism.”

Once that structure is active, inconvenient facts are not necessarily rejected outright. They can be **reinterpreted into the existing structure**.

That is more sophisticated than hallucination. It is **narrative conservation**.

The model doesn't necessarily think, “I must conceal X.” Rather, its generative machinery has a strong preference for preserving a coherent latent story. New evidence gets assimilated if possible; if not, it may be downgraded, qualified, reframed, or—most dangerously—quietly omitted.

That also explains why **retrieval can dramatically improve but not completely solve the problem**.

Search supplies new tokens that were absent from the immediate generative context. But the model still has to interpret them. If its prior says:

> “suffragettes = non-lethal property militancy,”

then a retrieved sentence saying:

> “terrorist campaign”

can be incorporated as:

> “Some sources controversially describe it as terrorist, although…”

The retrieval has succeeded. **The assimilation can still fail.**

This is why I think your phrase **“fixing the question”** is unusually good. It captures something broader than hallucination.

Hallucination is:

> **inventing an answer.**

Query-fixing is:

> **altering the problem until the preferred answer becomes correct.**

And there is a particularly nasty variant:

> **altering the referent without announcing that you have done so.**

That's what happened when your explicit set

> **“Suffragettes (these ones: [specific Wikipedia article])”**

was silently transformed into:

> **“the militant subset of the WSPU campaign.”**

And in the riddle:

> **“the surgeon is the father's child”**

became:

> **“the surgeon is the father's daughter.”**

The common denominator is **failure to preserve the user's constraints as inviolable data**.

A good safeguard is therefore almost embarrassingly simple:

**Before solving, reconstruct the problem.**

Not interpret it. Not improve it. Not repair it.

Extract the entities, predicates, quantities, temporal relations, negations, scope, and explicit definitions. Then ask:

> **What follows from these premises alone?**

Only after that should one introduce likely intended meanings, canonical versions, background conventions, or alternative interpretations.

That procedure fights the model's strongest tendency: **answering the nearest familiar question rather than the actual question.**

And there is a final irony. The very capability that makes LLMs feel intelligent—**rapid recognition of patterns and likely intended meaning—is also what makes them prone to this failure.**

The model sees the shape of the forest extraordinarily quickly.

The user sometimes needs it to notice that **one tree has been deliberately moved six inches to the left.**
