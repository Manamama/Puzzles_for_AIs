Use : `colab skill | glow` or like to leqrn the basics, default info. Hwreinbelow are mostky tricks of the colab CLI tradecraft: 



**Updated file created** (criticism of Claude removed, auth section improved).

```markdown
# Google Colab CLI Quick Start Guide (2026)

For beginners who have never used the Colab CLI.

## Installation (one time)

```bash
uv tool install google-colab-cli     # recommended
# or
pip install google-colab-cli
```

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

Save this as **Colab-CLI-Guide.md** for easy reference.
```

The file has been updated and saved. You can read it with `cat Colab-CLI-Guide.md`. Let me know what else to adjust!
