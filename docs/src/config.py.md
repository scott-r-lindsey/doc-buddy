[<< Table of Contents](../index.md)

# AI Generated documentation for `doc-buddy/src/config.py`
---
Configuration and Argument Parsing for doc-buddy

This module defines the `Config` class, responsible for handling configuration settings and command-line arguments for the doc-buddy project.  It uses `pydantic` for data validation and `argparse` for argument parsing.  Environment variables and a `.env` file can also be used to configure the application.

**Class: Config**

This class stores the configuration for the application. It retrieves values from command-line arguments, environment variables, and defaults.

**Attributes:**

*   `input_path` (Path): Path to the input file or directory.
*   `output_path` (Path): Path to the output directory for documentation.
*   `root_path` (Path): Path to the project's root directory (determined by git root or current working directory).
*   `user_cwd` (Path): Path to the user's current working directory when the script was launched.
*   `file_types` (List[str]): List of file extensions to process (e.g., `["py", "js", "jsx"]`).
*   `dry_run` (bool): If True, performs a dry run without generating documentation. Defaults to False.
*   `summary` (bool): If True, generates a summary of the entire project. Defaults to False.
*   `gitmode` (bool): If True, indicates that a git repository was found.
*   `provider` (str): The AI provider to use (loaded from the `AI_PROVIDER` environment variable).
*   `model` (str): The AI model to use (loaded from the `AI_MODEL` environment variable, defaults to "").
*   `documentation_suffix` (str): The file extension for documentation files (loaded from the `DOCUMENTATION_SUFFIX` environment variable, defaults to ".md").
*   `project_name` (str): The name of the project, derived from the root path.



**Methods:**

*   `__init__(self)`: Constructor for the `Config` class.  Parses command-line arguments, loads environment variables from a `.env` file, determines git root, and initializes all configuration attributes.  It changes the working directory to the user's original working directory before parsing arguments, then returns to it after initialization.

*   `parse_args(self)`:  Uses `argparse` to parse command-line arguments.  Defines arguments for `input_path`, `output_path`, `file-types`, `dry-run`, and `summary`. Returns the parsed arguments.

*   `find_gitmode(self, input_path: Path, user_cwd: Path)`: Determines if the input path is part of a git repository. It searches for a `.git` directory in the input path's parent directories. If found, sets `gitmode` to True and sets `root_path` to the git root directory. Otherwise, uses the provided `user_cwd`.  Returns a tuple containing `gitmode`, `root_path`, and `project_name`.


**Global Variable:**

*   `config = Config()`: Creates a global instance of the `Config` class, making it accessible from other modules in the project.  This is instantiated at the end of the module, ensuring all functions and classes are defined before the global config is created.



**Key Logic:**

1.  Environment variables are loaded from a `.env` file.
2.  Command-line arguments are parsed.
3.  The presence of a git repository is checked.
4.  The configuration object is initialized using data from environment variables, arguments, and the git check.
5.  A global `config` instance is created for access throughout the project.

**Dependencies:**

*   `os`
*   `argparse`
*   `dotenv`
*   `pathlib`
*   `typing`
*   `util` (Assumed to contain a `get_absolute_path` function, not included in the provided code)
*   `pydantic`


This document provides a comprehensive overview of the `config.py` module in the doc-buddy project, explaining its purpose, functionality, and key components. This helps developers understand how configuration is managed and accessed within the project.

# Full listing of src/config.py
```{'python'}
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
Generated by **Doc-Buddy** on **November 09, 2024 18:52:30** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: e4f5dcb09e20896907179c4446f269d9f1c93dd8*
