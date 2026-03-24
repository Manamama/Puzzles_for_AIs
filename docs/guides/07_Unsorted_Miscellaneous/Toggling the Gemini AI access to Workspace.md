1. Go to : https://mail.google.com/mail/u/0/#settings
2. Find: 'Google Workspace smart features:
Choose to personalise your experience with smart features across Workspace and other Google products. Workspace includes Google apps for businesses and school, such as Gmail, Chat, Meet and Drive.' 
3. Click there "Manage Workspace smart feature settings" for pop up. (Nota bene: it is blocked by Ublock etc. on mobile GUI, seemingly) 
4. Gemini AI's templated (but cryptic, as the URL is not right) prompt says that the both of these settings need to be turned on (apart from man other ones):
'
Google Workspace smart features
A. **Smart features in Google Workspace**

When you turn this setting on, you agree to let Google Workspace use your Workspace content and activity to personalise your experience across Workspace. Workspace includes apps for businesses and schools, such as Gmail, Chat, Meet, Drive and more. To learn more, visit the Workspace website. Smart features include:
Show events from Gmail in Calendar (such as flight itineraries and invitations)
Personalised search (such as keyword suggestions, file suggestions and more relevant results)
Ask Gemini to summarise content, create drafts and find key information, along with other Gemini for Workspace features

Experiment shows that it is NOT needed for Gemini AI accessing e.g. GCal via function call. 

B. **Smart features in other Google products**

When you turn this setting on, you agree to let Google use your Workspace content and activity to personalise your experience in other Google products. Smart features include:
Restaurant reservations and takeaway orders in Maps
Suggested tickets, loyalty cards and other passes in Wallet
Answers and reminders in Google Assistant
Suggestions and answers in the Gemini app
Learn more about these smart features
'

In summary, the requirement for two toggles (Settings A & B) instead of one, became the standard user experience starting in January 2025.


4. Another setting to turn on is here: https://gemini.google.com/apps "Google Workspace
Summarise, find and get quick answers from your own content to fuel your personal journeys

Gmail
@Gmail
Learn more

Google Calendar
@Google Calendar
Learn more

Google Docs
@Google Docs
Learn more

Google Drive
@Google Drive
Learn more

Google Keep
@Google Keep
Learn more

Google Tasks
@Google Tasks
"

Read: https://support.google.com/a/answer/15293691?hl=en and https://support.google.com/gemini/answer/15305236?hl=en&co=GENIE.Platform%3DAndroid



That is a great idea—let's consolidate the findings to create a minimal, necessary setup.

Based on our experiments and the most up-to-date documentation, here is the minimal set of switches that must be toggled **ON** (an AND operation) for Gemini to access your Google Calendar (GCal) and other Workspace content:

| \# | Setting Name | Location / Context | Status |
| :--- | :--- | :--- | :--- |
| **1.** | **Smart features in other Google products** | Found within the Gmail Settings pop-up, accessed via: [$\text{https://mail.google.com/mail/u/0/#settings/general}$](https://www.google.com/search?q=https://mail.google.com/mail/u/0/%23settings/general) then **Manage Workspace smart feature settings**. | **ON** |
| **2.** | **Google Workspace Extension Toggle** | Managed in the Gemini Apps settings: [$\text{https://gemini.google.com/apps}$](https://gemini.google.com/apps) | **ON** |
| **3.** | **Final Workspace Consent Prompt** | A one-time, explicit "Are you OK?" prompt that appears the very first time you use the feature. | **Accepted** |

### Key Observations:

  * **Setting \#1** is the **data sharing prerequisite**. If this is OFF, the data is blocked from leaving Workspace, and the Gemini App toggle (Setting \#2) is functionally useless.
  * **Setting \#2** is the **feature activation switch** you tested. This acts as the direct on/off control for the Gemini tool itself.
  * **Setting \#3** is a **legal/privacy confirmation** that must be accepted once and ensures the *use* of the data is consented to.

While **"Smart features in Google Workspace"** (Setting A in your previous list) is often *also* required for the internal components to work seamlessly, the combination of **1, 2, and 3** is the verified minimal set needed to power external applications like Gemini with your GCal data.


Grok AI's summary: 
#,Setting Name,Location/Access Path,Purpose & Direct Tie to GCal Access,Status Requirement,Source Citation
1,Smart features in other Google products,"Gmail web: mail.google.com/mail/u/0/#settings/general → Scroll to ""Google Workspace smart features"" → Click ""Manage Workspace smart feature settings"" (pop-up with checkboxes). Web-only; syncs across devices but blocked by ad-blockers on mobile.","Unlocks Workspace data (e.g., GCal events) for external apps, explicitly including ""suggestions and answers in the Gemini app."" This is the sole data-export gate for non-Workspace integrations; without it, Gemini's backend cannot query or display GCal results, yielding errors like ""required Gmail settings are off"" (plural in templating, but singular in effect here). Your experiments confirm: this toggle alone broke/resumed full execution. Quote: ""When you turn this setting on, you agree to let Google use your Workspace content and activity to personalise your experience in other Google products. Smart features include: [...] Suggestions and answers in the Gemini app.""",Must be toggled ON (checkbox checked). Default: OFF in EEA/UK/Japan/Switzerland; user-overridable elsewhere.,","
2,Google Workspace Extension Toggle,"gemini.google.com/apps (or /extensions; auto-redirects) → Locate ""Google Workspace"" in extensions list → Toggle slider. Requires same-account sign-in as Workspace.","Activates Gemini's execution layer for Workspace tools, routing ""@Google Calendar"" prompts to backend APIs. Prerequisite: #1 must permit data flow; otherwise, toggle appears but fails silently on use. Your OFF/ON test directly halted result display while allowing background queries—exposing it as the frontend enforcement point. Quote: ""To create and manage your Google Calendar events, you'll need to connect Google Workspace to Gemini Apps. [...] If you haven't connected Google Workspace, you'll get the option to connect it.""",Must be toggled ON (slider right). Visual icon confirms; one-time but revocable.,","
3,Final Workspace Consent Prompt,"Dynamic overlay: Triggers on first GCal prompt (e.g., ""@Google Calendar find concerts"") post-#1/#2. Phrased as ""Are you OK with Gemini using your Workspace [data for features like event search]?"" with privacy links.","Enforces explicit legal buy-in for data usage; non-skippable and non-revocable without full reset. Blocks tool execution until clicked—your transcript's ""fourth setting"" matches this verbatim. No toggle; it's a one-way valve. Docs imply it's bundled in the ""on-screen instructions"" after connection.","Must be explicitly accepted (""OK"" or equivalent). No URL; app-served.",","
4,Keep Activity (New Addition: Unmentioned Prerequisite),"myactivity.google.com/product/gemini → Toggle ""Keep Activity"" slider. Applies globally to Gemini features.","Enables retention of interaction history, without which GCal tools are outright unavailable in Gemini (e.g., search fails at initialization). This is a silent global kill-switch; docs state calendar access ""only available when Keep Activity is on."" Omission in prior lists reveals docs' layered opacity—it's not in Gmail flows but gates all persistent features. Quote: ""The supported calendar apps are only available in Gemini Apps when Keep Activity is on.""",Must be toggled ON. Default: ON for most; auto-delete options (3/18/36 months) available but irrelevant to access.,




The default-off status for the "Smart features in other Google products" toggle in the EEA (including EU states), UK, Japan, and Switzerland stems directly from region-specific data protection laws that mandate explicit, affirmative user consent (opt-in) for non-essential data processing, such as sharing Workspace content (e.g., emails, calendar events) with external AI tools like Gemini for "personalization." These laws classify such uses as high-risk profiling or automated decision-making, where default-on would violate consent requirements and expose Google to crippling fines (up to 4% of global revenue under GDPR). Elsewhere—primarily the US, Canada, Australia, and much of Asia/Latin America—laxer frameworks (e.g., CCPA's opt-out model) permit default-on, enabling Google to harvest and monetize data aggressively from the outset, with reversal buried in fragmented settings. This isn't benevolence; it's coerced minimal compliance where regulators hold leverage, revealing the model's core: unchecked extraction masquerading as convenience.

### Raw Legal Triggers by Region
- **EEA (EU + Norway, Iceland, Liechtenstein) and UK**: Enforced by GDPR (EU Regulation 2016/679, post-Brexit UK GDPR) and the EU's Digital Markets Act (DMA, 2024). Article 6(1)(a) of GDPR demands "freely given, specific, informed and unambiguous" consent for processing personal data beyond strict necessities; default-on counts as invalid pre-ticked consent, per EDPB Guidelines 05/2020. The DMA further restricts gatekeepers like Google from bundling consents or using data for ad targeting without granular opt-in. Google's support pages obliquely nod to this: "We rely on your consent for Google to use your Workspace Content & Activity... To provide smart features that personalize your experience in other Google products outside of Workspace." Violations have netted €50M+ fines (e.g., Google's 2019 CNIL slap for opaque consent). For Gemini, this blocks backend access until toggled, as data export to external apps triggers "transfer" scrutiny under Chapter V.

- **Switzerland**: Driven by the revised Federal Act on Data Protection (FDPA, effective September 1, 2023, with full enforcement by 2025), which mirrors GDPR's consent model (Art. 6: explicit for sensitive/automated processing) but adds nationality-based protections for Swiss residents. Google's July 2024 policy update explicitly extended EEA/UK-style consents to Switzerland for ad products, extending to Workspace features to preempt FDPIC enforcement. Quote from Google's announcement: "In response to evolving data privacy regulations, Google has recently introduced new consent requirements specifically targeting Switzerland." Fines reach CHF 250,000 per violation, but the real bite is reputational—Switzerland's adequacy decision with the EU hinges on FDPA alignment.

- **Japan**: Tied to the Act on the Protection of Personal Information (APPI, amended 2020/2022), which requires opt-in consent for third-party data sharing (Art. 16 bis) and sensitive information handling (Art. 18), especially for "provision to third parties" like Google's external AI ecosystem. Japan's Personal Information Protection Commission (PPC) deems default-on as non-compliant for cross-border transfers, per 2022 guidelines on AI/data analytics. No direct APPI quote in results, but grouping with GDPR regions signals adequacy reciprocity: Japan secured EU adequacy in 2019 by adopting opt-in for non-essential uses, forcing Google's hand to avoid PPC audits or trade barriers. Post-2022 amendments, fines hit ¥100M (~$670K), though enforcement lags EU rigor.

