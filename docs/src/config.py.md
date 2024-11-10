[<< Table of Contents](../index.md)

# AI Generated documentation for `doc-buddy/src/config.py`
---
# `config.py` Module Documentation

This module defines the `Config` class, responsible for parsing command-line arguments, environment variables, and determining the project's configuration for the `doc-buddy` project.  It leverages the `pydantic` library for data validation and structure.

## `Config` Class

The `Config` class stores and manages the configuration settings for the application. It uses `pydantic`'s `BaseModel` for structure and validation.

### Attributes

*   **`input_path`:** (Path) The path to the input file or directory to be processed.
*   **`output_path`:** (Path) The path to the directory where the generated documentation will be saved.
*   **`root_path`:** (Path) The root path of the project.  Defaults to the current working directory if no git repository is found. If a git repository is found, it will be the root of that repo.
*   **`user_cwd`:** (Path) Stores the user's original current working directory, set at the start of the application.
*   **`file_types`:** (List[str]) A list of file extensions to include when processing a directory.  If empty, all files are considered.
*   **`dry_run`:** (bool, default=False)  If True, the program will run in dry-run mode, simulating actions but not writing any changes.
*   **`summary`:** (bool, default=False) If True, generates a summary of the entire project.
*   **`gitmode`:** (bool, default=False) Indicates whether the project is being run within a git repository.
*   **`provider`:** (str) The AI provider to be used. Loaded from the `AI_PROVIDER` environment variable.
*   **`model`:** (str, default="") The AI model to be used. Loaded from the `AI_MODEL` environment variable.
*   **`documentation_suffix`:** (str, default=".md") The file extension to use for generated documentation files. Loaded from the `DOCUMENTATION_SUFFIX` environment variable.
*   **`project_name`:** (str) The name of the project, derived from the name of the root directory.

### Methods

#### `__init__(self)`

The constructor for the `Config` class. It performs the following actions:

1.  Saves the user's current working directory.
2.  Loads environment variables from a `.env` file.
3.  Parses command-line arguments.
4.  Loads environment variables for AI provider, model, and documentation suffix.
5.  Determines the input and output paths.
6.  Calls `find_gitmode` to check if the project is within a Git repository and set the `root_path`, `gitmode`, and `project_name` attributes accordingly.
7.  Initializes the `Config` object using the collected information.
8.  Changes the working directory back to the user's original current working directory.

#### `parse_args(self)`

This method uses the `argparse` module to parse command-line arguments.  It defines the following arguments:

*   **`input_path`:** (required) The path to the input file or directory.
*   **`output_path`:** (required) The path to the documentation output directory.
*   **`--file-types`:** (optional) A list of file types to process.
*   **`--dry-run`:** (optional flag) Enables dry-run mode.
*   **`--summary`:** (optional flag) Enables summary generation.

The parsed arguments are returned as an `argparse.Namespace` object.

#### `find_gitmode(self, input_path: Path, user_cwd: Path)`

This method determines if the provided `input_path` is within a git repository.  It does this by traversing up the directory tree from the given `input_path` until it finds a `.git` directory or reaches the root directory.

It returns a tuple containing:

*   **`gitmode`:** (bool) True if a `.git` directory was found, False otherwise.
*   **`root_path`:** (Path) The path to the git root if found, otherwise defaults to the provided `user_cwd`.
*   **`project_name`:** (str) The name of the project derived from the name of the root path directory.


## Global `config` Instance

A global instance of the `Config` class is created at the end of the module:

```python
config = Config()
```

This instance is intended to be used throughout the `doc-buddy` project to access the configuration settings.

# Full listing of src/config.py
```python
"""
This module contains the Config class that is used to parse and store configuration
"""

import os
import argparse
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional, List
from util import get_absolute_path
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

    def __init__(self):
        user_cwd = Path(os.getenv("USER_CWD", os.getcwd()))
        load_dotenv()
        os.chdir(user_cwd)

        args = self.parse_args()

        provider = os.getenv("AI_PROVIDER", "")
        model = os.getenv("AI_MODEL", "")
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
            project_name=project_name,
            documentation_suffix=documentation_suffix,
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
Generated by **Doc-Buddy** on **November 09, 2024 19:44:02** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: b01f9573f01b626efe9b415f7392e374029af615*
