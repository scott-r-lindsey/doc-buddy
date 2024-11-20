[<< Table of Contents](../index.md)

# AI Generated documentation for `doc-buddy/src/config.py`
---
The `src/config.py` file defines the `Config` class, which is responsible for parsing command-line arguments, environment variables, and determining the git root directory.  An instance of this class is created and stored in a global variable `config`, making it accessible across the project.

**Config Class:**

The `Config` class inherits from `pydantic.BaseModel`, which provides data validation and parsing capabilities.  It stores configuration settings as attributes:

*   **`input_path`:** Path to the input file or directory.
*   **`output_path`:** Path to the output directory for generated documentation.
*   **`root_path`:** Path to the root of the git repository (if found), otherwise defaults to the user's current working directory.
*   **`user_cwd`:** Path to the user's current working directory when the script was started.
*   **`file_types`:** A list of file extensions to process (e.g., \["py", "js"]).
*   **`dry_run`:** Boolean flag indicating whether to perform a dry run without writing changes.
*   **`summary`:** Boolean flag indicating whether to generate a project summary.
*   **`gitmode`:** Boolean flag indicating whether the project is in a git repository.
*   **`provider`:** Name of the AI provider to use.
*   **`model`:** Name of the AI model to use.
*   **`documentation_suffix`:** Suffix for documentation files (defaults to ".md").
*   **`project_name`:** Name of the project, derived from the git root directory name if available.
*   **`ai_prompt`:** Prompt template for the AI model.
*   **`prompt_debug`:** Boolean flag to print AI prompt and exit.



**`__init__` Method:**

The `__init__` method initializes the `Config` object.  It performs the following actions:

1.  Retrieves the user's current working directory using environment variable `USER_CWD` or `os.getcwd()`.
2.  Loads environment variables from a `.env` file.
3.  Changes working directory to the user's CWD using `os.chdir()`.
4.  Parses command-line arguments using `self.parse_args()`.
5.  Retrieves environment variables for AI settings (`AI_PROVIDER`, `AI_MODEL`, `AI_PROMPT`, `DOCUMENTATION_SUFFIX`).
6.  Determines paths and git mode information using `self.find_gitmode()`.
7.  Calls the `super().__init__()` method to initialize the `BaseModel` with the collected settings.
8.  Changes back to the user's working directory.


**`parse_args` Method:**

This method uses `argparse` to parse command-line arguments.  It defines the following arguments:

*   **`input_path` (required):** Path to the input file or directory.
*   **`output_path` (required):** Path to the output directory.
*   **`--file-types` (optional):** List of file extensions.
*   **`--dry-run` (optional flag):** Enables dry run mode.
*   **`--summary` (optional flag):** Enables summary generation.
*   **`--prompt-debug` (optional flag):** Prints AI prompt and exits.

**`find_gitmode` Method:**

This method checks whether the input path is part of a git repository.  It attempts to find a `.git` directory by traversing up the directory tree.  If a `.git` directory is found, it sets `gitmode` to `True` and sets the `root_path` to the git repository root.  If not found, it uses the initial `user_cwd` as the `root_path` and sets `gitmode` to `False`. The method also extracts and returns the project name from the `root_path`.



**Global `config` Instance:**

Finally, the code creates a global instance of the `Config` class: `config = Config()`. This makes the configuration accessible throughout the project without needing to pass it around explicitly.

# Full listing of src/config.py
```python
"""
This module contains the Config class that is used to parse and store configuration
"""

import os
import argparse
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel


class Config(BaseModel):
    # the path to the folder or file to be read
    input_path: Path

    # the path to the documentation root
    output_path: Path

    # the path to the git root
    root_path: Path

    # the path to the user's current working directory
    user_cwd: Path

    file_types: List[str]
    dry_run: bool = False
    summary: bool = False
    gitmode: bool = False
    provider: str
    model: str = ""
    documentation_suffix: str = ".md"
    project_name: str = ""
    ai_prompt: str = ""
    prompt_debug: bool = False

    def __init__(self):
        user_cwd = Path(os.getenv("USER_CWD", os.getcwd()))
        load_dotenv()
        os.chdir(user_cwd)

        args = self.parse_args()

        provider = os.getenv("AI_PROVIDER", "")
        model = os.getenv("AI_MODEL", "")
        ai_prompt = os.getenv("AI_PROMPT", "")
        documentation_suffix = os.getenv("DOCUMENTATION_SUFFIX", ".md")

        user_cwd = Path(os.getcwd())
        input_path = (
            Path(args.input_path).resolve() if (args.input_path is not None) else None
        )
        output_path = (
            Path(args.output_path).resolve() if (args.output_path is not None) else None
        )

        gitmode, root_path, project_name = self.find_gitmode(input_path, user_cwd)

        file_types = args.file_types if args.file_types is not None else []
        dry_run = args.dry_run if args.dry_run is not None else False
        summary = args.summary if args.summary is not None else False
        prompt_debug = args.prompt_debug if args.prompt_debug is not None else False

        super().__init__(
            input_path=input_path,
            output_path=output_path,
            root_path=root_path,
            user_cwd=user_cwd,
            file_types=file_types,
            dry_run=dry_run,
            summary=summary,
            gitmode=gitmode,
            provider=provider,
            model=model,
            ai_prompt=ai_prompt,
            project_name=project_name,
            documentation_suffix=documentation_suffix,
            prompt_debug=prompt_debug,
        )

        # change to the project path
        os.chdir(os.getenv("USER_CWD", os.getcwd()))

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="Read a file or directory and optionally run in dry-run mode."
        )
        parser.add_argument(
            "input_path", type=str, help="The path to the file or directory to be read."
        )
        parser.add_argument(
            "output_path", type=str, help="The path to the documentation root."
        )
        parser.add_argument(
            "--file-types",
            type=str,
            nargs="*",
            help="File types to process when input is a directory (e.g., 'py js jsx').",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Perform a dry run without actually reading the file.",
        )
        parser.add_argument(
            "--summary",
            action="store_true",
            help="Generate a summary of the entire project.",
        )
        parser.add_argument(
            "--prompt-debug",
            action="store_true",
            help="Print the prompt for the AI model and exit.",
        )

        # Parsing the arguments
        args = parser.parse_args()
        return args

    def find_gitmode(self, input_path: Path, user_cwd: Path):
        root_path = user_cwd
        gitmode = False

        # Change directory to the file's parent or the directory itself
        if input_path.is_file():
            os.chdir(input_path.parent)
        else:
            os.chdir(input_path)

        # Start searching for a ".git" directory in containing directories
        path = input_path

        while True:
            if (path / ".git").exists():
                gitmode = True
                root_path = path
                break
            # Move to the parent directory
            if path.parent == path:  # Reached the root directory
                break
            path = path.parent

        if gitmode:
            print(f"-> Git root found at {root_path}")
        else:
            print(f"-> No Git root found, using {root_path}")

        project_name = root_path.name

        return gitmode, root_path, project_name


# Create a global config instance to be shared across all modules
config = Config()

```
<br>
<br>


---
### Automatically generated Documentation for `doc-buddy/src/config.py`
This documentation is generated automatically from the source code. Do not edit this file directly.
Generated by **Doc-Buddy** on **November 20, 2024 15:08:47** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: 95d11f067c1bbf87e1127584466814b22ed990f2*
