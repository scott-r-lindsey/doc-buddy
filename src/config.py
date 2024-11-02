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
    documentation_suffix: str = ".md"

    def __init__(self):
        user_cwd = Path(os.getenv("USER_CWD", os.getcwd()))
        load_dotenv()
        os.chdir(user_cwd)

        args = self.parse_args()

        provider = os.getenv("AI_PROVIDER", "")
        documentation_suffix = os.getenv("DOCUMENTATION_SUFFIX", ".md")

        user_cwd = Path(os.getcwd())
        input_path = (
            Path(args.input_path).resolve() if (args.input_path is not None) else None
        )
        output_path = (
            Path(args.output_path).resolve() if (args.output_path is not None) else None
        )

        gitmode, root_path = self.find_gitmode(input_path, user_cwd)

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

        return gitmode, root_path


# Create a global config instance to be shared across all modules
config = Config()
