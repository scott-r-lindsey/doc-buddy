"""
Doc-buddy entry point.
https://github.com/scott-r-lindsey/doc-buddy/
"""

# from document.tree import tree_from_dir, find_files, render_tree
import os
from pathlib import Path
from config import config
from util import initialize_provider
from file import render_tree, find_files
from document import generate_doc, generate_toc, add_readme


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

    context_files = find_files(config.targets_root_path, False)
    context_tree = render_tree(context_files, False, True, config.targets_root_path)

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

                # Add a README file
                add_readme()
                print("Done!")

        else:
            print(f"Error: '{input_path}' is neither a file nor a directory.")


if __name__ == "__main__":
    # Pass file types only if the input is a directory
    main(config.input_path, config.dry_run, config.summary)
