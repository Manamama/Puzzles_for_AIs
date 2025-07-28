# Gemini CLI Logs Prettifier

## Problem
Gemini CLI stores chat sessions and checkpoints as raw JSON under `~/.gemini/tmp`. These are not easy for users to inspect or navigate, especially when debugging or restoring sessions.

## What this program does

This tool renders the logs human readable (prettifies them) and browsable as interlinked HTML, with thoughtful explanations and clickable links, improving transparency and usability for users debugging, auditing, or restoring sessions. 
This script scans for Gemini CLI projects and converts their JSON chat logs and checkpoints into readable, interlinked HTML files. 

This script automates the process of converting that data into a user-friendly format. It iterates through all the project folders in your `~/.gemini/tmp` directory, finds all `logs.json` and `checkpoint-*.json` files, and generates a set of interlinked HTML files.

## Features

- **Automatic Discovery:** The script automatically finds the Gemini CLI's temporary directory and scans all the project folders within it.
- **Intelligent Formatting:** It distinguishes between `logs.json` (chat history) and `checkpoint-*.json` (session snapshots) and provides a clear explanation of what each file type is for.
- **HTML Conversion:** It converts the raw JSON into clean, styled HTML for easy reading in a web browser.
- **Interlinked Pages:** Each generated HTML file contains navigation links to the other reports from the same project, making it easy to browse a complete session history.
- **Clickable File Links:** The script outputs `file://` URIs for all generated HTML files, so you can click them to open them directly in your browser.
- **Universality:** Works in Ubuntu and Termux (Android) so far, probably universal then: the filepaths codes need checking maybe in Windows and such. 

## How to use
0.  Just download this single .py file in this folder, so [right click here]([url](https://github.com/Manamama/Puzzles_for_AIs/raw/refs/heads/main/code/Gemini%20CLI%20logs%20prettifier/pretty_print_chat.py)): https://github.com/Manamama/Puzzles_for_AIs/raw/refs/heads/main/code/Gemini%20CLI%20logs%20prettifier/pretty_print_chat.py etc. or just use `wget` with that URL. 
1.  Make sure you have Python 3 installed.
2.  Run the script from your terminal:
    ```bash
    python3 pretty_print_chat.py
    ```
3.  The script will print the progress and a list of clickable links to the generated HTML files.
4.  If some errors with paths, do ask Gemini itself to adapt it for you. 

## The Script

The Python script that performs this conversion is `pretty_print_chat.py`.


## Sample results: 

```
=====================================================
 Gemini CLI Chat Log HTML Exporter
=====================================================
This script will scan for Gemini CLI projects and convert their
JSON chat logs and checkpoints into readable HTML files.
-----------------------------------------------------

Found 25 potential project directories.

Scanning project: f82ecedde95bc2921fb4c856690e6a6d6d1b5624507ddf04e9992923b3a22df6
  Processing 1 files in f82ecedde95bc2921fb4c856690e6a6d6d1b5624507ddf04e9992923b3a22df6...
... 

-----------------------------------------------------
 Export Complete!
-----------------------------------------------------
  - Projects Processed: 25
  - HTML Files Generated: 32

Generated files can be found in their respective project folders.
You can open them in your browser. Here are the links:

...

  - file:///home/user/.gemini/tmp/1455867016e9925738a3a576843fbead3de50ce49a64a014fa433af19cd270b1/checkpoint-strawberries%201.html
  - file:///home/user/.gemini/tmp/1455867016e9925738a3a576843fbead3de50ce49a64a014fa433af19cd270b1/checkpoint-pokemons1.html
=====================================================

```

plus: 

<img width="1881" height="421" alt="image" src="https://github.com/user-attachments/assets/ad6dbdd7-43f7-4f0b-95ac-b42b4114b631" />

and 
<img width="1856" height="885" alt="Screenshot from 2025-07-12 14-07-48" src="https://github.com/user-attachments/assets/ee5f0146-e87e-4987-8215-3c010368e42a" />




#ver. 0.3.2

#Updates

- **Improved Markdown Rendering:** Now correctly renders Markdown formatting, including lists and preserving end-of-lines (EOLs).
- Explanation that it works in Termux too
- Info that one py file only here
