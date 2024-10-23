"""
Doc-buddy entry point.
https://github.com/scott-r-lindsey/doc-buddy/
"""
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from util import get_absolute_path, initialize_provider
from document.single_file import document_single_file

load_dotenv()


def process_directory(directory_path, project_path, file_types, dry_run, provider):
    """
    Recursively process all files in a directory that match the given file types.
    """
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = Path(root) / file_name
            if any(file_path.suffix == f".{file_type}" for file_type in file_types):
                document_single_file(file_path, project_path, dry_run, provider)


def main(input_path, file_types, dry_run, summary):
    """
    Main function to read a file or directory and optionally run in dry-run mode.
    """
    provider = initialize_provider()  # Initialize the provider

    # Resolve the absolute path of the input (either file or directory)
    absolute_path = Path(get_absolute_path(input_path))

    # Get the project directory from USER_CWD or fallback to current working directory
    project_path = os.getenv("USER_CWD", os.getcwd())

    if summary:
        print("Generating summary...")
        print("Not implemented yet.")

    else:
        if absolute_path.is_file():
            # If it's a single file, document it
            document_single_file(absolute_path, project_path, dry_run, provider)

        elif absolute_path.is_dir():
            if not file_types:
                print(
                    "Error: '--file-types' is required when the input is a directory."
                )
                return
            # If it's a directory, process files recursively
            process_directory(absolute_path, project_path, file_types, dry_run, provider)
        else:
            print(f"Error: '{absolute_path}' is neither a file nor a directory.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read a file or directory and optionally run in dry-run mode."
    )
    parser.add_argument(
        "input_path", type=str, help="The path to the file or directory to be read."
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

    args = parser.parse_args()

    # Pass file types only if the input is a directory
    main(args.input_path, args.file_types, args.dry_run, args.summary)
