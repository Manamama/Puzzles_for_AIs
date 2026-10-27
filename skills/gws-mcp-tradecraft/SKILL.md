---
name: gws-mcp-tradecraft
description: Field-tested operational knowledge for the google-workspace (GWS) MCP server — Docs, Gmail, Drive, Calendar, Tasks, Apps Script — covering what the individual tool descriptions do not say. Use whenever you read or write Google Docs programmatically, bridge Gmail attachments into Drive and Calendar, decode Calendar event URIs, script Apps Script through the MCP, or build Google Tasks trees; and load this BEFORE attempting any multi-step Gmail→Drive→Calendar pipeline, before regex-parsing a tool result as if it were data, or whenever a write appears to have silently failed. Its failure modes look retryable but are not, and its payload-handling rules are what keep multi-megabyte binaries intact.
---

# GWS MCP Tradecraft

Read the individual tool descriptions first — this skill assumes that base knowledge and covers what they do not say.

version 1.0.0

Distilled from a live multi-step automation session (2026). All identifiers removed deliberately: this skill may be shared; the lessons are what matter.

## Golden rules (read these before any GWS pipeline)

1. **Results are prose, not JSON.** Tool returns are human-readable sentences. Structured bits do exist — task/list/file IDs appear as `ID: <value>` — but payload data (base64, bodies) must be mined out carefully. Prefer *few* parses, *exact* matches.
2. **Verify by read-back, with the right flags.** Every write deserves a read; but some reads hide the field you care about unless you opt in (Calendar attachments need `detailed=true` AND `include_attachments=true`). A summary read that omits your field looks exactly like a silent failure — it is not.
3. **Know the patch semantics before you patch.** Several update calls REPLACE list-valued fields rather than merging (`manage_event.attachments` on update is the canonical example). Read the existing value, merge it yourself, then write the full list.
4. **Personal data stays personal.** Attachments fetched from a mailbox are personal data. Drive files are unshared by default — keep them that way unless the task says otherwise; never paste account addresses, file IDs, or mail content into public artifacts (issues, gists, docs meant to be shared).
5. **If a list call returns suspiciously empty, retry it once, alone.** Concurrent bursts against retry-wrapped servers can surface transient failures as a silent zero. A think-it-should-have-items result is not proof of emptiness.

## Code-mode sandbox laws (when scripting tool calls)

When composing tool calls inside a code-mode/sandbox execution rather than calling tools one by one:

- **No `Buffer`, often no `crypto.subtle`.** Hand-roll base64 decode/encode if needed. Do not assume Node or WebCrypto globals exist.
- **State does not survive between executions.** Variables from a previous execution are gone. Any flow where the *output* of one tool becomes the *input* of the next (download → upload) must live inside a **single** execution. Splitting it costs you a redundant download and a duplicate side effect.
- **Never echo large payloads into context.** Return sizes, hashes, IDs, and short previews — move the bulky value tool-to-tool inside the execution.

## Recipe: Gmail attachment → Drive file → Calendar event attachment

Why the Drive hop exists at all: Calendar's `EventAttachment` (`fileUrl`, `title`, `mimeType`) renders a true attachment card for **Drive** files. Gmail attachments are not Drive files, and there is no public API that converts a Gmail attachment part into a Drive file (the Drive API has no server-side "fetch from URL"). A copy step is structurally unavoidable unless you are happy with a plain hyperlink.

Canonical agent-side pipeline (all in one execution):

1. **Find the message** — `search_gmail_messages` with a quoted subject query; use `include_headers` to confirm sender/date. Deterministic queries beat fuzzy ones.
2. **Get the attachment pointer** — `get_gmail_message_content`. Attachments are listed at the **tail** of the response (filename, MIME type, size, attachment ID). If you slice the head to save tokens, you will slice the attachments off.
3. **Download the bytes** — `get_gmail_attachment_content(..., return_base64=true)` (pass `attachment_index`: it resolves Gmail's refreshed attachment IDs). The response is prose containing the payload; extract the longest run of `[A-Za-z0-9+/]` characters. The attachment_id is *also* base64-ish but uses the **URL-safe** alphabet (`-`, `_`), so a strict standard-alphabet regex naturally skips it — do not loosen the regex.
4. **Sanity-check before trusting the payload** — decode and verify: magic bytes for the format, and byte length exactly equal to the size Gmail reported. Two cheap checks that catch every truncation.
5. **Upload to Drive** — `create_drive_file(base64_content=..., content_mime_type=...)`; pass `base64_sha256` when hashing is available. For remote content, `fileUrl` makes the server fetch it directly — usage varies by deployment.
6. **Attach to the event** — `manage_event(action="update", attachments=[drive_url_or_id])`. Remember: this **replaces** the event's attachment list. Read first, merge, write.
7. **Verify** — `get_events(event_id=..., calendar_id=..., detailed=true, include_attachments=true)` and confirm filename/MIME/file ID. Then ask the human to look at the GUI; the GUI is the acceptance test, the API read is the smoke test.

### Streamlined alternatives (in ascending order of engineering effort)

- **Server-side bridge via Apps Script** — the MCP can create, edit, deploy, and run scripts (`manage_script_project` → `manage_script_content` → `manage_deployment` → `run_script_function`). Code that reads the mail and writes the file *in the same process* moves the blob inside Google; the agent only passes two small primitives (message id, attachment index) and receives back a file ID:

  ```js
  function gmailAttachmentToDrive(msgId, attIndex) {
    const att = GmailApp.getMessageById(msgId).getAttachments()[attIndex];
    const f = DriveApp.createFile(att.copyBlob());
    return { id: f.getId(), name: f.getName(), size: f.getSize() };
  }
  ```

  Two calls total, zero corruption risk, byte-parity checkable via `size`. First execution may trigger an OAuth consent screen — a human must approve once in the GUI.
- **A composite verb**, if and only if the MCP server source is locally editable: one tool that does fetch → upload → patch(merge) → verify → structured JSON, idempotent via filename+size dedupe. Do not build it on a server you cannot patch.
- **Direct URL attachment (experiment only)** — passing a mailbox-scoped attachment permalink as `fileUrl` may be accepted and render as a plain link chip, but it opens only for the mailbox owner and shows no preview. Zero-copy, zero utility for anyone else.

## Decoding Calendar event URIs

Google Calendar event links carry `?eid=` — base64 of `"<eventId> <calendarId>"` (space-separated). Decode it with any base64 decoder (note: sandbox runtimes may lack `Buffer`; hand-roll). Two quirks:

- Secondary-calendar IDs appear **truncated** in the URI (`...@g`); the real ID is `...@group.calendar.google.com`.
- Resolve calendar *names* to IDs with `list_calendars` rather than trusting memory; the eid path and the name path must agree before you write.

`get_events` takes `calendar_id` + `event_id`; the URI gives you both. When verifying write success, remember the attachment flags rule above.

## Google Docs API traps

- **Read as Markdown** — `get_doc_as_markdown` (comments: `inline` / `appendix` / `none`).
- **Append rendered Markdown** — `modify_doc_text` with `heading=<existing heading>` + `end_of_segment=true` appends formatted content (headings, emphasis, lists, code). It lands at the end of that heading's section — pick the final heading to append at the end of the document.
- **Bulk populate** — `manage_doc_tab(action="populate_from_markdown")` renders a whole Markdown document into one tab; cleanest large write, with `replace_existing` to control overwrite.
- **Find & replace cannot cross paragraphs.** A `find_text` containing a newline silently matches 0 — the operation reports "Replaced 0 occurrence(s)" and changes nothing. Do replacements within single paragraphs, or fix formatting after the fact.
- **There is no CHECKBOX in `insert_doc_elements`** (that call only offers UNORDERED/ORDERED). To get real, clickable Doc checkboxes: write the items as paragraphs (any style), then `create_bullet_list(list_type="CHECKBOX")` over their index ranges, or `update_paragraph_style(list_type="CHECKBOX")`.
- **Always index before you edit** — `inspect_doc_structure(detailed=true)` gives per-paragraph `start_index`/`end_index` and previews (`preview_chars=0` for full paragraph text). Body text starts at index 1; a table or suggestion in range shifts everything after it.
- **Cosmetic compression is normal** — Markdown renderers may merge paragraphs where you wrote blank lines; headings, lists, and bold survive. Do not chase it with patches unless the human cares.

## Apps Script via the MCP

- Lifecycle: `manage_script_project` (create) → `manage_script_content` (write files; a project is files + manifest) → `manage_script_version` (immutable snapshot) → `manage_deployment` (API executable) → `run_script_function` (`dev_mode` for latest saved code vs deployed version).
- `run_script_function` resolves the highest-version API-executable deployment automatically; pass `deployment_id` only to pin.
- Triggers: the REST API cannot create them — `manage_script_trigger` lists and deletes only.
- Return small JSON primitives from scripts (IDs, sizes), never bytes. The whole point of the script is that the bulky data never crosses the agent boundary.
- Scopes are real: a first run touching Gmail/Drive/Calendar raises a consent prompt; plan for a human click.

## Google Tasks as an agent-human shared plan

- `manage_task_list(create)` then `manage_task(create)`; ordering is explicit, not automatic — pass `previous=<sibling id>` to chain and `parent=<task id>` to nest (subtasks).
- Creation results are prose with `ID: <value>` — parse, then verify the whole tree with `list_tasks` (it renders parents as top-level and subtasks indented).
- `status="completed"` marks done; there is no bulk import — a 15-task plan is 15 sequential creates. Do them in one execution with chained `previous` references.
- Put the *how-to* in each task's `notes`: the task list becomes the durable, human-readable plan while the conversation is ephemeral.

## Anti-patterns (things that actually bit)

- Splitting a download/upload across two executions → lost payload, redundant side effect.
- Reading message content from the head only → "no attachments found" while attachments sit at the tail.
- Trusting `get_events` without `detailed`+`include_attachments` → "the attachment vanished" while the API had it all along.
- Patching `attachments` over an existing list → previous attachments silently erased.
- Cross-paragraph find/replace → 0 replacements, no error.
- Assuming a checkbox list type exists in the generic list inserter → use the dedicated list-type ops instead.
- Loosening the base64-matching regex → the attachment ID (URL-safe base64) gets mistaken for the payload.
