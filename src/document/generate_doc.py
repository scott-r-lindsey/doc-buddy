"""
This module contains the logic to document a single file.
"""

import os
import sys
import threading
import time
from pathlib import Path
from os.path import basename
from config import config
from .generate_footer import generate_footer


def spinner():
    """
    Function to show a spinner while a task is running.
    """
    spinner_chars = ["|", "/", "-", "\\"]
    idx = 0
    while not done:
        sys.stdout.write(f"\rDocumenting file {current_file} {spinner_chars[idx]}")
        sys.stdout.flush()
        idx = (idx + 1) % len(spinner_chars)
        time.sleep(0.1)


def generate_doc(file_path: Path, provider):
    """
    Document a single file and write the output to a file with suffix.
    """
    suffix = config.documentation_suffix

    global done, current_file
    done = False
    current_file = file_path
    input_path = config.input_path

    # get a path for the file_path without the input_path
    relative_path = file_path.relative_to(config.root_path)

    # Start spinner in a separate thread
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    start_time = time.time()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents = file.read()

            documentation = generate_preface(relative_path)

            # Document the file using the provider
            documentation += provider.document_file(
                file_name=basename(file_path),
                project_path=(relative_path.parent),
                file_contents=file_contents,
            )

            if documentation:
                footer = generate_footer(relative_path)
                documentation += generate_code_block(file_contents, relative_path)
                documentation += footer

                output_file_path = config.output_path / relative_path.parent / (
                    basename(relative_path) + suffix
                )

                # create the directory if it does not exist
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                # Write the documentation to the file
                with open(output_file_path, "w", encoding="utf-8") as doc_file:
                    doc_file.write(documentation)

    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        # Stop the spinner
        done = True
        spinner_thread.join()

        # Clear the spinner line and print elapsed time
        elapsed_time = time.time() - start_time
        sys.stdout.write(
            f"\rDocumenting file {file_path} - {elapsed_time:.2f} seconds\n"
        )

def generate_preface(file_path: Path):
    block = ""
    block += f"[<< Table of Contents](../{'../' * (len(file_path.parts) -2)}index.md)\n\n"
    block += f"# AI Generated documentation for `{config.project_name}/{file_path}`\n"
    block += "---\n"

    return block

def generate_code_block(code: str, file_name):
    """
    Generate a code block with a specific language.
    """
    language = guess_language_for_markdown(file_name)

    block = f"\n# Full listing of {file_name}\n"
    block += f"```{language}\n{code}\n```\n"

    print(f"Language: {language}")

    return block


def guess_language_for_markdown(filename):
    # Extract the file extension
    _, extension = os.path.splitext(filename)
    extension = extension.lower()

    # Define a mapping of extensions to languages for markdown
    extension_mapping = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
        ".cs": "csharp",
        ".rb": "ruby",
        ".php": "php",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "bash",
        ".go": "go",
        ".rs": "rust",
        ".swift": "swift",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".xml": "xml",
        ".sql": "sql",
        ".kt": "kotlin",
        ".m": "matlab",
        ".r": "r",
        ".pl": "perl",
        ".dockerfile": "dockerfile",
        ".ps1": "powershell",
        ".vim": "vim",
        ".lua": "lua",
        ".scala": "scala",
        ".hs": "haskell",
        ".md": "markdown"
    }

    # Return the markdown language string if found, else return plain text
    return extension_mapping.get(extension, '')
