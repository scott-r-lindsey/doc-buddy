[<< Table of Contents](../index.md)

# AI Generated documentation for `doc-buddy/src/main.py`
---
# Doc-buddy

This document explains the `main.py` file, the entry point for the Doc-buddy project.  Doc-buddy aims to automatically generate documentation from source code files.

## Core Logic

The `main` function orchestrates the documentation generation process based on the provided input path (file or directory), dry run setting, and summary flag.

## Functions

### `main(input_path: Path, dry_run: bool, summary: bool) -> None`

This function is the main entry point for the Doc-buddy application. It takes the input path, dry run flag, and summary flag as arguments.

1. **Provider Initialization:** It initializes a "provider", which is likely an abstraction for interacting with a documentation generation service or library.  This is done through the `initialize_provider()` function from the `util` module.

2. **Project Path Determination:** It determines the project's root directory using the environment variable `USER_CWD` or falls back to the current working directory if the variable is not set.

3. **Summary Generation (Not Implemented):**  If the `summary` flag is set, it's intended to generate a summary of something, but this functionality is not yet implemented.

4. **File Processing:** If the `input_path` is a file:
    - **Dry Run:** If `dry_run` is true, it prints a message indicating that it's a dry run and displays the file path without actually generating documentation.
    - **Documentation Generation:** If `dry_run` is false, it calls `generate_doc()` from the `document` module to generate documentation for the specified file, passing the file path and the initialized provider.

5. **Directory Processing:** If the `input_path` is a directory:
    - **File Discovery:** It uses the `find_files()` function from the `file` module to find all files within the directory that should be processed.
    - **Dry Run:** If `config.dry_run` is true (note the use of the global config object here), it prints a dry run message and displays a tree-like representation of the files found using `render_tree()` from the `file` module.
    - **Documentation Generation:** If `config.dry_run` is false, it iterates through each file found and calls `generate_doc()` to generate documentation for each file, passing the file path and the initialized provider.
    - **Table of Contents Generation:** After processing all files, it calls `generate_toc()` from the `document` module to generate a table of contents for the documented files.

6. **Error Handling:** If the `input_path` is neither a file nor a directory, it prints an error message.


## Modules and External Dependencies

The code utilizes several modules:

- **`os`**:  Used for interacting with the operating system, specifically to get environment variables and the current working directory.
- **`pathlib`**: Provides object-oriented filesystem paths.
- **`config`**:  A custom module (likely containing configuration settings read from a configuration file or environment variables). The `config` module exposes `input_path`, `dry_run`, and `summary` attributes.
- **`util`**:  A custom module providing utility functions, including `initialize_provider()`.
- **`document`**: A custom module containing functions for generating documentation (`generate_doc()` and `generate_toc()`).
- **`file`**: A custom module containing functions related to file operations, including `find_files()` and `render_tree()`.

## Execution

The script's execution starts at the `if __name__ == "__main__":` block. It calls the `main` function with arguments retrieved from the `config` module: `config.input_path`, `config.dry_run`, and `config.summary`. This approach allows configuring the script's behavior through the `config` module.

# Full listing of src/main.py
```{'python'}
"""
Doc-buddy entry point.
https://github.com/scott-r-lindsey/doc-buddy/
"""

# from document.tree import tree_from_dir, find_files, render_tree
import os
from pathlib import Path
from config import config
from util import initialize_provider
from document import generate_doc, generate_toc
from file import render_tree, find_files


def main(input_path: Path, dry_run: bool, summary: bool) -> None:
    """
    Main function to process files.

    Args:
        input_path (str): Path to the input directory or file.
        file_types (List[str]): List of file types to process.
        dry_run (bool): If True, perform a dry run.
        summary (bool): A dictionary summarizing some information.
    """
    provider = initialize_provider()  # Initialize the provider

    # Get the project directory from USER_CWD or fallback to current working directory
    project_path = os.getenv("USER_CWD", os.getcwd())

    if summary:
        print("Generating summary...")
        print("Not implemented yet.")

    else:
        if input_path.is_file():
            if dry_run:
                print("- Dry run enabled. No files will be created.")
                print(f"File to be processed: {input_path}")

            else:
                # If it's a single file, document it
                generate_doc(input_path, provider)
                print("Done!")

        elif input_path.is_dir():
            files = find_files()

            if config.dry_run:
                print("Dry run enabled. No files will be created.")
                print("Files to be processed:")
                print(render_tree(files))

            else:
                # If it's a directory, document all files in it
                for file in files:
                    generate_doc(file, provider)

                # Generate table of contents
                generate_toc(files)
                print("Done!")

        else:
            print(f"Error: '{input_path}' is neither a file nor a directory.")


if __name__ == "__main__":
    # Pass file types only if the input is a directory
    main(config.input_path, config.dry_run, config.summary)

```
<br>
<br>


---
### Automatically generated Documentation for `doc-buddy/src/main.py`
This documentation is generated automatically from the source code. Do not edit this file directly.
Generated by **Doc-Buddy** on **November 09, 2024 18:54:22** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: e4f5dcb09e20896907179c4446f269d9f1c93dd8*
