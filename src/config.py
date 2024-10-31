# config.py

import os
import argparse
from pathlib import Path
from typing import Optional
from util import get_absolute_path

class Config:
    def __init__(self):
        self.input_path: Optional[str] = None
        self.file_types: Optional[str] = []
        self.dry_run: bool = False
        self.summary: bool = False
        self.provider: str = ""
        self.gitmode: bool = False
        self.root_path: str = ""
        self.doc_root: str = ""

        # change to the project path
        os.chdir(os.getenv("USER_CWD", os.getcwd()))

    def load_from_env(self):
        """Load configuration from environment variables."""
        self.provider = os.getenv("AI_PROVIDER", "")

    def load_from_args(self, args):
        """Load configuration from parsed command line arguments."""
        if args.input_path is not None:
            self.input_path = args.input_path
        if args.file_types is not None:
            self.file_types = args.file_types
        if args.dry_run is not None:
            self.dry_run = args.dry_run
        if args.summary is not None:
            self.summary = args.summary
        if args.doc_root is not None:
            self.doc_root = get_absolute_path(args.doc_root)

    def find_paths(self):
        print(f"Documentation will be created in {self.doc_root}")

        self.input_path = Path(self.input_path).resolve()
        print (f"Input path is {self.input_path}")

        # Change directory to the starting directory
        os.chdir(self.input_path.parent)

        # Look for a ".git" directory in containing directories
        path = self.input_path

        while True:
            if (path / ".git").exists():
                self.gitmode = True
                self.root_path = path
                break
            # Get the parent directory
            if path.parent == path:
                break  # Reached the root, stop searching
            path = path.parent

        if self.gitmode:
            print(f"Git root found at {self.root_path}")
        else:
            print("No git root found.")

    def initialize(self):
        """Initialize the configuration one time from environment and CLI args."""
        self.load_from_env()

        parser = argparse.ArgumentParser(
            description="Read a file or directory and optionally run in dry-run mode."
        )
        parser.add_argument(
            "input_path", type=str, help="The path to the file or directory to be read."
        )
        parser.add_argument(
            "doc_root", type=str, help="The path to the documentation root."
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

        # Step 3: Update config with command line arguments
        self.load_from_args(args)

        # Step 4: Find the root of the git repository
        self.find_paths()

# Create a global config instance to be shared across all modules
config = Config()
