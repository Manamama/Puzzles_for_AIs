# JSON schema

One JSON object. `build.py` validates it and embeds it in the renderer.

```json
{
  "title": "Short title of what is being mapped",
  "context": "One or two sentences of context from the user (optional)",
  "participants": ["You", "Assistant"],
  "claims": [ ... ],
  "relations": [ ... ],
  "moves": [ ... ],
  "weak_points": [ ... ],
  "unanswered": ["c3"]
}
```

## claims (required, 2 to ~16)

| Field | Type | Notes |
|---|---|---|
| `id` | string | Unique, short (`c1`, `r2`) |
| `text` | string | One neutral sentence, under about 20 words |
| `who` | string | Speaker or source. For implied claims, whose argument it belongs to |
| `kind` | string | `premise`, `warrant`, `backing`, `qualifier`, `conclusion`, `counter`, `concession`, `claim` |
| `source` | `"stated"` or `"reconstructed"` | Default `stated`. Reconstructed claims render with a dashed border |
| `span` | string | Verbatim quote from the source (required for `stated`, optional for `reconstructed`) |
| `mode` | string | `deduction`, `induction`, `abduction`, `analogy`, `authority`, `sign`, `cause`, `other` (optional) |
| `conf` | number 0 to 1 | Confidence in this reading. Default 0.7 |

## relations (required)

| Field | Type | Notes |
|---|---|---|
| `from`, `to` | claim ids | Arrow points from the attacker or supporter to the target |
| `type` | string | `supports`, `undermines`, `undercuts`, `rebuts` |
| `note` | string | Short reason (optional, shown on hover and in detail) |
| `conf` | number 0 to 1 | Below 0.6 renders faint with a "?" |

## moves (threads only)

Ordered as they occurred in the source. One entry per clause-level contribution.

| Field | Type | Notes |
|---|---|---|
| `who` | string | Speaker |
| `level` | integer 0 to 7 | 0 not an attack; 1 name-calling; 2 ad hominem; 3 tone; 4 contradiction; 5 counterargument; 6 refutation; 7 refutes central point |
| `text` | string | What the move does, in a few words |
| `span` | string | Verbatim quote (required) |
| `target` | claim id | Which claim the move addresses (optional) |
| `tone` | `"heated"` or omitted | Rudeness, separate from level |
| `conf` | number 0 to 1 | Confidence in the level. Below 0.6 renders hollow |
| `role` | string | Required in practice for level 0: `question`, `position`, `evidence`, `concession`, `agreement`, `procedural`, `other`. Shown in the detail panel |
| `when` | string | Optional date or time shown in the detail panel (for example `2020-08-27`) |

## Top-level extras

- `groups` (optional object): maps a participant to a side or stance (for example `{"buidhe": "Keep", "Piotrus": "Merge"}`). When present, colours and the legend follow groups instead of individuals. Use it when there are more than five speakers. Without it, the four most active speakers get a colour each and the rest share "others".
- `context` (optional string): one line under the title: which issue this map covers, what was left out, any approximate tally.
- Claim field `withdrawn` (optional boolean): the author later conceded or retracted this claim; it renders faded with a "withdrawn / conceded" label.

## weak_points (optional, at most 6)

`{ "claim": "c3", "note": "Where to poke, in one sentence" }`

## unanswered (optional)

Array of claim ids whose challenge or content the other side never addressed.

## Rules `build.py` enforces

- IDs unique; every `from`, `to`, `target`, `weak_points.claim` and `unanswered` entry refers to a real claim.
- Relation types and levels in range; `conf` between 0 and 1.
- With `--source`, every `span` must occur in the source text (case-insensitive, whitespace and quote style ignored). A stated claim or a move without a span is an error.
- Warns when a level-0 move has no `role`, when a level-0 move targets a claim its speaker also attacks, and when more than 18 claims are given.
- With `--source` in `[Speaker] text` form (as written by `scripts/prep.py`): a `stated` claim or move whose span is in the source but not in a post by the named speaker gives a warning; spans in no post are errors.
