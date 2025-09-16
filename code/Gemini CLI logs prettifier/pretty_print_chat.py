#!/data/data/com.termux/files/usr/bin/python
import os
import json
import glob
from html import escape as html_escape
from urllib.parse import quote
from pathlib import Path

try:
    import markdown
    markdown_available = True
except ImportError:
    markdown_available = False

def generate_html_for_directory(directory_path):
    """
    Finds all chat-related JSON files in a directory and its subdirectories,
    and generates interlinked HTML files for them.
    """
    # Find all .json files recursively in the given directory
    files_to_process = glob.glob(os.path.join(directory_path, '**', '*.json'), recursive=True)

    if not files_to_process:
        return [], 0

    print(f"  Processing {len(files_to_process)} files in {os.path.basename(directory_path)}...")

    generated_html_paths = []
    for file_path in files_to_process:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"    - Could not read or parse {os.path.basename(file_path)}: {e}")
            continue

        output_filename = os.path.splitext(file_path)[0] + '.html'
        html_content = "<html><head><title>Chat Log</title>"
        html_content += '''
        <style>
            body { font-family: sans-serif; margin: 2em; }
            .turn { border: 1px solid #ccc; padding: 1em; margin-bottom: 1em; border-radius: 5px; }
            .user { background-color: #e0f7fa; }
            .model { background-color: #fce4ec; }
            .tool-call { background-color: #dcedc8; border: 1px solid #a5d6a7; padding: 1em; margin-top: 1em; }
            .tool-response { background-color: #c5cae9; border: 1px solid #9fa8da; padding: 1em; margin-top: 1em; }
            .thought { background-color: #fff9c4; border: 1px solid #fff176; padding: 1em; margin-top: 1em; }
            .log-entry { border-bottom: 1px solid #eee; padding: 0.5em 0; }
            nav { margin-bottom: 2em; border-bottom: 2px solid black; padding-bottom: 1em;}
        </style>
        '''
        html_content += "</head><body>"

        # Add navigation
        html_content += "<nav><h3>Session Chat Navigation</h3>"
        for f in files_to_process:
            # Create a relative path for the link from the current directory
            nav_filename = os.path.relpath(os.path.splitext(f)[0] + '.html', os.path.dirname(output_filename))
            display_name = os.path.relpath(os.path.splitext(f)[0] + '.html', directory_path)
            current_filename = os.path.basename(output_filename)
            
            if os.path.basename(output_filename) != os.path.basename(f).replace('.json', '.html'):
                 html_content += f'<a href="{nav_filename}">{display_name}</a><br>'

        html_content += "</nav>"

        # Add file explanation
        file_basename = os.path.basename(file_path)
        if 'checkpoint' in file_basename:
            html_content += "<h1>Checkpoint File</h1>"
            html_content += '''
            <p>
                This file is a complete, high-fidelity 'snapshot' of a specific session's state, created automatically by the Gemini CLI as a safety feature.
                Checkpoints are generated just before a tool is about to modify the file system (e.g., with <code>write_file</code>).
                They contain the full conversational context, including user messages, model responses, internal thoughts, and the exact tool calls made.
                This allows you to use the <code>/restore</code> command to revert the project files and conversation state to the moment right before the change was made.
            </p>
            '''
            html_content += generate_html_from_data(data)
        elif 'logs' in file_basename:
            html_content += "<h1>Chat History Log File</h1>"
            html_content += '''
            <p>
                This file is the Gemini CLI's long-term memory. It's a persistent, cross-session log of all user messages.
                The primary purpose of this file is to provide the AI with historical context about our interactions, allowing it to 'remember' previous conversations and requests even after a session is closed and reopened.
                It is a core component for maintaining continuity.
            </p>
            '''
            html_content += generate_html_from_data(data)
        elif 'session' in file_basename:
            html_content += "<h1>Session File</h1>"
            html_content += '''
            <p>
                This file is an automatically saved chat session. It contains the full conversation history for a specific session.
            </p>
            '''
            html_content += generate_html_from_data(data)
        else:
            html_content += "<h1>JSON Log File</h1>"
            html_content += "<p>This is a generic JSON log file. The structure of this file is not recognized as a standard Gemini CLI log file, but the content is displayed below.</p>"
            html_content += generate_html_from_data(data)

        html_content += "</body></html>"

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        generated_html_paths.append(output_filename)
    
    return generated_html_paths, len(files_to_process)

def generate_html_from_data(data):
    """
    Generates HTML content from a list of chat entries.
    This function can handle both 'checkpoint' and 'logs' formats.
    """
    html = ""
    if not isinstance(data, list):
        # Handle cases where the top-level JSON is a single object
        data = [data]

    for entry in data:
        # Heuristic to guess the format
        if 'role' in entry and 'parts' in entry:
            # Looks like a checkpoint/session entry
            role = entry.get('role', 'unknown')
            parts = entry.get('parts', [])
            css_class = "user" if role == "user" else "model"
            html += f'<div class="turn {css_class}>'
            html += f'<h3>{role.capitalize()}</h3>'

            for part in parts:
                if 'text' in part:
                    processed_text = part['text'].replace('\n*   ', '\n\n*   ')
                    if markdown_available:
                        html += markdown.markdown(processed_text, extensions=['nl2br'])
                    else:
                        html += f'<pre>{processed_text}</pre>'
                elif 'functionCall' in part:
                    fc = part['functionCall']
                    html += '<div class="tool-call">'
                    html += '<h4>Function Call</h4>'
                    html += f"<b>Name:</b> {fc['name']}<br>"
                    try:
                        html += f"<pre>{json.dumps(fc.get('args', {}), indent=2)}</pre>"
                    except TypeError:
                        html += f"<pre>{str(fc.get('args', {}))}</pre>"
                    html += '</div>'
                elif 'functionResponse' in part:
                    fr = part['functionResponse']
                    html += '<div class="tool-response">'
                    html += '<h4>Function Response</h4>'
                    html += f"<b>ID:</b> {fr.get('id', 'N/A')}<br>"
                    html += f"<b>Name:</b> {fr.get('name', 'N/A')}<br>"
                    html += f"<pre>{json.dumps(fr.get('response', {}), indent=2)}</pre>"
                    html += '</div>'
                elif 'thoughtSignature' in part:
                    html += '<div class="thought"><h4>Thinking...</h4></div>'
            html += '</div>'
        elif 'type' in entry and 'message' in entry:
            # Looks like a logs.json entry
            msg_type = entry.get('type', 'unknown')
            message = entry.get('message', '')
            timestamp = entry.get('timestamp', '')
            css_class = "user" if msg_type == "user" else "model"

            html += f'<div class="log-entry {css_class}">'
            html += f"<b>Timestamp:</b> {timestamp}<br>"
            html += f"<b>Type:</b> {msg_type}<br>"
            html += f"<b>Message:</b><pre>{message}</pre>"
            html += '</div>'
        else:
            # Fallback for unknown JSON structure
            html += f"<pre>{json.dumps(entry, indent=2)}</pre>"
            
    return html

def main():
    """
    Main function to find and process all Gemini CLI session logs.
    """
    print("=====================================================")
    print(" Gemini CLI Chat Log HTML Exporter")
    print("=====================================================")
    print("This script recursively scans for the Gemini CLI's session logs (.json files) and converts them into readable HTML files.")
    print("-----------------------------------------------------")

    gemini_tmp_dir = os.path.expanduser('~/.gemini/tmp')
    if not os.path.isdir(gemini_tmp_dir):
        print(f"Error: Gemini temp directory not found at '{gemini_tmp_dir}'")
        return

    # Get the top-level session directories
    try:
        session_dirs = [os.path.join(gemini_tmp_dir, d) for d in os.listdir(gemini_tmp_dir) if os.path.isdir(os.path.join(gemini_tmp_dir, d))]
    except OSError as e:
        print(f"Error reading directories from {gemini_tmp_dir}: {e}")
        return

    if not session_dirs:
        print("No directories found to process in ~/.gemini/tmp.")
        return

    total_log_files_found = 0
    total_dirs_with_logs = 0
    all_generated_files = []

    for directory in session_dirs:
        generated_files, files_found_in_dir = generate_html_for_directory(directory)
        if files_found_in_dir > 0:
            total_dirs_with_logs += 1
            total_log_files_found += files_found_in_dir
            all_generated_files.extend(generated_files)

    print(f"\nFound a total of {total_log_files_found} log files within {total_dirs_with_logs} directories containing session logs.\n")

    print("-----------------------------------------------------")
    print(" Export Complete!")
    print("-----------------------------------------------------")
    print(f"Processed {total_dirs_with_logs} directories of session logs, generating {total_log_files_found} HTML files.")
    
    if all_generated_files:
        print("\nThe generated files can be found in their respective directories.")
        print("You can open them in your browser. Here are the links:")

        for html_file in all_generated_files:
            file_uri = Path(html_file).as_uri()
            print(f"  - {file_uri}")
            
    print("=====================================================")


if __name__ == "__main__":
    main()
