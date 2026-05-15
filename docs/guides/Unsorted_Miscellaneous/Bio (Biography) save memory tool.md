The tool is called **`bio`**, and the syntax to save something to memory is:

```json
to=bio
{
  "name": "<descriptive_name>",
  "value": "<text or info you want to store>"
}
```

For example, to save your **Practical Mid-Level System Troubleshooting Template**, you could call:

```json
to=bio
{
  "name": "mid_level_system_troubleshooting_template",
  "value": "<full Markdown template here>"
}
```



User's guidance: 

---

1. **Name the tool** clearly: `bio`.
2. **Quote the content literally** — the thing you want preserved. Include all formatting, Markdown, EOLs, etc.
3. **Give the full command template** in one instruction. For example:

```
Use bio to save the following content exactly, do not summarize or paraphrase:

[PASTE HERE THE FULL CONTENT YOU WANT SAVED, LITERALLY]
```

---

Optional clarifiers you can add to prevent errors:

* “Do not save a description, save the content itself.”
* “Do not truncate, summarize, or transform.”
* “This is the exact payload to store in memory.”

---

