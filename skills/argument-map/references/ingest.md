# Getting a discussion into the skill

Lessons learnt on the RSN "ADL and Wikipedians" thread (2026-11-06), kept as guidance
rather than machinery: **where the text comes from decides how much structure survives,
and adaptation is cheaper by hand than by a fifth bespoke parser.**

## Route A — browser-saved page (Ctrl+S on the rendered thread). Best structure for least effort

A browser save keeps the full rendered DOM, and MediaWiki's DiscussionTools marks every
comment in two stable, locale-independent places:

    <span data-mw-comment-start id="c-<account>-<YYYYMMDDHHMMSS>-<parent account>-<parent ts>">
    <span data-mw-comment-sig ...>            <!-- start of the signature -->

The id alone gives speaker, timestamp and *which comment it replies to*; a null tail is a
thread root. Lookup parents by (account, timestamp) — ids embed only one level of
parentage, never a full chain. The signature is cut at its marker, so nested replies are
excluded from the parent's text for free.

    python scripts/wikitalk.py PAGE.html --section "Anti-Defamation" --tree <comment-id> --outdir work/frag

writes the skill's `[Speaker] text` source plus `posts.json`, with an indented outline on
stdout. `--grep TEXT` finds a comment and its id (e.g. to locate a fragment the user
points at); `--outline all` shows the whole section's tree.

What needs adapting by hand, per export, and why this is not automated further:

- **Signature decoration.** Crowns, superscripts, pronoun parentheticals, multi-part
  custom sigs. The parser ships with an empty `NAMES` table on purpose: add the two or
  three variants the current page actually shows, then eyeball the printed speaker list.
- **Localized UI strings.** "talk", "contribs", "Reply", timestamp phrasing — the
  markers and comment ids are code-level and survive translation (Arabic, Polish,
  Klingon…), but everything matched in *visible* text is locale-specific. On a
  non-English wiki, extend `clean_name`; never trust it unread.
- **Comment links in body text** (`[[User:X|…]]`, templates) can imitate signatures;
  the marker cut keeps bodies verbatim, so oddities show up in the report, not silently.

## Route B — the MediaWiki API. Canonical, but not offline

`action=parse` and the discussiontools modules return the same structure live. Use it
when network and rate limits allow; the user's Ctrl+S beats it for speed, works offline,
and captures exactly what the discussion looked like — including stuff (renamed users,
hidden sigs) the API renders differently.

## Route C — flattened text (copy-paste, print-to-text). Last resort

Reply nesting is lost; attribution and reply targets become guesses.
`scripts/prep.py` handles the common dump shapes (AfD, phpBB, `[Speaker] text`) and
prints flags — flags are warnings, not truth: **read the report**.

## Other sites

phpBB, Discourse, HN, mailing lists: no DiscussionTools markers, different everything.
Do not script a new guesser per site; build the `[Speaker] text` file by hand — one post
per line, verbatim, chrome removed — and spend the saved effort on the mapping itself.

Whatever the route: leave out of the source what is not part of the argument (profile
blocks, personal details), keep post text verbatim, and let `build.py --source` check
every quote against what actually stands in the file.
