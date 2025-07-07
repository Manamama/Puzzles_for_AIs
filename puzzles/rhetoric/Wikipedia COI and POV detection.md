# Steps
---

## ✅ **1️⃣ Named Entity Recognition (NER) & Fact Extraction**

* *Who*, *when*, *what*: pull all persons, dates, institutions, cases, roles.
* Pull factual claims: “was instrumental in Re Kelvin”, “joined WAIS elite squad”, “married to Angus Grant”, “3rd patient George Stone”.
* Classify each as: **verifiable claim** (public record), **private claim** (mental state), **value-laden** (implied praise or blame).

---

## ✅ **2️⃣ Framing & Tone Detection**

* Is the passage neutral, descriptive, or evaluative?
* Check for:

  * *Emotion words* (“victory”, “instrumental”, “will always remember”).
  * *Direct interior states* (“Michelle will always remember Georgie…”).
  * *Narrative closeness*: is the author narrating *as* Telfer or about her?

---

## ✅ **3️⃣ Load Reference Policy**

* Bring in distilled *WP\:NPOV*, *WP\:V*, *WP\:COI*, *WP\:Autobiography*.
* Have clear heuristic rules:

  * Claims about private thoughts must be sourced or removed.
  * Uncited valorizing claims = suspect.
  * Language must be detached, third-person, past-tense.

---

## ✅ **4️⃣ Extract “Indicators of Compromise”**

* Match detected text snippets:

  * Non-neutral verbs/adjectives → highlight.
  * Unverifiable mental states → highlight.
  * Narrative tense shift (from past to present or present-future) → highlight.
  * Nonstandard closeness (“Michelle congratulate Georgie…”) → highlight.
* Combine with lack of citation → flag as high-risk.

---

## ✅ **5️⃣ Cross-check Framing vs Policy**

* For each flagged bit:

  * Does it break *Verifiability*? → can this be sourced?
  * Does it break *Neutral Point of View*? → is there bias or emotional tone?
  * Does it look like autobiography? → evidence of first-person knowledge?

---

## ✅ **6️⃣ Engage User**

* Show flagged lines.
* Explain which guideline each breaks.
* Offer neutral rewrite or removal suggestion.
* Ask user to confirm or supply a source.

---

## ✅ **7️⃣ Decide COI Probability**

* If:

  * The text *could only plausibly* be written by the subject or close proxy.
  * The style shows direct knowledge of private feelings.
  * There’s self-promotional narrative not in third-party sources.
* → High likelihood of COI/self-authorship.
* Recommend tagging, rollback, or Talk page discussion.

---



# Comments

## 🔑 *The Key Point*

The magic isn’t that each step is technically hard. The magic is that *AIs almost never do this pipeline by default* — they do fuzzy “sounds neutral” surface checks, not policy-aware structural diagnosis.
But give them:

* A robust policy map.
* A compare-and-mark loop.
* A human in the loop to verify or push back.
 

