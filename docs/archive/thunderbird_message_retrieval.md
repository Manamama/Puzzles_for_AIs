# How to Read Thunderbird Messages from the Command Line

This document outlines methods for accessing Thunderbird email messages on a Unix-like system from the command line.

## Method 2: Parsing Mbox Files with Python (Recommended for Full Content)

This is the most robust and reliable method for reading the full content of emails. It correctly handles complex email structures, headers, and character encodings.

**Pros:**
- Provides correct and complete access to all parts of an email.
- Properly decodes headers and body content, handling various character sets.
- Manages multipart messages gracefully.

### Steps:

1.  **Locate the mail directories** within the active profile folder (e.g., `ImapMail` or `Mail`).
2.  **Identify the target mailbox file** (e.g., `INBOX`).
3.  **Use the following Python script** to parse the mbox file and extract a message.

### Example Python Script:

Save this script as `read_email.py`:

```python
#!/usr/bin/env python3

import mailbox
import email
from email import policy
from email.header import decode_header

# CONFIG
MBOX_PATH = "/home/zezen/.thunderbird/yxnyzh8h.default-release/ImapMail/imap.gmx.com/INBOX"   # adjust as needed, but is correct on this OS
MSG_INDEX = 0                  # 0 = first message

def decode_mime_words(s):
    if s is None:
        return ""
    decoded = decode_header(s)
    return ''.join(
        fragment.decode(encoding or 'utf-8') if isinstance(fragment, bytes) else fragment
        for fragment, encoding in decoded
    )

def extract_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition"))
            if ctype == "text/plain" and "attachment" not in disp:
                return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="replace")
    else:
        return msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="replace")
    return ""

# Open the mbox
mbox = mailbox.mbox(MBOX_PATH, factory=lambda f: email.message_from_binary_file(f, policy=policy.default))

# Get message by index
msg = mbox[MSG_INDEX]

# Headers
subject = decode_mime_words(msg['Subject'])
sender = decode_mime_words(msg['From'])
date = msg['Date']

print(f"From: {sender}")
print(f"Date: {date}")
print(f"Subject: {subject}\n")

# Body
body = extract_body(msg)
print("Body:\n")
print(body)
```

4.  **Execute the script** from your terminal:
    ```bash
    python3 read_email.py
    ```
    
    
 The script is here too: /home/zezen/Documents/Synchronized_with_Online/Code_snippets/Ubuntu/Scripts_python/read_email.py    
