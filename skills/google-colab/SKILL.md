---
name: google-colab-cli-tradecraft
description: Field-tested tricks, pitfalls, and error-handling logic for operating Google's official `colab` CLI (google-colab-cli) from a script or shell — beyond the built-in `colab skill` basics. Use this whenever creating, reusing, or troubleshooting a `colab` session (colab new/sessions/status/stop/exec/drivemount), writing a bash wrapper around the CLI, or diagnosing a colab-cli error (503 Service Unavailable, 412/TooManyAssignmentsError, a `[?]` ghost session, a drivemount 404, or a `zmq.backend.cython` ImportError on `colab` itself). Load this before adding any retry loop, poll, or wait logic around a `colab` command — several of its failure modes look retryable but are not, and this skill exists specifically to prevent looping around a wall that a loop cannot fix.
---

# Google Colab CLI Tradecraft

Use `colab skill | glow`  or `colab readme`  to learn the official basics first — this skill assumes that base knowledge and covers what it doesn't.

version 2.3.1

## Authentication

Try:

```bash
colab whoami
```

If you get a `DefaultCredentialsError`, set up authentication. Two main options:

1. **Browser flow** (easiest for interactive use):

```bash
colab --auth=oauth2 whoami
```

2. **Application Default Credentials (ADC)** — better for scripts/automation:

Follow the official guide: https://cloud.google.com/docs/authentication/external/set-up-adc

Or quick try:

```bash
gcloud auth application-default login
colab --auth=adc whoami
```

## Core Commands

- `colab new [-s name] [--gpu T4|L4|A100|...]`: Create session
- `colab sessions`: List sessions + short aliases
- `colab exec`: Run code (best with piped stdin)
- `colab run script.py`: One-shot fresh VM
- `colab stop -s alias`: Release session
- `colab console`: Raw bash shell

## Best Way to Run Multi-Line Commands

```bash
cat <<'EOF' | colab exec
!date
!uname -a
!pip install -q whisperx

import datetime
print("[remote]", datetime.datetime.now().isoformat())
import whisperx
print("whisperx imported successfully")
print("Version:", whisperx.__version__)
EOF
```

- Use `<<'EOF'` (single quotes) to avoid quoting problems.
- Put shell commands with `!`
- Put Python code directly.

## Timing Note

`time` around the command only measures the fast **local** part. Real remote execution time appears in the printed timestamps.

## Common Pitfalls & Lessons

- Short aliases (e.g. `c5a54b`) from `colab sessions` work best with `-s`.
- `colab run` needs a `.py` file — use `colab exec` for piped code.
- Sessions with `[?]` can be hard to re-attach.
- Always stop unused sessions with `colab stop`.

## `colab new` Is Already Synchronous — Don't Build a Readiness Poll

`colab new` blocks until the backend has actually finished assigning the VM. It only
returns once it has printed `[colab] Session READY.`, and it exits non-zero if
assignment fails. There is no separate "created but not yet ready" state to wait out.

Do **not** invent a poll loop, a sleep-and-retry-`colab status` check, or a dummy `colab exec` heartbeat to "wait for the session to come up." That's solving a problem
that doesn't exist and just adds latency and false-negative risk. The correct pattern
is the plain shell default:

```bash
set -euo pipefail   # -e: abort the script the instant any command exits non-zero
colab new --gpu T4 -s my_session
# reaching this line already means the session is ready — proceed directly
```

or equivalently, inline: `colab new --gpu T4 -s my_session && <next command>`.
Either one is just "check the exit code," nothing more elaborate is needed.

## Two Different Failure Shapes for `colab new` — Don't Treat Them the Same

`colab new` can fail for two structurally different reasons. Telling them apart
matters, because only one of them is helped by retrying:

1. **Transient backend error — `503 Service Unavailable`.** Google's assign endpoint was momentarily overloaded. This *can* legitimately be
   retried (with a short backoff) and will often succeed a few seconds later.

2. **`412 Precondition Failed` → `TooManyAssignmentsError`.** This means the account has already hit its concurrent-runtime quota — there is
   an existing active session (yours or leftover from an earlier run) still holding
   an assignment. **Retrying does nothing** — the condition won't clear on its own,
   no matter how long you wait or how many times you ask. The quota is enforced
   per-account by Colab's backend and applies uniformly across CPU/GPU/TPU — a CPU
   session and a GPU session both count as "1" against the same limit, so switching
   hardware type does not sidestep it. The known-tier ceiling has been reported as
   1 concurrent session on the free tier and up to 3 on Colab Pro, but Google does
   not publish or guarantee an exact number — treat it as "small and account-tied,"
   not as a fixed constant to hardcode.
   
   The fix is to free the quota, not to wait: check `colab sessions` before creating
   a new one, and `colab stop` anything already listed there (especially anything
   left over from a previous run of your own script that didn't clean up after
   itself). A robust wrapper should default to this defensively — stop stale
   sessions first — rather than assuming the account starts clean.

Practical takeaway: on a `colab new` failure, look at *which* error it is before
deciding what to do. A bare retry loop that doesn't distinguish the two will spin
uselessly forever against a `412`, while correctly recovering from a `503`.

## Don't Confuse a Script Syntax Error With a Runtime Error

If a `.sh` wrapper aborts partway through with something like `unexpected EOF while looking for matching` after an apparently unrelated Colab
error upstream, don't assume the two are connected. Run `bash -n script.sh` first
to check pure syntax in isolation — a stray quote, an unclosed heredoc, or a leftover
character from editing can produce a parse-time error that has nothing to do with
whatever Colab-side failure happened earlier in the same run, even though they show
up in the same terminal output and look causally linked.

## If `colab`/`jupyter_kernel_client` Fails to Import (`zmq.backend.cython` errors)

If invoking `colab` itself throws `ImportError: cannot import name '_device' from partially initialized module 'zmq.backend.cython'`, this is not a bug in `google-colab-cli`. It happens when an
old `pyzmq` (pre-26.x) was already present on the machine from unrelated prior work
(commonly pulled in by `ipykernel`) before `google-colab-cli` was installed — pip
only upgrades a dependency if the currently installed version fails its declared
lower bound, so a pre-existing old `pyzmq` silently satisfies `jupyter_client`'s loose `pyzmq>=25.0` constraint without actually being ABI-compatible with it. This is
environment-specific, not reproducible on a clean install. Fix: `pip install --user --no-cache-dir --upgrade jupyter_client` (its own dependency resolution will pull a
compatible `pyzmq`). Don't chase `zmq` (no underscore) — that's an unrelated
placeholder package on PyPI, not `pyzmq`.

## The Golden Rule: A Loop Cannot Manufacture a Resource That Doesn't Exist

The single most important instinct to suppress: when a command fails, the reflex to
wrap it in a bigger retry loop, a longer sleep, or more attempts is only valid if the
underlying blocker is genuinely time-bound (see the `503` case above). It is **not**
valid for every failure, and applying it universally is the same failure mode as
"if `sudo` didn't work, `sudo` harder" — adding force to a problem that isn't about
force. Before adding *any* retry/wait logic, first identify: is the blocking
condition something that resolves on its own with time, or is it a hard external
state (quota, capacity, permissions, config) that no amount of asking again will
change? If it's the latter, looping just burns time and produces misleading log
noise ("failed 40 times!") around what is really a single, simple, unretryable fact.
The sections below are two concrete instances of this.

## Ghost Sessions — `[?]` Entries the CLI Can't Manage Anymore

A session can end up in a state where `colab sessions` still lists it (with a `[?]`
in place of its name) but `colab stop`, `colab console`, etc. all say
`No active sessions found`. This happens when the CLI's *local* session cache
(`~/.config/colab-cli/sessions.json`) and Colab's *backend* assignment state
diverge — typically after the CLI itself detects a broken connection
(`Session 'X' appears to be lost (404/401). Cleaning up.`) and wipes its local
record of the session, while the backend still has the VM assigned to your account.
`colab sessions` queries the backend directly, so it keeps showing the orphan;
`colab stop`/`colab console` resolve against the local cache, which is now empty —
hence the contradictory-looking output.

**There is currently no CLI command to fix this** (no `colab adopt`/reattach
command exists yet as of this writing — it's an open feature request,
see `googlecolab/google-colab-cli` discussion #49). Don't loop `colab stop`,
don't retry `colab sessions`, don't try `-s [?]` — none of it will work, because the
local state the commands need simply isn't there anymore.

**The actual fix:** open `https://colab.research.google.com` in a browser → Runtime
→ Manage sessions, and terminate the orphaned runtime from there. That UI reads
from the same backend `colab sessions` does, independent of the CLI's local cache,
and terminating it there frees the concurrent-session quota immediately.

## `colab drivemount` Failing Once Right After (Re)Connecting Is Expected

The very first `colab drivemount` (or any `colab exec`-based automation) call
against a session that was just created, or reconnected to after being idle, can
throw a `404` on `.../api/kernels` while the remote kernel-gateway wakes up. A
second call immediately after typically succeeds. This is a known warm-up quirk,
not a bug to retry-loop around — one deliberate second attempt is the fix, not a
`while` loop:

```bash
colab drivemount -s "$SESSION_NAME" || true   # expected first-call 404 while gateway wakes; second call is the real one
colab drivemount -s "$SESSION_NAME"
```

`|| true` is preferable here to toggling `set +e`/`set -e` around the line: it's
scoped to exactly the one command that's allowed to fail, so a script running under
`set -e` still aborts loudly on any *other*, unexpected failure.

## `503 Service Unavailable` on `colab new --gpu ...` Is Often NOT Transient — It Can Mean "No GPU Capacity, Full Stop"

This is the most important failure shape to get right, because it looks identical
to the genuinely transient `503` case (same error text, same status code) but
requires the opposite response.

**Symptom:** `colab new --gpu T4 -s NAME` repeatedly throws
`ColabRequestError: ... Service Unavailable`, even after waiting a minute or more
between tries, even with a fully clean session state (`colab sessions` confirms
nothing else is assigned).

**How to tell which case you're in, in one step:** try `colab new -s NAME` with
*no* `--gpu`/`--tpu` flag (plain CPU). If that succeeds instantly while the GPU
variant keeps failing, the backend itself is fine — there is simply no GPU capacity
available for your account right now. This is Google's free-tier dynamic usage-limit
system (documented, if vaguely, at
https://research.google.com/colaboratory/faq.html#usage-limits), the same wall the
browser UI shows more legibly as *"Cannot connect to GPU backend — you cannot
currently connect to a GPU due to usage limits."* `google-colab-cli` just passes
this straight through as a raw `503` instead of that friendlier message.

**Do not build a retry loop for this case.** No amount of retrying, backoff, or
waiting a fixed short interval manufactures GPU capacity that Google isn't
allocating to a free-tier account at that moment — this can persist for minutes to
(per widely reported user experience) hours. A robust script should fail fast and
say so plainly, not spin. If GPU access is genuinely required and blocked, the only
real levers are: try a different accelerator (`--gpu L4` instead of `T4` —
availability is tracked per chip type, not as one pooled resource), wait an
unknown/long amount of time, or purchase compute units (Pay-As-You-Go or Colab Pro)
to move into a better-prioritized queue — waiting inside the script fixes nothing
that purchasing or switching doesn't also require.

**What a "compute unit" actually is**, for sizing that last option: it's a
currency-like credit (~$0.10 each), *not* a fixed block of time — different
hardware burns it at different rates, so "units" alone don't tell you how long
you'll get:

| Hardware    | Approx. units/hour          | Approx. hours per 100 units |
| ----------- | --------------------------- | --------------------------- |
| TPU         | ~1.76/hr                    | ~57 hrs                     |
| T4          | ~1.76–1.96/hr               | ~51–57 hrs                  |
| L4          | somewhat above T4           | —                           |
| V100        | ~5/hr                       | ~20 hrs                     |
| A100 (40GB) | ~13–15/hr                   | ~6–8 hrs                    |
| A100 80GB   | highest of the standard set | —                           |

Google doesn't publish a fixed, guaranteed rate table, and even sub-variants within
one chip type (e.g. A100 40GB vs 80GB) can burn differently — treat these as rough
planning numbers, not contract terms. Also note: a fresh account sitting at
`0 compute units` on the free tier is not "out of units" in the exhaustion sense —
units are a Pro/Pay-As-You-Go concept entirely separate from the free tier's GPU
usage-limit gate; buying units doesn't top up a meter you were draining, it moves
you into a different allocation queue.

**Bottom line for an AI operating this CLI:** if a GPU session request fails and a
same-second CPU request on the same account succeeds, stop — report the GPU
capacity wall plainly and ask the user how they'd like to proceed (different chip,
wait, upgrade, or fall back to CPU) rather than retry-looping a request that a
CPU-only workload doesn't even need in the first place.
