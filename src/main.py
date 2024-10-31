"""
Doc-buddy entry point.
https://github.com/scott-r-lindsey/doc-buddy/
"""

# from document.tree import tree_from_dir, find_files, render_tree
import os
from dotenv import load_dotenv
from util import initialize_provider
from document.single_file import document_single_file
from file import render_tree, find_files
from config import config

load_dotenv()


def main(
    input_path: str, dry_run: bool, summary: bool
) -> None:
    """
    Main function to process files.

    Args:
        input_path (str): Path to the input directory or file.
        file_types (List[str]): List of file types to process.
        dry_run (bool): If True, perform a dry run.
        summary (Dict[str, int]): A dictionary summarizing some information.
    """
    provider = initialize_provider()  # Initialize the provider

    # Get the project directory from USER_CWD or fallback to current working directory
    project_path = os.getenv("USER_CWD", os.getcwd())

    if summary:
        print("Generating summary...")
        print("Not implemented yet.")

    else:
        if input_path.is_file():
            # If it's a single file, document it
            document_single_file(input_path, project_path, dry_run, provider)

        elif input_path.is_dir():
            files = find_files()

            if config.dry_run:
                print("Dry run enabled. No files will be created.")
                print("Files to be processed:")
                print(render_tree(files, True))

        else:
            print(f"Error: '{input_path}' is neither a file nor a directory.")


if __name__ == "__main__":
    config.initialize()

    # Pass file types only if the input is a directory
    main(config.input_path, config.dry_run, config.summary)
