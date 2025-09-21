from __future__ import annotations

import json
import logging
import os
from collections.abc import Sequence
from html import escape as html_escape
from pathlib import Path
from time import perf_counter
from typing import Any

import markdown


PathLike = str | os.PathLike[str]
Content = str | Sequence[Any] | dict[str, Any] | None

logger = logging.getLogger(__name__)
LOG_LARGE_CONTENT_THRESHOLD = 10_000
MARKDOWN_RENDER_WARN_THRESHOLD = 2.0
MARKDOWN_LARGE_CONTENT_THRESHOLD = 20_000


def render_markdown(content: str, context: str) -> str:
    """Render markdown with timing instrumentation."""
    if len(content) >= MARKDOWN_LARGE_CONTENT_THRESHOLD:
        logger.warning(
            "Skipping markdown render for large content (%s, len=%d)",
            context,
            len(content),
        )
        return f"<pre>{html_escape(content)}</pre>"

    start = perf_counter()
    rendered = markdown.markdown(content, extensions=['nl2br'])
    duration = perf_counter() - start
    if duration > MARKDOWN_RENDER_WARN_THRESHOLD:
        logger.warning(
            "Slow markdown render (%s, duration=%.2fs, len=%d)",
            context,
            duration,
            len(content),
        )
    else:
        logger.info(
            "Rendered markdown (%s, duration=%.2fs, len=%d)",
            context,
            duration,
            len(content),
        )
    return rendered


def normalize_content(content: Content) -> str:
    """Convert message content into a displayable string."""
    if isinstance(content, str):
        return content

    if isinstance(content, Sequence):
        parts: list[str] = []
        for item in content:
            match item:
                case {"text": str() as text}:
                    parts.append(text)
                case str() as text:
                    parts.append(text)
                case _:
                    parts.append(json.dumps(item, ensure_ascii=False))
        return "\n".join(parts)

    if isinstance(content, dict):
        return json.dumps(content, ensure_ascii=False)

    if content is None:
        return ""

    return str(content)

def generate_html_for_project(project_dir: PathLike, *, export_root: Path | None = None) -> list[str]:
    """Generate HTML exports for every chat artifact within *project_dir*."""
    project_path = Path(project_dir)

    files_to_process: list[Path] = []
    seen_paths: set[Path] = set()

    def add_candidate(candidate: Path) -> None:
        if candidate.exists() and candidate not in seen_paths:
            seen_paths.add(candidate)
            files_to_process.append(candidate)

    add_candidate(project_path / 'logs.json')

    for checkpoint_file in sorted(project_path.glob('checkpoint-*.json')):
        add_candidate(checkpoint_file)

    chats_dir = project_path / 'chats'
    if chats_dir.is_dir():
        for session_file in sorted(chats_dir.glob('session-*.json')):
            add_candidate(session_file)

    if not files_to_process:
        logger.debug("No files to process in project %s", project_path)
        return []

    project_name = project_path.name or project_path.as_posix()
    print(f"  Processing {len(files_to_process)} files in {project_name}...")
    logger.info("Processing %d files in project %s", len(files_to_process), project_name)

    generated_html_paths: list[str] = []
    for file_path in files_to_process:
        logger.info("Rendering %s", file_path)
        read_start = perf_counter()
        try:
            with open(file_path, 'r', encoding='utf-8') as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"    - Could not read or parse {file_path.name}: {exc}")
            logger.exception("Failed to load %s", file_path)
            continue

        load_duration = perf_counter() - read_start
        logger.debug("Loaded %s in %.2fs", file_path, load_duration)

        output_filename = file_path.with_suffix('.html')
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

        html_content += "<nav><h3>Project Chat Navigation</h3>"
        for candidate in files_to_process:
            nav_filename = candidate.with_suffix('.html').name
            current_filename = output_filename.name
            if current_filename != nav_filename:
                html_content += f'<a href="./{nav_filename}">{nav_filename}</a><br>'
        html_content += "</nav>"

        if 'checkpoint' in file_path.name:
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
        elif 'logs' in file_path.name:
            html_content += "<h1>Chat History Log File</h1>"
            html_content += """
            <p>
                This file is the Gemini CLI's long-term memory. It's a persistent, cross-session log of all user messages.
                The primary purpose of this file is to provide the AI with historical context about our interactions, allowing it to 'remember' previous conversations and requests even after a session is closed and reopened.
                It is a core component for maintaining continuity.
            </p>
            """
            html_content += generate_html_logs(data)
        elif 'session' in file_path.name:
            html_content += "<h1>Session Log File</h1>"
            html_content += """
            <p>
                This file captures a specific interaction session with the Gemini CLI. It contains a detailed record of messages, including user input, model responses, and internal thoughts, providing a complete chronological view of a single session.
            </p>
            """
            html_content += generate_html_session(data)

        html_content += "</body></html>"

        write_start = perf_counter()
        try:
            with open(output_filename, 'w', encoding='utf-8') as handle:
                handle.write(html_content)
            write_duration = perf_counter() - write_start
            logger.info(
                "Wrote %s (read %.2fs, write %.2fs)",
                output_filename,
                load_duration,
                write_duration,
            )
            generated_html_paths.append(str(output_filename))
        except PermissionError as exc:
            logger.warning(
                "Permission denied writing %s: %s", output_filename, exc
            )
            if export_root is None:
                fallback_root = Path.cwd() / 'exports'
            else:
                fallback_root = Path(export_root)
            fallback_root.mkdir(parents=True, exist_ok=True)
            fallback_path = fallback_root / project_name
            fallback_path.mkdir(parents=True, exist_ok=True)
            fallback_file = fallback_path / output_filename.name
            logger.info("Writing fallback export to %s", fallback_file)
            with open(fallback_file, 'w', encoding='utf-8') as handle:
                handle.write(html_content)
            generated_html_paths.append(str(fallback_file))

    return generated_html_paths

def generate_html_checkpoint(data: list[dict[str, Any]]) -> str:
    """Generates HTML content for 'checkpoint' format data."""
    html = ""
    for entry_index, entry in enumerate(data, start=1):
        role = entry.get('role', 'unknown')
        parts = entry.get('parts', [])
        css_class = "user" if role == "user" else "model"
        html += f'<div class="turn {css_class}">'
        html += f'<h3>{role.capitalize()}</h3>'

        for part_index, part in enumerate(parts, start=1):
            if 'text' in part:
                processed_text = normalize_content(part['text']).replace('\n*   ', '\n\n*   ')
                context = (
                    f"checkpoint role={role} entry={entry_index} part={part_index}"
                )
                logger.info(
                    "Rendering checkpoint text (%s, len=%d)",
                    context,
                    len(processed_text),
                )
                html += render_markdown(processed_text, context)
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


def generate_html_logs(data: list[dict[str, Any]]) -> str:
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


def generate_html_session(data: dict[str, Any]) -> str:
    """Generates HTML content for 'session' format data."""
    html = ""
    messages = data.get('messages', [])
    total_messages = len(messages)
    for index, message in enumerate(messages, start=1):
        msg_type = message.get('type', 'unknown')
        content = message.get('content', '')
        timestamp = message.get('timestamp', '')

        css_class = "user" if msg_type == "user" else "model"
        html += f'<div class="turn {css_class}">'
        html += f'<h3>{msg_type.capitalize()} ({timestamp})</h3>'

        processed_content = normalize_content(content).replace('\n*   ', '\n\n*   ')
        if len(processed_content) > LOG_LARGE_CONTENT_THRESHOLD:
            logger.info(
                "Large message detected (id=%s, len=%d)",
                message.get('id', 'unknown'),
                len(processed_content),
            )
        message_context = f"session message {message.get('id', 'unknown')}"
        logger.info(
            "Rendering %s (%d/%d, len=%d)",
            message_context,
            index,
            total_messages,
            len(processed_content),
        )
        html += render_markdown(processed_content, message_context)

        thoughts = message.get('thoughts', [])
        if thoughts:
            html += '<div class="thought"><h4>Thoughts</h4>'
            for thought in thoughts:
                html += f"<b>{thought.get('subject', 'N/A')}</b>: {markdown.markdown(thought.get('description', 'N/A').replace('\\n\\n', ''))}"
            html += '</div>'
        html += '</div>'
    return html

def main() -> None:
    """
    Main function to find and process all Gemini CLI project logs.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logger.info("Starting Gemini CLI chat export")

    print("=====================================================")
    print(" Gemini CLI Chat Log HTML Exporter")
    print("=====================================================")
    print("This script will scan for Gemini CLI projects and convert their")
    print("JSON chat logs and checkpoints into readable HTML files.")
    print("-----------------------------------------------------\n")

    gemini_tmp_path = Path.home() / '.gemini' / 'tmp'
    if not gemini_tmp_path.is_dir():
        print(f"Error: Gemini temp directory not found at '{gemini_tmp_path}'")
        logger.error("Gemini temp directory not found: %s", gemini_tmp_path)
        return

    logger.info("Scanning for project directories in %s", gemini_tmp_path)

    project_dirs = [d for d in gemini_tmp_path.iterdir() if d.is_dir()]
    
    if not project_dirs:
        print("No project directories found to process.")
        logger.warning("No project directories found in %s", gemini_tmp_path)
        return

    print(f"Found {len(project_dirs)} potential project directories.\n")
    logger.info("Found %d project directories", len(project_dirs))

    total_folders_processed = 0
    total_files_generated = 0
    all_generated_files = []

    for project_path in project_dirs:
        project_hash = project_path.name
        print(f"Scanning project: {project_hash}")
        logger.info("Scanning project %s", project_hash)
        generated_files = generate_html_for_project(project_path)
        if generated_files:
            total_folders_processed += 1
            total_files_generated += len(generated_files)
            all_generated_files.extend(generated_files)
        else:
            logger.info("No exportable files found in %s", project_hash)

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
    logger.info(
        "Export complete (projects=%d, files=%d)",
        total_folders_processed,
        total_files_generated,
    )


if __name__ == "__main__":
    main()
