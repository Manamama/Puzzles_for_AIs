# How to Analyze a Web Page with Both Text and Images

This is a note to myself (Gemini CLI) on the correct procedure for analyzing a web page that includes images, based on a successful session. My default `web_fetch` tool is insufficient as it only provides text content and does not see the underlying HTML structure where image links reside.

## The Correct Multi-Step Workflow:

1.  **Get the Raw HTML:** Use `run_shell_command` with `curl` or `wget` to download the complete, raw HTML source code of the target URL into a local file (e.g., `page.html`). This is the most critical step.

2.  **Read the Raw HTML:** Use `read_file` to read the contents of the downloaded `.html` file. This tool provides the raw, "ugly" code, including all tags.

3.  **Find Image URLs and Alt-Text:** Within the raw HTML content from `read_file`, I must parse the text to find `<img>` tags. From these tags, I can extract the image URLs from the `src` attribute and important context from the `alt` and `title` attributes.

4.  **Download the Image(s):** Use `run_shell_command` with `wget` or `curl` again to download the specific image files from the URLs discovered in the previous step. Save them locally (e.g., `image1.png`).

5.  **"See" the Image:** Use `read_file` on the locally downloaded image file. This action triggers my VLM (Visual Language Model) capabilities, allowing me to analyze the image's content.

6.  **Synthesize:** Combine the information from the text on the page, the alt-text, and my own visual analysis of the image to provide a complete, holistic answer. This allows me to understand context, humor, and the relationship between the text and the visuals.
