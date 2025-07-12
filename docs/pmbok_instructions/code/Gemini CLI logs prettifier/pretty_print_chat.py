import json
import os
import glob
from pathlib import Path
import markdown

def generate_html_for_project(project_dir):
    """
    Finds all chat-related JSON files in a project directory
    and generates interlinked HTML files for them.
    """
    files_to_process = []
    # Find logs.json
    logs_file = os.path.join(project_dir, 'logs.json')
    if os.path.exists(logs_file):
        files_to_process.append(logs_file)

    # Find all checkpoint files
    checkpoint_files = glob.glob(os.path.join(project_dir, 'checkpoint-*.json'))
    files_to_process.extend(checkpoint_files)

    if not files_to_process:
        return []

    print(f"  Processing {len(files_to_process)} files in {os.path.basename(project_dir)}...")

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
        html_content += """
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
        """
        html_content += "</head><body>"

        # Add navigation
        html_content += "<nav><h3>Project Chat Navigation</h3>"
        for f in files_to_process:
            nav_filename = os.path.basename(os.path.splitext(f)[0] + '.html')
            current_filename = os.path.basename(output_filename)
            if current_filename != nav_filename:
                html_content += f'<a href="./{nav_filename}">{nav_filename}</a><br>'
        html_content += "</nav>"

        # Add file explanation
        if 'checkpoint' in file_path:
            html_content += "<h1>Checkpoint File</h1>"
            html_content += """
            <p>
                This file is a complete, high-fidelity 'snapshot' of a specific session's state, created automatically by the Gemini CLI as a safety feature.
                Checkpoints are generated just before a tool is about to modify the file system (e.g., with <code>write_file</code>).
                They contain the full conversational context, including user messages, model responses, internal thoughts, and the exact tool calls made.
                This allows you to use the <code>/restore</code> command to revert the project files and conversation state to the moment right before the change was made.
            </p>
            """
            html_content += generate_html_checkpoint(data)
        elif 'logs' in file_path:
            html_content += "<h1>Chat History Log File</h1>"
            html_content += """
            <p>
                This file is the Gemini CLI's long-term memory. It's a persistent, cross-session log of all user messages.
                The primary purpose of this file is to provide the AI with historical context about our interactions, allowing it to 'remember' previous conversations and requests even after a session is closed and reopened.
                It is a core component for maintaining continuity.
            </p>
            """
            html_content += generate_html_logs(data)

        html_content += "</body></html>"

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        generated_html_paths.append(output_filename)
    
    return generated_html_paths

def generate_html_checkpoint(data):
    """Generates HTML content for 'checkpoint' format data."""
    html = ""
    for entry in data:
        role = entry.get('role', 'unknown')
        parts = entry.get('parts', [])
        css_class = "user" if role == "user" else "model"
        html += f'<div class="turn {css_class}">'
        html += f'<h3>{role.capitalize()}</h3>'

        for part in parts:
            if 'text' in part:
                processed_text = part['text'].replace('\n*   ', '\n\n*   ')
                html += markdown.markdown(processed_text, extensions=['nl2br'])
            elif 'functionCall' in part:
                fc = part['functionCall']
                html += '<div class="tool-call">'
                html += '<h4>Function Call</h4>'
                html += f"<b>Name:</b> {fc['name']}<br>"
                html += f"<pre>{json.dumps(fc['args'], indent=2)}</pre>"
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
    return html

def generate_html_logs(data):
    """Generates HTML content for 'logs' format data."""
    html = ""
    for entry in data:
        msg_type = entry.get('type', 'unknown')
        message = entry.get('message', '')
        timestamp = entry.get('timestamp', '')
        css_class = "user" if msg_type == "user" else "model"

        html += f'<div class="log-entry {css_class}">'
        html += f"<b>Timestamp:</b> {timestamp}<br>"
        html += f"<b>Type:</b> {msg_type}<br>"
        html += f"<b>Message:</b><pre>{message}</pre>"
        html += '</div>'
    return html

def main():
    """
    Main function to find and process all Gemini CLI project logs.
    """
    print("=====================================================")
    print(" Gemini CLI Chat Log HTML Exporter")
    print("=====================================================")
    print("This script will scan for Gemini CLI projects and convert their")
    print("JSON chat logs and checkpoints into readable HTML files.")
    print("-----------------------------------------------------\n")

    gemini_tmp_dir = os.path.expanduser('~/.gemini/tmp')
    if not os.path.isdir(gemini_tmp_dir):
        print(f"Error: Gemini temp directory not found at '{gemini_tmp_dir}'")
        return

    project_dirs = [d for d in os.listdir(gemini_tmp_dir) if os.path.isdir(os.path.join(gemini_tmp_dir, d))]
    
    if not project_dirs:
        print("No project directories found to process.")
        return

    print(f"Found {len(project_dirs)} potential project directories.\n")

    total_folders_processed = 0
    total_files_generated = 0
    all_generated_files = []

    for project_hash in project_dirs:
        project_path = os.path.join(gemini_tmp_dir, project_hash)
        print(f"Scanning project: {project_hash}")
        generated_files = generate_html_for_project(project_path)
        if generated_files:
            total_folders_processed += 1
            total_files_generated += len(generated_files)
            all_generated_files.extend(generated_files)

    print("\n-----------------------------------------------------")
    print(" Export Complete!")
    print("-----------------------------------------------------")
    print(f"  - Projects Processed: {total_folders_processed}")
    print(f"  - HTML Files Generated: {total_files_generated}")
    print("\nGenerated files can be found in their respective project folders.")
    print("You can open them in your browser. Here are the links:")

    for html_file in all_generated_files:
        # Create a clickable file URI
        file_uri = Path(html_file).as_uri()
        print(f"  - {file_uri}")
    print("=====================================================")


if __name__ == "__main__":
    main()