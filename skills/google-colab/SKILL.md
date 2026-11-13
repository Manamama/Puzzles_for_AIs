---
name: google-colab-cli-tradecraft
description: Field-tested tricks, pitfalls, and error-handling logic for operating Google's official `colab` CLI (google-colab-cli) from a script or shell — beyond the built-in `colab skill` basics. Use this whenever creating, reusing, or troubleshooting a `colab` session (colab new/sessions/status/stop/exec/drivemount), writing a bash wrapper around the CLI, or diagnosing a colab-cli error (503 Service Unavailable, 412/TooManyAssignmentsError, a `[?]` ghost session, a drivemount 404, or a `zmq.backend.cython` ImportError on `colab` itself). Also load it when *every* session shows `[?]`, or when `colab ssh -s NAME` / `colab exec -s NAME` behaves oddly because `sessions.json` was truncated by two concurrent invocations — in that state `colab ssh` silently rents a new VM instead of reattaching. Load this before adding any retry loop, poll, or wait logic around a `colab` command — several of its failure modes look retryable but are not, and this skill exists specifically to prevent looping around a wall that a loop cannot fix. Also load it when a session needs Google Drive (the `colab drivemount` consent flow, which is human-in-the-loop), or when the CLI is driven from a non-interactive agent shell where `colab console` would block forever. Also load it before planning a GPU / ML experiment on Colab (model install, `pip wheel` vs git+URL, OOM-by-arithmetic pre-flight, dtype vs GPU kernel support, driver-vs-CLI choice, smoke test, no-polling fire-and-forget with `/usr/bin/time -v`).
---

# Google Colab CLI Tradecraft

Use `colab skill | glow`  or `colab readme`  to learn the official basics first — this skill assumes that base knowledge and covers what it doesn't.

version 2.9.0

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
- `colab ssh -s name`: Shell over SSH; `--proxy-mode` makes it an OpenSSH ProxyCommand
- `colab log -s name [-t TYPE] [-o file]`: Structured history, incl. `drive_auth_needed`

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
- **`!` lines do not share shell variables.** Each `!` command runs in its own
  subshell, so `P=/some/path` on one line is *empty* on the next (and exported
  `PATH`/`HOME` vanish too). `rm -rf "$P"/lib/node_modules/x` then silently
  targets `/lib/node_modules/x` and reports success. Set the variable on **every**
  `!` line that uses it, or do the whole job in one `!bash -c '…'`.

## For an Agent: Use `colab exec`, Never `colab console`

- **`colab console`** is a raw interactive TTY. In a non-interactive agent shell it does not
  "fail" — it **blocks forever** waiting on a human. It is a human tool, not an automation
  entry point.
- **`colab exec`** with piped stdin is the agent entry point (see "Best Way to Run
  Multi-Line Commands" above). `colab new` is already synchronous, so
  `colab new … && printf '…' | colab exec -s NAME` is the whole recipe — no readiness poll.
- **`colab ssh` with a command** is the other agent-safe door: one command, then it
  returns, no tty needed (see "The Two Doors" below).

Minimal GPU recipe, start to finish:

```bash
colab sessions                         # quota check: stop stale sessions first (see the 412 section)
colab new --gpu T4 -s session_1_gpu    # synchronous; prints "[colab] Session READY." or exits non-zero
printf '!nvidia-smi\n' | colab exec -s session_1_gpu
```

### The `colab_me` wrapper alias — and its trap for agents

A convenience alias may exist in `Ubuntu_Scripts_1/utils/aliases3.sh`:

```bash
alias colab_me="bash ~/Downloads/GitHub/Ubuntu_Scripts_1/utils/colab_exec_wrapper.sh"
```

`colab_me gpu` creates/reuses a session named **`session_1_gpu`**
(`colab new -s session_1_gpu --gpu T4`), mounts Drive, and finally opens **`colab console`**.

Traps:

- Because it ends in `colab console`, the wrapper **hangs an agent indefinitely**.
- It hits the interactive Drive-consent prompt **once**, not twice (as of v2.4.3): the
  first `colab drivemount` triggers consent, the second is the deliberate warm-up repeat
  (see the drivemount section below). Notes claiming "blocks twice" predate that.
- It calls `colab drivemount … 2>/dev/null` twice, so the consent URL survives only
  because the CLI prints it to **stdout**, never stderr. Don't "tidy" that redirection.
- Feeding `stdin` from `/dev/null` does **not** skip the consent requirement; it only
  answers "Press Enter" with EOF, so the mount fails immediately. The wrapper then
  `exit`s on the second failed `drivemount` and never reaches `colab console` — which is
  why an agent can run the wrapper headlessly to surface the URL, yet still cannot
  complete a mount alone.
- Shell aliases are **not** loaded in non-interactive shells, so `colab_me` may not even
  exist in an agent's shell. Invoke the script path directly if needed; never assume the
  alias is present.

## The Two Doors: `exec` (kernel) and `ssh` (shell)

Both are non-interactive, both land on the same VM with the same `/content`.

```bash
# kernel door — python, with `!shell` lines allowed
printf 'import sys\nprint(sys.version)\n!ls /content\n' | colab exec -s NAME

# shell door — one command, then the bridge closes
ssh -o ProxyCommand="colab ssh --proxy-mode -s NAME" root@localhost \
  'hostname; uname -sr; ls -a /content'
```

- `colab ssh --proxy-mode` is an OpenSSH `ProxyCommand` bridge (WebSocket-stdio), not a
  replacement for `ssh`: you still run the real `ssh` client and hand it a command.
- `--identity` is optional — it defaults to the first of `~/.ssh/id_ed25519`,
  `~/.ssh/id_ecdsa`, and only selects which public key is sent in the
  `X-Colab-Ssh-Pubkey` header.
- A file written over ssh is immediately visible to the kernel through `colab exec`, and
  vice versa (verified both directions with a probe file). One filesystem, two doors.
- `df -h /content/drive` reports the **Drive quota** (e.g. 15 GB with most of it used),
  not the VM's local disk. Don't read it as free space on the runtime.
- `echo 'cmd' | colab console -s NAME` is the third, slower shell door: bash inside tmux,
  so piped output carries terminal-control bytes — filter with `grep -a`.

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

## When *Every* Session Shows `[?]` — Truncated `sessions.json` and the Silent Re-Create Trap

The single-ghost case above has a sibling that looks similar and is considerably worse.
If `colab sessions` lists **all** your runtimes as `[?]`, the local cache has not lost one
entry — it has lost everything:

```bash
ls -l ~/.config/colab-cli/sessions.json     # 0 bytes == empty, not "no sessions"
```

Cause: two `colab` processes writing that file at the same time. The write is not atomic,
so a `colab sessions` / `colab stop` / `colab log` issued while another `colab`
invocation is still alive (a long `colab exec` inside a wrapper, another terminal,
another agent) can leave the file truncated to zero. Nothing is recoverable from the CLI,
and Google has no idea about your names: a name is only a local nickname for
`endpoint + url + token`.

The dangerous part is what `-s NAME` means in that state:

| command | with a live local record | with `sessions.json` empty |
| --- | --- | --- |
| `colab exec -s NAME` | attaches to the existing kernel | `Session 'NAME' not found`, exits non-zero |
| `colab console -s NAME` | attaches | not found |
| `colab stop -s NAME` | stops that runtime | not found |
| `colab ssh -s NAME` | attaches to the existing runtime | **silently creates a NEW runtime** under that name (its own help: "`-s NAME` creates the session if missing") |

So `colab ssh` can look like a successful reattach while you are in fact sitting on a
brand-new VM with no Drive. Tell them apart in one command:

```bash
ssh -o ProxyCommand="colab ssh --proxy-mode -s NAME" root@localhost \
  'hostname; ls -a /content'
```

A bare `/content` (only `sample_data`, no `drive`, none of your files) means you were
rented a fresh machine, not reconnected; `hostname` differing between runs is the same
signal. The old runtime is now another `[?]` orphan, still holding quota and still
holding whatever Drive consent it had — consent belongs to the runtime, not the name, so
it does not transfer.

**Prevention:** never run two `colab` commands concurrently from different terminals or
agents — not even the harmless-looking `colab sessions` next to a long `colab exec`.
Serialise them, or give each run its own state file with the global `--config <path>`
flag. Check `ls -l sessions.json` whenever names behave strangely.

**Recovery:** none from the CLI, same as the single-ghost case. Terminate the orphans at
`https://colab.research.google.com` → Runtime → Manage sessions; any surviving local
record stays usable, all orphaned ones are lost.

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

Two structurally different reasons make that first call not finish, and they need
different responses — tell them apart with `colab log -s NAME -t drive_auth_needed`:

| what you see | meaning | response |
| --- | --- | --- |
| `404` on `…/api/kernels` | kernel gateway still waking | one more identical call |
| a `drive_auth_needed` event plus `Press Enter after you have granted access…` | this runtime has no Drive consent yet | hand the URL over, wait for the click, then call again |

Both can occur in the same run, in either order (consent first, then a 404 on the retry),
and neither is helped by a `while` loop.

`|| true` is preferable here to toggling `set +e`/`set -e` around the line: it's
scoped to exactly the one command that's allowed to fail, so a script running under
`set -e` still aborts loudly on any *other*, unexpected failure.

## Two Auths, Not One — and the Drive-consent Gate Is Human-in-the-Loop

`colab` involves two independent kinds of authorization, and an AI agent can complete only the first:

1. **CLI login** — `colab whoami`, via the OAuth/ADC flows in the Authentication section above.
   Machine-doable.
2. **Google Drive consent** — triggered the first time `colab drivemount` (or anything needing
   `/content/drive`) runs against a session. The CLI prints an
   `https://accounts.google.com/o/oauth2/v2/auth?…` URL and then blocks on:
   `Press Enter after you have granted access…`

The second is a **human-in-the-loop consent**: it needs a browser plus the account owner's
approval, so an agent **cannot** satisfy it alone. The correct agent behaviour is to
**surface the URL and stop**, let the human grant access and press Enter, then continue —
*not* to wrap `drivemount` in a retry loop. This is the "Golden Rule" failure shape again: the
blocker is a missing human action, not a transient error, so retrying manufactures nothing but
latency and misleading log noise ("failed 40 times" around a prompt waiting for a person).

**What the "Press Enter" actually reads: nothing that matters.** `automation.py` opens
`/dev/tty`, calls `readline()`, and discards the result (falling back to
`sys.stdin.readline()`, then `input()`, when there is no tty). Pasting the `4/0AUn6Hd-…`
code that Google sometimes displays and pressing Enter on an empty line are therefore
indistinguishable to the CLI. The browser approval is what grants Drive; the prompt is
only an acknowledgement that you are finished.

**Whether Google shows that copy-a-code page depends on the browser, not the CLI.** The
request is `response_type=none+gsession`: a browser that already holds a
`colab.research.google.com` session completes the round-trip silently, while a cold or
incognito browser falls back to showing a code. Both end in the same server-side grant —
don't read the difference as nondeterminism.

**No tty at all skips the gate rather than blocking.** In an agent shell, `open("/dev/tty")`
raises `OSError` (`No such device or address`), the fallback read gets EOF, and execution
continues immediately. The mount then fails — but a wrapper that exits on that failure
never reaches its `colab console`, so an agent can safely trigger the flow just to harvest
the URL. It still cannot complete a mount on its own.

Consequences worth remembering:

- The consent URL is **ephemeral** (note `redirect_uri=…/authorize-for-drive-credentials-ephem`)
  — per-session and time-limited, so a stale URL is useless; regenerate before handing it over.
- **Stopping a session drops the Drive mount**, and the next session needs Drive re-consented.
  So don't stop sessions casually "to be tidy" while the workflow still needs Drive — `colab
  stop` frees the concurrent-session slot but costs you the Drive authorization.
- **Consent belongs to the runtime, not the name.** A runtime the CLI has lost keeps its
  grant on Google's side but is unreachable by name; a fresh runtime created under the old
  name starts unconsented, so Drive must be approved again minutes after the first approval.

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

---

## The Drive-Backed `$HOME`: Why an Install There Costs ~5× — and the Knob That Fixes It

`setup/colab_paths_add.sh` (the file `colab_me` sources at the end) exports
`HOME=/content/drive/MyDrive/Shared` and `USER_BASE=…/.local`. Consequences:

- npm's **global prefix** and pip's **user base** both live on the FUSE mount, so
  a "temporary" Colab install persists into Google Drive and is billed against the
  Drive quota weeks later.
- **The mount cannot hardlink.** `@opencode/cli`'s `postinstall.mjs` calls
  `fs.linkSync(source, bin/opencode.exe)` and falls back to `copyFileSync`. On
  Drive that fallback always fires, so one install materialises as
  `bin/opencode.exe` **plus** the four `node_modules/@opencode/cli-linux-x64*`
  binaries: 5 real files, 3 of them byte-identical, 1238 MiB instead of 247 MiB.
- **npm cannot prune that for you, and no config key can.** The package ships 12
  platform packages; `os`/`cpu` filtering cuts them to 4 on linux-x64, and the
  survivors are indistinguishable to npm because the variant packages declare
  **no `libc` field** (their package.json holds only `cpu, license, name, os,
  repository, version`). npm's `libc` knob exists (`libc = null` in npm 11) but
  filters on a declared field, so it has nothing to match. Same for AVX2: only
  `-baseline` vs plain differs, and that is not expressible.

### Measured behaviour (npm 11.19.1 on Colab; 11.9.0 on a laptop — same results)

| Invocation | Platform packages installed | Files on disk |
|---|---|---|
| `npm i -g @opencode/cli` | 4 | 5 |
| `npm i -g --omit=optional @opencode/cli` | **4 — flag silently ignored** | 5 |
| `npm_config_omit=optional npm i -g …` | 4 — still ignored | 5 |
| `npm i --omit=optional --prefix DIR @opencode/cli` | **0** | **1** |

`omit=optional` is honoured only for **non-global** installs; the control case
(`esbuild`, whose platform package is the same kind of direct optional dependency)
behaves identically, so this is npm's global tree, not opencode's packaging.

The single file is not a degraded install. With the optional packages absent,
`postinstall.mjs` falls into `installPackage()`, which `npm install`s only the one
matching package into `os.tmpdir()`, copies the binary to `bin/opencode.exe`, and
deletes the temp tree — with `verifyBinary()` gating it, so a failed download
errors out instead of leaving a stub.

### Recipe A — the `--prefix` trick (recommended: one package, no prune, no risk)

A **non-global** install pointed at the prefix you want, plus one symlink:

```bash
DIR=/content/drive/MyDrive/Shared/.local     # or /root/.oc for an ephemeral copy
npm i --omit=optional --no-save --no-package-lock --prefix "$DIR" @opencode/cli
mkdir -p "$DIR/bin"
ln -sfn ../node_modules/@opencode/cli/bin/opencode.exe "$DIR/bin/opencode"
"$DIR/bin/opencode" --version                # must print v2.2.x
```

Verified end to end: exactly one 247 MiB file, and `$DIR` ends up holding **only**
`node_modules` — `--no-save --no-package-lock` stops npm writing `package.json`
and `package-lock.json` into the prefix (without them you get both, which is
harmless but untidy in `.local`). npm also creates
`$DIR/node_modules/.bin/{opencode,opencode2}`, so putting that directory on `PATH`
works even without the manual symlink.

Caveats: the payload lives in `$DIR/node_modules`, so `npm ls -g` does not list it
and `npm update -g` will not touch it — upgrade by re-running the same command.

### Recipe B — standard global layout, then prune (and prove it survived)

Use this when something depends on `npm root -g` / `npm ls -g`:

```bash
npm i -g @opencode/cli && \
  P="$(npm root -g)/@opencode/cli" && \
  "$P/bin/opencode.exe" --version && \
  rm -rf "$P"/node_modules/@opencode/cli-linux-* && \
  "$P/bin/opencode.exe" --version
```

The ordering is the whole point. A prune that runs after a failed install, or that
also removes `bin/opencode.exe`, leaves a dangling `…/bin/opencode` symlink — and
bash reports a dangling PATH entry as `command not found`, which sends you hunting
through `PATH` for a filesystem fault that is not there. Cost: 1238 MiB downloaded,
247 MiB kept.

### What does not work, and why

| Idea | Outcome |
|---|---|
| `npm config set omit optional` (global) | breaks `esbuild`, `rollup`, `sharp`, `@swc/*` — same publishing trick, and `rollup` has no fallback |
| `npm i -g @opencode/cli-linux-x64` | nothing to run: the variant package declares **no `bin`** |
| `--libc=glibc` | no-op: no variant declares `libc` |
| global install into an ephemeral `$HOME` | works, but still 5 files — ~1.2 GB of scratch **downloaded** per session |

Best of both worlds for a Colab wrapper: Recipe A with `DIR=/root/.oc` — 247 MiB
in the ephemeral overlay, **zero** bytes on Drive, nothing to prune, and only the
version string needs persisting.

On a normal ext4 machine the same package wastes less (the launcher is hardlinked,
so 4 files / ~915 MiB rather than 5), but the platform packages are still
installed; Recipe A avoids them there too, and Recipe B's prune frees nothing when
the surviving variant *is* the launcher's inode — `links` drops to 1 and the byte
count stays identical.

### Deleting over the mount is trash, not destruction — but `df` is not the receipt

- `rm` of a **file** on `/content/drive` leaves it with `explicitlyTrashed=true`
  (verified through the Drive API) — recoverable from Trash for 30 days.
- **Trash is per account, and not necessarily yours.** After `rm -rf` of four
  variant folders the package genuinely shrank (1238 → 247 MiB), yet a search as
  the collaborator credential returned nothing (`trashed = true and name contains
  'cli-linux'` → 0 items). The objects went to the trash of whichever account the
  **mount** runs as, which need not be the account behind your API credential.
  Sweep the web UI as that account.
- `df -h /content/drive` reports **Drive quota** and does not move until Trash is
  emptied; a 1 GB delete can show the same percentage twice. Never read `df` as a
  receipt for a delete — check `stat`/`ls` on the mount, or the API's `trashed`
  flag.
- Only the **owner** can trash. A collaborator holding the `writer` role gets
  `403 insufficientFilePermissions`, and "Remove from my Drive" reclaims zero
  bytes. Consequence: to clean a tree you must act as the account that owns it —
  in the CLI that means the account behind `colab whoami`, and for the browser
  flow the account that granted Drive consent.

### Never `du -sh` a multi-GB tree over the mount from the kernel

`colab exec` has **one** execution slot per session. A `du` walking 12 GB across
FUSE leaves `colab status -s NAME` reporting `Status: BUSY (exec(stdin))` for
minutes; every later `colab exec` returns nothing, and if the `colab_me` port
forward is still alive the ssh door answers:

```
[colab] Already-active SSH session (HTTP 429): another `colab ssh` is connected
```

Use bounded probes (`ls -l`, `stat -c '%s'`, `find -maxdepth 2`) instead. To
reclaim a wedged slot: `colab restart-kernel -s NAME` — it keeps the VM and the
mount, but **loses the env `colab_me` sourced**, so `HOME` reverts to `/root` and
`colab_paths_add.sh` must be re-sourced before any further install work. A bare
`exec` shell therefore has no Drive `.local/bin` on `PATH` and a `command not
found` there is the environment rather than a broken install — though since you
always re-enter through `colab_me`, that is a lab curiosity, not a daily hazard.

### `~` may resolve into a shortcut target

`realpath ~/Downloads` can return
`/content/drive/.shortcut-targets-by-id/<folder-id>/Shared/Downloads` — the same
bytes as `/content/drive/MyDrive/Shared/Downloads`, reached through a Drive
shortcut. Resolve with `realpath` before deriving paths from `$HOME`, and never
assume the `MyDrive/...` form is the only name for a file.

## GPU Experiments: Decide the Accelerator *Before* `colab new`

The session type is the first decision, not the first command. Read the
workload's code before creating anything: an install path that force-upcasts
to fp32 on CPU (`if device.type == "cpu": dtype = torch.float32`) plus a
multi-GB checkpoint announces "GPU" from the source. Creating a CPU session
first, discovering the mismatch mid-install, stopping it, and creating a GPU
session costs the session quota (**only one session at a time**) plus ~6
minutes of setup. Do the paper work first:

```bash
# before any session exists: read the code that decides the device
grep -rn "device.type == \"cpu\"" /path/to/package/          # dtype forcing
grep -rn "attn_implementation\|sdpa\|flash" /path/to/package # attention kernel
```

## Ship Code as a Wheel, Not a git URL or a Tarball

Three ways to get a repo-only package onto a VM, in order of cost:

- **`pip install git+https://…@<sha>`** — fails on a fresh clone with
  `fatal: reference is not a tree` when pip's shallow fetch cannot see a raw
  SHA not on the default branch. Also: the local clone's HEAD may not be on the
  public remote at all (verified — checkout failed there too).
- **`git archive` tarball** — works, but it is a two-step dance: ship the
  tarball, extract, `pip install /path`.
- **`pip wheel /local/clone -w dist/`** — once, on a machine that has the repo.
  Then `pip install dist/<name>-<ver>-py3-none-any.whl` on the VM: one file,
  exact code, no git on the target, exact-version provenance for free. The
  wheel *is* the tarball with its installation logic pre-resolved. Costs ~1
  minute to build and sidesteps every failure above.

## Pre-flight Memory Arithmetic on Paper

Before launching anything expensive on unfamiliar hardware, one paragraph on
paper: what gets allocated, where, in which dtype, and what the hardware
supports. Two of three failures in a real session were measurable-on-paper
errors:

- **Eager attention materialises N_heads × L² score tensors.** 16 heads ×
  11.6k tokens² × 2 B ≈ 8.6 GiB — bigger than a T4's free VRAM. This is
  arithmetic, not experiment; the OOM traceback was confirming a calculation.
- **The GPU's kernel support decides dtype choices.** T4 is sm_75: no native
  bf16, no FlashAttention. bf16 + SDPA falls back to the *math* backend, which
  materialises the same 8 GiB score tensor in fp32. fp16 gets the
  memory-efficient cutlass kernel and fits with room to spare.
- **Check where the dispatch happens.** `attention_interface =
  ALL_ATTENTION_FUNCTIONS.get_interface(self.config._attn_implementation, …)`
  reads the attribute *at forward time*, so setting it on the loaded model is
  the lever — no package edit needed. If the dispatch happened at import time,
  the same flag would be a no-op.

Empiricism is for the two things that remain uncertain *after* that paragraph —
not for the first two guesses.

## Read the CLI Defaults Before Trusting Them

The stock CLI had three traps: no attention-implementation flag (hard OOM),
`--max-new-tokens` default 2048 that silently truncates a 6562-token transcript
(confounding the very thing being measured), and no progress output until
completion. When the stock CLI is missing a knob, a ~10-line driver that
reuses the library's own functions (`generate_transcription`, the exporters)
keeps the experiment honest — only the kernel or the length cap changes, not
the science. Also check the output naming: `--out-dir` versioned from the
start beats renaming files afterwards.

## Smoke Test Before the Real Run

A 60-second clip exercises load → prefill → decode → export in minutes. Two of
the three failures in the session died during the *full* run instead of a cheap
probe. A smoke test is also the cheapest possible way to confirm the
`--model`/`--out-dir`/`--dtype` flags actually reach the code path you think.

## Fire and Forget — No Polling

Launch with a detached wrapper, then read the log on demand — there is no
condition on the remote that a sleep-loop on the local shell helps:

```bash
ssh -o UserKnownHostsFile=$K -o ProxyCommand="colab ssh --proxy-mode -s NAME" \
  root@localhost 'apt-get install -y time >/dev/null 2>&1; \
  setsid nohup /usr/bin/time -v python driver.py > /content/run.log 2>&1 < /dev/null & echo started'
```

- **`/usr/bin/time` is NOT installed on Colab images** — the launch dies with
  `nohup: failed to run command '/usr/bin/time': No such file or directory`
  and GPU idle for minutes. `apt-get install -y time` first (or check with
  `command -v time`).
- **Let the driver write its own summary JSON** (`peak_gpu_alloc_gb`,
  `prompt_len`, `generated_tokens`, `elapsed_sec`) — that plus the `time -v`
  block is the whole record, and neither needs a watcher.
- **Polling is pure theatre.** A background job does not get faster because
  it is stared at; every `sleep N; ssh … tail` is a turn spent on nothing.
  Check the log when you actually need the answer, not on a timer.

## One Experiment at a Time — Propose, Don't Bolt On

A second experiment bolted on mid-session (a CPU probe to answer a different
question) was never asked about, cost the user's message quota and trust, and
produced the polling-loop theatre above. If an experiment is worth running,
it is worth a one-line proposal: "want me to also run X, to answer Y?". Scope
additions the user did not request are the user's call, not the agent's.

## Moving Data: `colab upload` Beats the Script Payload ~20× (measured)

`colab run` ships *only the script text*: `sys.argv` is faked by embedding
`repr()`-quoted strings into one kernel code message. Data does not travel
with it. Two doors exist for bytes, and they differ by an order of magnitude
(measured on a home uplink, 2026-11-13):

| channel | payload | result |
| --- | --- | --- |
| script body / script args (kernel code message) | 47 MB | **never landed in 15 min** — upload-bound, first script line prints only after the whole payload arrives |
| `colab upload -s NAME file /content/file` | 34 MB | **45.7 s** |

Consequences:

- **`colab run` is for compute-only scripts.** A one-file script with data
  embedded (base64) only works while payload ≲ a few MB. Session+kernel
  overhead for a trivial script: **13.5 s** end-to-end (`--keep` probe).
- **For data, upload first, then exec**: `colab upload` needs an existing
  session (`-s`), so the sequence is `colab run --keep -s NAME setup.py` →
  `colab upload -s NAME …` → `colab exec -s NAME --timeout 7200 -f driver.py`
  → `colab stop -s NAME`. Four observable commands, no sleeps, no ssh.
- **`exec -f` streams progress and maps `sys.exit(N)` to the CLI exit code**,
  but its `--timeout` defaults to **30 s** — pass hours for real jobs. (`exec`
  appends the IPython "To exit: use…" warning and CLI log lines to stdout;
  `run`'s payload suppresses that warning — don't mistake the noise for
  script output when diffing transcripts.)
- A working end-to-end template (clone repo → `pip install .` → HF weights →
  fp16+SDPA transcription → summary JSON + transcript on stdout) lives in
  `templates/mtd_colab_driver.py` next to this file. Its setup measured
  8.7 s on Colab (torch/transformers preinstalled), model download 33 s.
- Don't `grep` a long *streaming* command — trimming `time -v` noise that way
  also blinds you to the progress that would have diagnosed the hang. Capture
  to a file (`> run.log 2>&1`), then inspect the file.
