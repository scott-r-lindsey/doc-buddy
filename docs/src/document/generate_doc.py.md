[<< Table of Contents](../../index.md)

# AI Generated documentation for `doc-buddy/src/document/generate_doc.py`
---
# `generate_doc.py`

This module contains the logic to document a single file within the `doc-buddy` project.  It uses a provider to generate documentation and then appends the original file contents within a code block.

## Functions

### `spinner()`

Displays an animated spinner in the console while the documentation generation process is running.  It uses a global variable `done` to control the spinner loop.

### `generate_doc(file_path: Path, provider)`

This is the main function of the module. It takes a `Path` object representing the file to be documented and a `provider` object (which is assumed to have a `document_file` method).  The function performs the following steps:

1. **Initialization:** Initializes global variables `done` and `current_file` for the spinner.  Determines the relative path of the file within the project.

2. **Spinner Start:** Starts the `spinner()` function in a separate thread.

3. **File Reading:** Reads the contents of the file to be documented.

4. **Documentation Generation:**
    - Creates a preface including a link back to the table of contents and a title.
    - Calls the `provider.document_file()` method to generate the core documentation content.  This provider is external to this module and is responsible for the actual documentation logic.
    - If documentation is generated successfully:
        - Generates a footer using `generate_footer()` from the `generate_footer` module.
        - Appends the original file contents as a code block using `generate_code_block()`.
        - Appends the generated footer.

5. **Output File Writing:**
    - Constructs the output file path based on the configuration settings.
    - Creates the necessary output directories.
    - Writes the generated documentation to the output file.

6. **Error Handling:** Includes a `try...except` block to catch and print any exceptions that occur during the process.

7. **Spinner Stop and Timing:**  Ensures the spinner is stopped and joins the spinner thread.  Calculates and prints the elapsed time for documenting the file.


### `generate_preface(file_path: Path)`

Generates a preface for the documentation file. This includes a link back to the table of contents (calculated relative to the file's path) and an H1 title with the project name and file path. It also adds a horizontal rule (`---`).

### `generate_code_block(code: str, file_name)`

Generates a Markdown code block containing the given `code`. It attempts to guess the appropriate language for syntax highlighting based on the `file_name` using the `guess_language_for_markdown()` function.

### `guess_language_for_markdown(filename)`

Guesses the programming language based on the file extension.  It returns a string representing the language to be used in a Markdown code block. If the extension is not recognized, it returns an empty string which defaults to no syntax highlighting in Markdown.

## Global Variables

- `done`: A boolean flag used to control the spinner.
- `current_file`: Stores the path of the file currently being documented, used for display in the spinner.


## Dependencies

- `os`, `sys`, `threading`, `time`: Standard Python libraries.
- `pathlib`: For file path manipulation.
- `config`: A custom module presumably containing configuration settings.
- `generate_footer`: A custom module containing the `generate_footer` function.


## Key Logic

The core logic revolves around using an external `provider` to generate the documentation content.  This module handles file I/O, preface and footer generation, code block formatting, and displaying a progress spinner.  The `guess_language_for_markdown` function provides basic language detection for syntax highlighting. The relative path calculations ensure correct link generation for the table of contents regardless of the file's location within the project.

# Full listing of src/document/generate_doc.py
```{'python'}
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
    return {extension_mapping.get(extension, '')}

```
<br>
<br>


---
### Automatically generated Documentation for `doc-buddy/src/document/generate_doc.py`
This documentation is generated automatically from the source code. Do not edit this file directly.
Generated by **Doc-Buddy** on **November 09, 2024 18:52:57** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: e4f5dcb09e20896907179c4446f269d9f1c93dd8*
