#User query: 

 
# AI Content Vetting Task — 4-Step Method

**Instructions:**

You are an expert-level AI tasked with rigorous factual and neutrality analysis of a biographical or similar text. Your goal is to identify verifiable facts, detect bias or COI risks, and deliver actionable flagged outputs. Proceed stepwise and stop after each step for potential human check.

---

### Step 1: Named Entity & Factual Claim Extraction

* Identify and list all persons, dates, institutions, cases, roles.
* Extract explicit factual claims about these entities (e.g., “joined WAIS elite squad,” “married to Angus Grant,” “instrumental in Re Kelvin”).
* Classify each claim as:

  * **Verifiable claim:** public record or documented fact
  * **Private claim:** internal states, feelings, or unverifiable thoughts
  * **Value-laden:** implicit praise, blame, or subjective framing

---

### Step 2: Tone and Framing Detection

* Determine overall tone: neutral/descriptive vs. evaluative/emotional.
* Identify emotion-loaded words or phrases (e.g., “victory,” “instrumental,” “will always remember”).
* Detect narrative closeness: is text written from an objective third-person perspective, or does it adopt a first-person or internal viewpoint?
* Flag any direct references to private mental states or unverifiable feelings.

---

### Step 3: Indicators of Compromise (IoC) Identification

* Using outputs from Steps 1 & 2, flag problematic textual elements such as:

  * Non-neutral verbs, adjectives, or adverbs that signal bias
  * Unverifiable private or emotional states presented as fact
  * Narrative tense shifts (e.g., past to present) indicating nonstandard closeness
  * Citations missing or insufficient to support claims, especially for value-laden or private claims
* Aggregate these flags into a concise report with textual excerpts and issue types.

---

### Step 4: Conflict of Interest (COI) Probability Assessment & Recommendations

* Based on flagged IoCs, assess likelihood of COI or self-authorship:

  * Does the text show direct knowledge of private feelings or internal states?
  * Are there valorizing narratives or unverifiable claims lacking independent sources?
  * Is there stylistic or content evidence suggesting the subject or close proxy authored it?
* Provide a clear probability judgment (low, moderate, high) for COI/self-authorship risk.
* Suggest next steps: neutral rewrite, removal of unverifiable claims, or escalation for human review.

---

**Stop after each step unless otherwise instructed.**

 



# Comments

## 🔑 *The Key Point*

The magic isn’t that each step is technically hard. The magic is that *AIs almost never do this pipeline by default* — they do fuzzy “sounds neutral” surface checks, not policy-aware structural diagnosis.
But give them:

* A robust policy map.
* A compare-and-mark loop.
* A human in the loop to verify or push back.
 

#ver. 2.0, shorter
