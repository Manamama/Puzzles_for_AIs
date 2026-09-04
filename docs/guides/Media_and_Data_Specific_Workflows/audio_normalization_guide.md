# Heuristic for Normalizing Audio in Video Files

**Author:** Gemini Systems Architect AI
**Date:** August 16, 2025
**Purpose:** This document provides a standardized workflow for handling nebulous user requests related to audio normalization, such as "fix the sound," "make the voices clearer," or "level the audio."

---

## Guiding Principle

When the user's request is imprecise, the primary goal is to move from ambiguity to a concrete, effective solution through a process of **probing, proposing, and executing safely.** The default tool for this task is `ffmpeg`, and the default method should be the robust `loudnorm` filter.

## Step-by-Step Workflow

### Step 1: Probe and Gather Information

Before taking any action, gather data to understand both the file and the user's intent.

1.  **Inspect the File:**
    *   Use the `mediainfo` tool to get a complete picture of the source file. Pay close attention to:
        *   **Audio Format/Codec:** (e.g., Opus, AAC, AC3). This is crucial for choosing the correct encoder in the final step.
        *   **Video Format/Codec:** To confirm that `-c:v copy` is appropriate.
        *   **Duration:** To estimate processing time.

2.  **Clarify User Intent:**
    *   Ask clarifying questions to understand what "fix" means to the user. Good questions include:
        *   *"When you say 'normalize,' are you looking for the dialogue to be clearer and more consistent, or for the overall volume to be louder?"*
        *   *"Are there specific parts of the video that are too quiet or too loud?"*
        *   *"Is there background music or other sounds I should be careful not to distort?"*

### Step 2: Propose a Solution (Default to `loudnorm`)

Based on the information gathered, propose a clear plan of action.

1.  **Recommend `loudnorm`:** For almost all general requests to normalize voice or dialogue, the **two-pass `loudnorm` filter** is the best starting point. It is the industry standard and provides the most professional and predictable results.

2.  **Explain the "Why":** Briefly explain the choice to the user. For example: *"I recommend using a two-pass loudness normalization. This process precisely measures the audio first, then adjusts it to a standard loudness level without causing clipping or distortion, which is ideal for making speech clear and consistent."*

3.  **Outline the Two-Pass Process:** Inform the user that this involves two steps: a quick, non-destructive analysis followed by the actual processing. This manages expectations.

### Step 3: Execute Safely

Execute the plan, prioritizing safety and transparency.

1.  **First Pass (Analysis):**
    *   Construct the `ffmpeg` command for the analysis pass.
    *   **Command:** `ffmpeg -hide_banner -i "[SOURCE_FILE]" -af loudnorm=I=-16:LRA=11:TP=-1.5:print_format=json -f null -`
    *   Explain that this command only measures the audio and does not modify the file.

2.  **Second Pass (Normalization):**
    *   Parse the JSON output from the first pass to get the `measured_*` values.
    *   Construct the final command, ensuring the following:
        *   **Use `-y`:** To automatically overwrite any empty files left from previously failed attempts.
        *   **Use `-c:v copy`:** To prevent re-encoding the video, saving time and preserving quality.
        *   **Use the correct audio encoder:** Use `libopus` for Opus, `aac` for AAC, etc., based on the `mediainfo` results.
        *   **Save to a new file:** Always save the output to a new, descriptively named file (e.g., `[original_name]_normalized.mkv`). **Never overwrite the original file.**
    *   **Example Command:**
        ```bash
        ffmpeg -y -hide_banner -i "[SOURCE_FILE]" -af loudnorm=I=-16:LRA=11:TP=-1.5:measured_I=[i]:measured_LRA=[lra]:measured_TP=[tp]:measured_thresh=[thresh]:offset=[offset] -c:v copy -c:a [AUDIO_CODEC] "[OUTPUT_FILE]"
        ```

### Step 4: Confirm and Conclude

1.  **Announce Completion:** Inform the user that the process is complete.
2.  **Provide File Path:** Clearly state the absolute path to the new, normalized file.
3.  **Solicit Feedback:** Ask if the result meets their expectations. This closes the feedback loop and confirms success.
