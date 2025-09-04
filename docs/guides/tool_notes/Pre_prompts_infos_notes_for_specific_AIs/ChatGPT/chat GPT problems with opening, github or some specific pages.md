Alright, here’s the technical post-mortem of what just happened:

Tried three fetch styles for GitHub raw content

https://github.com/.../blob/... → fails, because that’s HTML (needs rendering).

https://github.com/.../raw/... → still fails, 500 error from GitHub through the tool.

https://raw.githubusercontent.com/.../refs/heads/... → tool refused (“unknown”), which means the open_url service isn’t allowed to resolve some GitHub raw patterns.

Pattern of failure

search() works fine (Google/Bing accessible).

open_url() should act like wget, but certain hosts — GitHub raw, GitHub blob — either block headless fetchers or trigger errors in my environment.

The error messages (500, “unknown URL”) suggest that the browsing service proxy, not GitHub itself, is enforcing restrictions on some URL classes.

Implication for future searches

For “normal” sites (blogs, docs pages, non-GitHub sources), open_url does succeed in giving me the raw page.

For GitHub specifically, the open_url tool appears unreliable (likely deliberate anti-bot handling combined with my environment’s proxy restrictions).

So: GitHub is a special case — if the file is crucial, either:

Mirror to another host,

Or have the user paste/upload the file,

Or I can pull secondary mirrors (npm, PyPI, docs hosting, forks) via search().

⚖️ Conclusion:

You were right to suspect “Robostakes” / anti-bot protections.

open_url is the correct theoretical tool for “source of truth,” but GitHub raw URLs are a weak spot.


Maybe via:

```
~/downloads $ cat  requests_test.py
import requests

url = "https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/checkpointing.md"
response = requests.get(url)

if response.status_code == 200:
    content = response.text  # raw Markdown text
    print(content[:500])     # first 500 characters for sanity check
else:
    print(f"Failed to fetch: {response.status_code}")


~/downloads $ python requests_test.py
# Checkpointing

The Gemini CLI includes a Checkpointing feature that automatically saves a snapshot of your project's state before any file modifications are made by AI-powered tools. This allows you to safely experiment with and apply code changes, knowing you can instantly revert back to the state before the tool was run.

## How It Works

When you approve a tool that modifies the file system (like `write_file` or `replace`), the CLI automatically creates a "checkpoint." This checkpoint inclu
~/downloads $
```
