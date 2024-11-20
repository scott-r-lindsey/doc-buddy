[<< Table of Contents](../index.md)

# AI Generated documentation for `doc-buddy/src/main.py`
---
The `main.py` file serves as the entry point for the doc-buddy application. It orchestrates the process of generating documentation for a given input, which can be either a single file or a directory.

The script starts by importing necessary modules and functions from other parts of the project, including configuration settings (`config`), utility functions (`util`), document generation functions (`document`), and file processing functions (`file`).

The core logic resides within the `main` function, which takes three arguments:

1.  **input_path (Path):**  A Path object representing the input file or directory to be documented.

2.  **dry_run (bool):**  A flag indicating whether to perform a dry run without generating actual documentation files.

3.  **summary (bool):** A flag indicating whether to generate a summary of files to be processed. Currently, this functionality is not implemented and prints a placeholder message.

The `main` function begins by initializing the AI provider using `initialize_provider()` from the `util` module.  It then determines the project path using the `USER_CWD` environment variable or falls back to the current working directory.

Next, it identifies all files within the project directory using `find_files` and generates a tree-like representation using `render_tree` to provide context for the documentation process.

The subsequent logic branches based on whether the `input_path` points to a file or a directory:

**File Input:**

If `input_path` is a file, the script either performs a dry run, printing information about the context and the file to be processed, or proceeds with generating the documentation for the single file using `generate_doc`, passing the `input_path`, `provider`, and `context_tree` as arguments.

**Directory Input:**

If `input_path` is a directory, it retrieves a list of files within the directory using `find_files()`.  Similar to the file input case, it either performs a dry run, printing a rendered tree of files to be processed, or generates documentation for each file in the directory using `generate_doc`.  After processing all files, it calls `generate_toc` to create a table of contents for the generated documentation.

**Error Handling:**

If `input_path` is neither a file nor a directory, it prints an error message.

Finally, if the script is run directly (`if __name__ == "__main__":`), the `main` function is called with parameters loaded from the `config` module, passing the input path, dry run flag, and summary flag as arguments.

# Full listing of src/main.py
```python
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

    context_files = find_files(Path(project_path))
    context_tree = render_tree(context_files, False, True)

    if summary:
        print("Generating summary...")
        print("Not implemented yet.")

    else:
        if input_path.is_file():
            if dry_run:
                print("-> Dry run enabled. No files will be created.")
                print(f"-> Context contains {len(context_files)} files.")
                print(f"-> File to be processed: {input_path}")

            else:
                # If it's a single file, document it
                print(f"-> Context contains {len(context_files)} files.")
                print(f"-> Processing single file '{input_path}'")
                generate_doc(input_path, provider, context_tree)
                print("Done!")

        elif input_path.is_dir():
            files = find_files()

            if dry_run:
                print("-> Dry run enabled. No files will be created.")
                print(f"-> Context contains {len(context_files)} files.")
                print("Files to be processed:")
                print(render_tree(files))

            else:
                print(f"-> Context tree contains {len(context_files)} files.")
                print(f"-> Processing {len(files)} files...")
                for file in files:
                    generate_doc(file, provider, context_tree)

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
Generated by **Doc-Buddy** on **November 20, 2024 15:10:13** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: 95d11f067c1bbf87e1127584466814b22ed990f2*
