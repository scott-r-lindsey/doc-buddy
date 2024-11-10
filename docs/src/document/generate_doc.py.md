[<< Table of Contents](../../index.md)

# AI Generated documentation for `doc-buddy/src/document/generate_doc.py`
---
This module contains the logic to document a single file within the `doc-buddy` project.  It uses a provider to generate documentation and appends the original file content as a code block.

**Global Variables:**

* `done`: A boolean flag used to control the spinner.
* `current_file`: Stores the path of the file currently being documented.  Used by the spinner.

**Functions:**

* **`spinner()`**: Displays an animated spinner in the console while the documentation generation process is running.  It uses a global `done` flag to stop the spinner.

* **`generate_doc(file_path: Path, provider)`**: This is the main function of the module. It takes the file path and a documentation provider as input.  It performs the following steps:
    1. Initializes global variables `done` and `current_file`.
    2. Calculates the relative path of the file being documented.
    3. Starts the `spinner()` function in a separate thread.
    4. Reads the contents of the file.
    5. Calls `generate_preface()` to create the introductory section of the documentation.
    6. Calls the provider's `document_file()` method to generate the core documentation.
    7. If documentation is successfully generated:
        * Calls `generate_footer()` to create the footer.
        * Calls `generate_code_block()` to append the original file content as a code block.
        * Creates the output directory if it doesn't exist.
        * Writes the complete documentation to the output file.
    8. Handles potential exceptions during file processing.
    9. Stops the spinner thread and prints the elapsed time.

* **`generate_preface(file_path: Path)`**:  Generates the preface section of the documentation. It includes a link back to the table of contents and a heading indicating the file being documented.

* **`generate_code_block(code: str, file_name)`**:  Generates a code block for the given code content. It attempts to guess the appropriate language for syntax highlighting based on the file extension using `guess_language_for_markdown()`.  Prints the guessed language to the console.

* **`guess_language_for_markdown(filename)`**:  Guesses the programming language based on the file extension.  It uses a dictionary `extension_mapping` to map extensions to language strings used by Markdown code blocks.  If no mapping is found, it returns an empty string, resulting in no syntax highlighting.


**Key Logic and Dependencies:**

* **Configuration:** The module relies on a `config` object (presumably imported from a `config.py` file) for settings such as the documentation suffix, input path, output path, and project name.
* **Documentation Provider:** The `provider` argument to `generate_doc()` is an object that must implement a `document_file()` method.  This method is responsible for generating the actual documentation content.
* **Threading:**  The `spinner()` function runs in a separate thread to provide visual feedback without blocking the main documentation generation process.
* **File I/O:** The module reads the input file and writes the generated documentation to an output file.
* **Path Manipulation:** The `pathlib` library is used for file path operations.
* **Error Handling:**  A `try...except` block is used to catch potential errors during file processing.


This module provides a structured way to document individual files, leveraging a pluggable documentation provider and incorporating the original file content within the generated documentation. The use of a spinner provides a better user experience during potentially long documentation generation processes.

# Full listing of src/document/generate_doc.py
```python
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

```
<br>
<br>


---
### Automatically generated Documentation for `doc-buddy/src/document/generate_doc.py`
This documentation is generated automatically from the source code. Do not edit this file directly.
Generated by **Doc-Buddy** on **November 09, 2024 19:44:26** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: b01f9573f01b626efe9b415f7392e374029af615*
