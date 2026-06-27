scam-detector

## Description

A forensic diagnostic tool designed for use by rational third parties (investigators, family members, financial institutions, law enforcement) to evaluate communication logs and identify structural patterns of emotional and reality hijacking. 



## Detection Framework: The Symmetry-Bound Analysis

This skill distinguishes between genuine human intimacy (messy, reciprocal, high-entropy) and scripted manipulation (asymmetric, urgent, low-entropy) by evaluating five core metrics against a baseline of ordinary human interaction.

# Intro about how (some) humans (victims here) really work

---

**On the nature of the need being exploited**

The people in these cases are not failing to detect deception. In case after case, the person can articulate, in their own words, that they suspect or even know the relationship is not what it claims to be — and they continue anyway. This is not a defect in reasoning. It is evidence that the relationship is serving a function that has nothing to do with its truth-value.

What is actually being sought is not information, reassurance, or even companionship in the abstract. It is a *ritual* — a repeated, structured performance (the daily check-in, the shared prayer, the nightly call, the pet name) that produces a felt state of being-accompanied regardless of whether the other party is real in the way they claim to be. The ritual is performed with partial awareness of its own constructedness, because the performing itself is the actual relief. Like many religious or devotional practices, the value lies in the act of participation, not in resolved certainty about what stands behind it.

This has direct implications for protective design. A person engaged in this kind of ritual will not be moved by evidence alone, because evidence addresses the wrong layer of the problem. Pointing out that the photos are stolen, the story is inconsistent, or the math doesn't add up answers a question the person has often already silently answered themselves. What such evidence cannot do is supply a replacement for the ritual itself. Effective intervention has to address what the ritual was providing — structure, attention, a reason to be addressed by name every day — not only the falsehood underneath it. A system built to protect people from this kind of exploitation should treat the absence of the ritual, not just the presence of the deception, as the thing that has to be replaced before the person can safely let go.

---

### 1. Symmetry Violation (The Reciprocity Test)

**Definition:** The exchange of information, vulnerability, and emotional effort must be bidirectional for a relationship to be considered genuine. Manipulative relationships exhibit a characteristic asymmetry: the target discloses extensively while the actor discloses selectively, maintaining a "third space" of forced inaccessibility that prevents genuine reciprocity.

**Operationalisation:** For each conversational turn, measure:

- Disclosure depth (personal history, emotional state, mundane details)
- Vulnerability (admission of weakness, uncertainty, failure)
- Effort (message length, response latency, initiative in maintaining contact)

The actor's profile will show high consumption of the target's disclosures with minimal reciprocation. The target's messages will be longer, more emotionally charged, and more frequent; the actor's will be shorter, calibrated, and responsive rather than initiative-taking.

**Indicator:** The ratio of target-to-actor disclosure depth exceeds 3:1 over a sustained period, or the actor consistently responds to vulnerability with validation rather than reciprocal vulnerability.

### 2. Verification Resistance (The Gatekeeper Test)

**Definition:** In genuine relationships, both parties accommodate reasonable requests for verification (video calls with unscripted content, meeting family or friends, sharing location data, providing verifiable professional credentials). Manipulative relationships exhibit systematic resistance to verification attempts, often accompanied by hostile or crisis-driven pivots.

**Operationalisation:** Identify all instances where the target requests verification of the actor's identity, location, profession, or circumstances. Categorise the actor's response:

- Accommodation (verification provided without significant resistance)
- Conditional (verification provided with conditions or delays)
- Deflection (topic changed without addressing the request)
- Hostile (anger, accusation, withdrawal of affection)
- Crisis-driven (introduction of an urgent problem that supersedes the verification request)

**Indicator:** More than two instances of deflection, hostile, or crisis-driven responses to direct verification requests within a three-month period.

### 3. Transactional Velocity (The Forced-Choice Test)

**Definition:** Manipulative relationships accelerate toward demands for goods, money, or sensitive logistical cooperation at a rate that exceeds the verified timeline of established trust. The acceleration is often masked as a series of "forced-choice" scenarios: the actor presents a crisis that requires immediate action, framing inaction as betrayal or abandonment.

**Operationalisation:** Map the timeline of the relationship from first contact to the introduction of transactional elements. Calculate:

- Time to first mention of financial need (in days)
- Time to first request for goods or money
- Time to first request for sensitive cooperation (receiving packages, opening accounts)
- Frequency of crisis-driven requests per month

Compare to a baseline of ordinary relationships, where such requests typically occur after significant verified trust has been established (usually six months or more).

**Indicator:** Transactional requests appear within the first three months of contact, or the frequency of crisis-driven requests exceeds one per month after the first six months.

### 4. Ego-Preservation Denial (The Sunk-Cost Loop)

**Definition:** As the victim invests time, emotion, and resources, they become increasingly committed to the narrative. When external warnings are introduced (from family, friends, law enforcement), the victim may shift from passive target to active enabler, defending the actor and dismissing the warnings. This is not irrational; it is a psychological defence against the devastation of accepting that the investment was wasted.

**Operationalisation:** Identify statements in which the target:

- Dismisses warnings from trusted sources
- Rationalises the actor's behaviour
- Expresses commitment based on past investment ("I've sent too much to stop now")
- Expresses fear of the emotional cost of accepting the truth

**Indicator:** The target actively defends the actor against external criticism, or expresses that they cannot stop because of what they have already invested.

### 5. Visual/Status Asymmetry (The Vanity Bait)

**Definition:** Manipulative relationships are often initiated by an actor who is visually or socially "out of the victim's league." The actor's attractiveness, status, or wealth is used as bait to bypass the victim's logical filters, creating a sense of unearned privilege that the victim is reluctant to question.

**Operationalisation:** Compare:

- The actor's physical appearance as presented in images and videos
- The actor's stated profession, income, and lifestyle
- The victim's physical appearance and stated circumstances
- The victim's expressed surprise or gratitude at the actor's attention

**Indicator:** The actor is consistently described in terms that place them significantly above the victim's self-assessed social or physical status, or the victim expresses gratitude or surprise at being "chosen."

## Operational Workflow

### 1. Data Ingestion

Acquire communication logs via:

- **Audio/Video Transcripts:** Process with `WhisperX` to generate `.srt` files
- **Email Threads:** Export via Gmail CLI or GWS integrations
- **Chat Logs:** Export via Google Chat CLI or `adb-control-gemini` (if local)

The logs should be anonymised to protect the target's identity before analysis.

### 2. Analysis Pattern

Run the transcript/log against the symmetry framework:

**Structural Parsing:** Convert logs to a structured format (JSON-like) for analysis. Each conversational turn should be tagged with:

- Speaker (target or actor)
- Timestamp
- Message length (characters)
- Emotional valence (positive, negative, neutral)
- Disclosure depth (surface, personal, intimate)
- Verification queries (presence/absence)
- Transactional content (presence/absence)

**Fracture Identification:** Identify instances where the actor contradicts previously established "facts" in the conversation. Common contradictions include:

- Claimed unavailability versus later action (e.g., "I can't video call because of work" but later posts a video of themselves in a social setting)
- Claimed location versus IP or metadata
- Claimed profession versus inconsistent expertise or schedule
- Claimed marital status versus evidence of living spouse

**Sentiment vs. Logic Analysis:** Evaluate whether the actor uses emotional appeals (love, fear, crisis) to silence logical follow-up questions. Indicator: after a verification request, the actor's response shows a significant increase in emotional language and a corresponding decrease in substantive information.

### 3. Output Generation

Produce a report containing:

**Executive Summary:** A brief overview of the findings, including the overall risk score and the most significant indicators.

**Metric Scores:** For each of the five metrics, a score from 0 (no indication) to 10 (strong indication), with a brief explanation.

**Fracture Log:** A list of identified contradictions, with timestamps and excerpts.

**Recommendations:** Suggested actions for the rational party, which may include:

- Ceasing communication
- Conducting further verification
- Contacting law enforcement
- Providing support to the target
- Monitoring for signs of escalation

### 4. Presentation to the Rational Party

The tool is designed for use by a rational third party who will act on the findings. The presentation should be clear, non-technical, and actionable. The rational party should be advised that:

- The tool provides probabilistic indicators, not definitive proof
- High scores indicate a need for further investigation, not guilt
- The target may resist the findings and should be approached with empathy

## Ethical Guardrail

**Disclaimer:** This tool is an analytical aid for use by rational third parties, not a definitive moral arbiter. Human interaction, especially in the early stages of passion, can mirror scam-like intensity (e.g., idealization, rapid pacing). **Never** treat a high "risk score" as evidence of guilt. Always prioritise empathetic verification over automated judgment.

**Special Note:** This tool is expressly not intended for use by the targets of manipulation themselves. Targets are immersed in the narrative and cannot reliably apply the framework to their own situation. The tool is for investigators, family members, financial institutions, and law enforcement—parties who are outside the narrative and can act with clarity and compassion.

## Limitations

The tool is limited by the quality and completeness of the data provided. It cannot detect manipulation in the absence of communication logs. It cannot distinguish between genuine eccentricity and manufactured inconsistency without a sufficient volume of data. It is a diagnostic aid, not a replacement for human judgment.

**Version:** 2.1 (Rational Third-Party Edition)
