# Gemini CLI Logs Prettifier

This script scans for Gemini CLI projects and converts their JSON chat logs and checkpoints into readable, interlinked HTML files.

## What it does

The Gemini CLI stores chat history and session checkpoints in a series of JSON files located in `~/.gemini/tmp`. While this is great for the tool's own state management, it's not very human-readable.

This script automates the process of converting that data into a user-friendly format. It iterates through all the project folders in your `~/.gemini/tmp` directory, finds all `logs.json` and `checkpoint-*.json` files, and generates a set of interlinked HTML files.

## Features

- **Automatic Discovery:** The script automatically finds the Gemini CLI's temporary directory and scans all the project folders within it.
- **Intelligent Formatting:** It distinguishes between `logs.json` (chat history) and `checkpoint-*.json` (session snapshots) and provides a clear explanation of what each file type is for.
- **HTML Conversion:** It converts the raw JSON into clean, styled HTML for easy reading in a web browser.
- **Interlinked Pages:** Each generated HTML file contains navigation links to the other reports from the same project, making it easy to browse a complete session history.
- **Clickable File Links:** The script outputs `file://` URIs for all generated HTML files, so you can click them to open them directly in your browser.

## How to use

1.  Make sure you have Python 3 installed.
2.  Run the script from your terminal:
    ```bash
    python3 pretty_print_chat.py
    ```
3.  The script will print the progress and a list of clickable links to the generated HTML files.

## The Script

The Python script that performs this conversion is `pretty_print_chat.py`.
