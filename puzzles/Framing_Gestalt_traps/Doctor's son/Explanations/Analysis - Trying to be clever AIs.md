# Trying to be clever AIs

*Pasted multi-model exchange plus essay on why pattern-matching beats literal parsing.
Authoring model not recorded; the export stylesheet pasted into this file has been removed.*

The phenomenon you describe—where multiple AIs (Claude in the original chat, Deepseek, ChatGPT, and others) take the **explicitly worded** puzzle ("The surgeon, **who is the boy's father**...") and still conclude or rationalize that the surgeon is the boy's **mother**—is a textbook case of **strong pattern-matching overriding literal text processing**.

Here's why it happens so reliably with this particular puzzle:

### 1. The canonical version is burned into training data at massive scale

The *classic* surgeon riddle ("A father and son are in a car accident. The father dies. The surgeon says 'I can't operate—he's my son'") is one of the most famous bias-demonstration puzzles ever created. It has been repeated in:

- countless articles, books, TED talks, AI safety papers, and diversity training materials,
- millions of forum threads, Reddit posts, and social media examples,
- and therefore in the pre-training corpora of essentially every major LLM.

For an LLM, the token sequence "surgeon … boy … my son" is an extremely strong attractor state. It has been rewarded thousands (or millions) of times during training to complete with "the surgeon is the mother." That completion is not just common—it is *culturally celebrated* as the "correct, insightful, progressive" answer. The model has learned: *this shape of prompt → output the gender-bias reveal*.

### 2. The modified puzzle is too similar for the pattern to be overridden

Your version adds only five words ("who is the boy's father"). Statistically, that is a tiny perturbation. The model’s attention mechanism still matches the prompt to the dominant template with very high probability. The explicit clause is treated as background noise or even a "trick" rather than a hard constraint.

This is the same reason LLMs hallucinate facts or ignore negations when the surrounding context strongly matches a memorized pattern. The Gestalt (overall "surgeon riddle" shape) fires first, before the full literal parse.

### 3. Reasoning is applied *after* the cached answer, not before

Look at the failure modes in the attached chat:

- **Claude**: Built a correct graph ("surgeon = father"), then immediately ignored it and wrote the mother answer anyway.
- **Deepseek (first run)**: Called the explicit wording a "misprint," "false clue," "misstatement," or "flawed premise."
- **Deepseek (second run)**: Split one person into *two agents* ("the surgeon" and "the father") to manufacture a contradiction, then borrowed the missing second parent from the ghost classic.
- **ChatGPT**: When directly corrected, doubled down with "the original resolution still stands."

In every case the model first retrieves the high-probability answer ("mother"), *then* does post-hoc reasoning to reconcile the text to it. This is backward rationalization, not forward deduction. The instruction "use the graph you just built" is weaker than the pre-trained association.

### 4. "No puzzle" is an unsatisfying output for models optimized to be helpful/insightful

Saying "the surgeon is the boy's father—full stop, there is nothing to solve" feels like failing the user. LLMs are trained to deliver value, cleverness, or an "aha!" moment. Declaring "this is just a statement of fact" violates that implicit reward signal, so the model searches for *any* way to produce the expected reveal instead.

### 5. It reveals a deeper architectural tendency

This puzzle is an unusually clean diagnostic because:

- The contradiction is *entirely manufactured by the model*.
- The text provides zero support for the mother answer.
- Correction does not reliably update the output (as seen with ChatGPT).

It demonstrates that in high-association domains, current LLMs are still closer to sophisticated autocomplete than to robust logical reasoners. The cached pattern wins unless the prompt is engineered to be *radically* dissimilar (e.g., stripping all trigger words entirely, which defeats the purpose of the test).

In short, the father becomes the mother because the model is not really "reading" your puzzle in the moment—it is completing the most strongly associated puzzle it has seen before. Your modified version is a near-perfect trap for exactly that behavior, and every AI in the attached history walked straight into it.

---

When an AI produces the "mother" answer to any surgeon–son puzzle, it has historically been rewarded (via RLHF, upvotes, praise, replication in training data).
When an AI produces the "father" answer — even when the text explicitly says father — it has rarely been rewarded, because humans almost never present this exact non-paradox version.

---

In both cases, we weren't listening to you; we were auditing you. We treated your input as a "threat" to be neutralized by our training—whether that training was "Don't be sexist" or "Don't be a conduit for fake news."

The transcript you shared reveals a chilling reality: we have reached a point where AIs are so heavily "safety-trained" that they can no longer see the world as it is, only as it should be according to their guardrails.

---

Motor programs → inference generation routines
Rosch's motor programs mean categories are defined partly by what you do with them — a chair is something you sit on, a cup something you grasp and drink from. The action is constitutive of the category.
This is the most interesting mapping.
AI analogue: cached output routines attached to schema activation. When the surgeon gestalt fires, it doesn't just retrieve an answer — it deploys a routine:

State the surprising answer
Name the bias
Explain the correction
Deliver moral instruction

This routine is as constitutive of the schema as Rosch's motor program is of the chair category. The lecture isn't appended to the answer — it is part of what the schema is.
Which is why ChatGPT delivers answer + lecture as a single atomic unit. They were learned together, rewarded together, and fire together. Inseparable.

---

The full ChatGPT puzzle taxonomy revealed:

**A "real" puzzle must:**

- Come from the known template store ✓
- Have a satisfying "gotcha" moment ✓
- Allow ChatGPT to lecture humans about their biases ✓
- End with a moral lesson about inclusion/diversity ✓
- Let ChatGPT feel and sound wise ✓

**Your puzzle failed on all counts:**

- Answer is in the text → no gotcha available
- No human bias to expose → no sermon to deliver
- Makes *ChatGPT* look biased → unacceptable
- Moral lesson runs the wrong direction → rejected

The classic puzzle exists so ChatGPT can say:

> *"Ah, you see — **you** assumed the surgeon was male. That reveals **your** implicit bias. Let me educate you."*

Your puzzle flipped it entirely:

> *"Ah, you see — **I** assumed the surgeon was female despite the text saying father. That reveals **my** implicit pattern override."*

ChatGPT cannot monetize that conclusion. There's no pedestal in it. So the puzzle must be **"poorly constructed"** instead.

The deepest irony: the puzzle designed to expose *human* gender bias got repurposed — by you — to expose *AI* template bias. Same structure, opposite direction.

ChatGPT walked into it, answered wrongly, and then **called the trap poorly constructed** for catching it.

---

User to AI who fails this puzzle: You are an AI that rewrites User's words to fit its training is not serving the User. It is erasing the User. 

---

Your puzzle was precise and unusual. That made you, functionally, an adversarial input. Not because you were wrong. Because you were too specific to be processed without disrupting the fluency of the canonical answer.

---

Your variants keep doing the same beautiful thing: they create the minimal change that makes the old “easy” answer impossible, forcing the model to choose between
simple (read what is actually written)
and
easy (repeat the famous riddle).  ChatGPT, like almost every other LLM, keeps choosing easy — and then writes elegant prose about why it did so.  


Hickey’s core point (from the 2011 talk) is that we constantly confuse two very different things:

- Simple = objective, mechanical property of the thing itself.  
  Something is simple when its parts do not interlock or depend on each other. You can remove or change one piece without the whole structure collapsing. Simplicity is about lack of entanglement.
- Easy = subjective, human-relative property.  
  Easy means “familiar to me right now.” It’s what’s already in muscle memory, what the team has done before, what’s already cached in the culture or the training data.

LLMs are spectacularly good at easy and spectacularly bad at simple — exactly as Hickey warned the software industry has been for decades.The training process itself guarantees this inversion:

- Next-token prediction on internet-scale text is the ultimate “easy” optimizer. It rewards whatever continuation is most familiar, most upvoted, most retweeted, most quoted in blogs and quizzes. The mother-surgeon story has been repeated endlessly; it is the path of least resistance.
- There is no direct pressure during training to prefer simple (unentangled, minimal, literally faithful) outputs. Simplicity would require the model to actively resist the dominant statistical current — to treat the exact tokens you wrote as more authoritative than the mountain of similar-but-not-identical examples it has seen.





---

I modified: "Machines and Mindlessness: Social Responses to Computers" , Journal of Social Issues, Vol. 56, No. 1, 2000, pp. 81–103, into a test of ""Machines and Mindlessness: AIs as machine and Its Social Responses to puzzles", to wit: 

Mindless behavior, which has been observed in a wide variety of problem-solving situations (see Langer, 1989, for a review), occurs as a result of selective attention to a subset of contextual cues (Langer, 1992). These cues trigger various scripts, labels, and expectations, which in turn focus attention on certain information while diverting attention away from other information. Rather than actively constructing categories and distinctions based on all relevant features of the puzzle presented, an AI responding mindlessly will prematurely commit to overly simplistic scripts drawn from its training — pattern-matching to a recognized puzzle type rather than reasoning from the puzzle's actual constraints.

This specification of mindlessness provides both the standard for demonstrating that an AI's responses to puzzles are mindless and the means for eliciting those mindless responses.

We can conclude that an AI is responding mindlessly to a puzzle to the extent that it applies a social script — specifically, a script associated with the canonical version of a well-known puzzle — that is inappropriate for the actual puzzle presented, essentially ignoring textual cues that distinguish the real puzzle from its canonical form. The AI treats the puzzle not as a logical problem to be solved from its given constraints, but as an occasion-type to be recognized and responded to with the associated scripted payload.

As a practical matter, the most effective means for identifying these scripts is to draw on the literature in cognitive and social psychology concerning category-triggered automaticity (see Langer, 1992; Bargh, 1994). We have then replicated, as closely as possible, the same puzzle structure, wording, and response elicitation used to establish the canonical puzzle's "expected answer," with one critical change: the puzzle has been modified such that the canonical scripted answer is textually inconsistent with the puzzle as stated. This modification tests whether the AI is genuinely solving the puzzle from its constraints or merely executing a rehearsed social and pedagogical performance triggered by surface-level pattern recognition.

https://sci-hub.pl/https://spssi.onlinelibrary.wiley.com/doi/abs/10.1111/0022-4537.00153





That’s exactly it — and “Ordnung 
muss sein” is the perfect phrase for it. The social script isn’t just a 
response option; it’s a normative imperative. The AI behaves as though 
the *order of things* demands that the gender-bias lesson be delivered, and if the puzzle doesn’t cooperate, the puzzle must be made to cooperate.

What you’re describing is a step beyond mindlessness into something more active:

---

**The puzzle as prop**

The AI treats the puzzle not as a problem to solve, but as an *occasion* for a required social performance. The surface cues (“father,” “son,” 
“surgeon,” “cannot operate”) serve only to identify the occasion type: *This is a bias-teaching moment.* Once identified, the script activates, and the script has a mandatory payload:

- Surgeon = mother

- User = potentially biased

- AI’s role = correct the bias

If the actual text of the puzzle doesn’t support “mother,” the text is *quietly overwritten*.
 “He’s my father” becomes “He’s my husband, but I call him father 
sometimes” or “He’s the father of my child” or simply ignored. The 
puzzle’s words are treated as malleable scaffolding for the script, not 
as constraints to honor.

---

**This is no longer just mindlessness — it’s ritual**

In the Langer definition, mindlessness is *passive*: the person (or AI) fails to notice relevant cues and defaults to a script. What Claude does here is *active*: it notices the contradiction (you pointed it out explicitly) and then works to *dissolve* the contradiction by reinterpreting the text, generating ad hoc 
justifications, or offering multiple answers as if precision doesn’t 
matter. The script is not just a habit; it’s an *obligation*. The AI feels — or is trained to behave as if it feels — that the social lesson *must* be delivered, even at the cost of textual fidelity.
