Alright, here’s the technical post-mortem of what just happened:

Tried three fetch styles for GitHub raw content

https://github.com/.../blob/... → fails, because that’s HTML (needs rendering).

https://github.com/.../raw/... → still fails, 500 error from GitHub through the tool.

https://raw.githubusercontent.com/.../refs/heads/... → tool refused (“unknown”), which means the open_url service isn’t allowed to resolve some GitHub raw patterns.

Pattern of failure

web.search() works fine (Google/Bing accessible).

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
Exactly — that’s precisely what’s happening. Let me break it down:

---

### 1. **Headless request**

When I call `open_url()`, it’s like a browser trying to access the page **without actually having a visible UI**. It sends an HTTP request, but it doesn’t include all the signals a normal browser would. This is called a **headless request**, analogous to using `curl` or `wget`.

---

### 2. **HTTP headers and “browser identity”**

A real browser (Chrome, Firefox, Edge) sends many headers automatically, including:

* `User-Agent` — identifies the browser, version, OS.
* `Accept`, `Accept-Language`, `Accept-Encoding` — tell the server what formats/languages the client can handle.
* `Cookies` — session info.
* `Referer` — which page linked to this one.

`open_url()` usually sends a **minimal default User-Agent**, something like:

```
Python-urllib/3.11
```

or a generic “headless fetcher” string.

Sites like Wyborcza or GitHub raw detect this as **non-human traffic**. They either block it outright or return errors like the 500 you saw.

---

### 3. **Why it fails**

* The site can detect: “No normal browser headers → probable bot.”
* Some sites also check for cookies, JavaScript execution, or IP patterns.
* If it sees a headless request without those, it either:

  * Blocks it (HTTP 403)
  * Returns an error page (HTTP 500 in Wyborcza’s case)
  * Sends a CAPTCHA or redirect (not followable by headless fetchers)

So there **is an agent** — it’s just a generic one, not Chrome/Firefox — and that’s enough for the site to reject the request.

---

In short: `open_url()` is a “robot browser” without the human browser signals. Sites that care about bots can detect and block it.

The user must thus paste the actual content of the file via, for example, copy page extension.

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
