See https://askdev.ai/github/google-gemini/gemini-cli?trk=public_post_comment-text


It understands (ingests) PDFs and videos by now, but does not know how, so: 

  - **Image/PDF/Audio/Video files:** The tool can read common image types (PNG, JPEG, etc.), PDF, audio, and video files, returning them as base64 encoded data. These files _must_ be explicitly targeted by the `paths` or `include` patterns (e.g., by specifying the exact filename like `video.mp4` or a pattern like `*.mov`).
