# Gemini CLI Logs Prettifier

## Problem
Gemini CLI https://github.com/google-gemini/gemini-cli stores various chat logs (checkpoint, session, and general logs) as raw JSON files under `~/.gemini/tmp`. These are not easy for users to inspect or navigate, especially when debugging or restoring sessions.

## What this program does

This tool renders Gemini CLI's JSON chat logs human-readable (prettifies them) and browsable as interlinked HTML files. It improves transparency and usability for users who want to debug, audit, or restore chat sessions.

This script automates the conversion process. It recursively scans the `~/.gemini/tmp` directory and its subdirectories, finds all `.json`  files, and generates a set of interlinked HTML files for easy browsing. 

## Features

- **Recursive Discovery:** The script automatically finds the Gemini CLI's temporary directory (`~/.gemini/tmp`) and recursively scans all subdirectories for `.json` files.
- **HTML Conversion:** It converts the raw JSON into clean, styled HTML for easy reading in a web browser. 
- **Clickable File Links:** The script outputs `file://` URIs for all generated HTML files, so you can click them to open them directly in your browser.
- **Universality:** Works in Ubuntu and Termux (Android) so far, probably universal then: the filepaths codes need checking maybe in Windows and such. 

## How to use
1.  The Python script that performs this conversion is `pretty_print_chat.py`. Just download this single .py file in this folder, so [right click here]([url](https://github.com/Manamama/Puzzles_for_AIs/raw/refs/heads/main/code/Gemini%20CLI%20logs%20prettifier/pretty_print_chat.py)): https://github.com/Manamama/Puzzles_for_AIs/raw/refs/heads/main/code/Gemini%20CLI%20logs%20prettifier/pretty_print_chat.py etc. or just use `wget` with that URL. 

2.  Run the script from your terminal:
    ```bash
    python3 pretty_print_chat.py
    ```
3.  The script will print the progress and a list of clickable links to the generated HTML files.
4.  If some errors with paths, do ask Gemini itself to adapt it for you. 



## Sample results: 

```
=====================================================
 Gemini CLI Chat Log HTML Exporter
=====================================================
This script will recursively scan for Gemini CLI chat logs (.json files)
and convert them into readable HTML files.
-----------------------------------------------------

Found 25 potential session directories.

Scanning session: f82ecedde95bc2921fb4c856690e6a6d6d1b5624507ddf04e9992923b3a22df6
  Processing 1 files in f82ecedde95bc2921fb4c856690e6a6d6d1b5624507ddf04e9992923b3a22df6...
... 

-----------------------------------------------------
 Export Complete!
-----------------------------------------------------
  - Sessions Processed: 25
  - HTML Files Generated: 32

Generated files can be found in their respective session folders.
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




#ver. 0.3.5

#Updates

- **Improved Markdown Rendering:** Now correctly renders Markdown formatting, including lists and preserving end-of-lines (EOLs).
- Explanation that it works in Termux too
- Info that one .py file only here
