import argparse
import os
from dotenv import load_dotenv
from util import read_file, get_absolute_path
from pathlib import Path
from AIProvider.OpenAIProvider import OpenAIProvider
from AIProvider.GoogleGenAIProvider import GoogleGenAIProvider

load_dotenv()

# Initialize provider globally
provider = None

def initialize_provider():
    """
    Initialize the AI provider.
    """
    global provider

    if os.getenv('AI_PROVIDER') == 'GOOGLE':
        provider = GoogleGenAIProvider()
    else:
        provider = OpenAIProvider()

def document_single_file(file_path, project_path, dry_run):
    """
    Document a single file and write the output to a file with '-apidoc.md' suffix.
    """
    global provider  # Access the global provider
    suffix = os.getenv('DOCUMENTATION_SUFFIX', '-apidoc.md')

    try:
        if not dry_run:
            with open(file_path, 'r') as file:
                file_contents = file.read()

            # Document the file using the provider (OpenAI)
            documentation = provider.document_file(file_name=file_path.name,
                                                     project_path=project_path,
                                                     file_contents=file_contents)
            if documentation:
                # Define output file path with original filename + '-apidoc.md' suffix
                output_file_path = file_path.parent / (file_path.name + suffix)

                # Write the documentation to the file
                with open(output_file_path, 'w') as doc_file:
                    doc_file.write(documentation)

                print(f"Documentation generated and saved to: {output_file_path}")
            else:
                print(f"Failed to generate documentation for: {file_path}")
        else:
            print(f"Dry run: would have documented the file '{file_path}'")

    except Exception as e:
        print(f"An error occurred during execution: {e}")

def process_directory(directory_path, project_path, file_types, dry_run):
    """
    Recursively process all files in a directory that match the given file types.
    """
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = Path(root) / file_name
            if any(file_path.suffix == f".{file_type}" for file_type in file_types):
                document_single_file(file_path, project_path, dry_run)

def main(input_path, file_types, dry_run):
    initialize_provider()  # Initialize the provider

    # Resolve the absolute path of the input (either file or directory)
    absolute_path = Path(get_absolute_path(input_path))

    # Get the project directory from USER_CWD or fallback to current working directory
    project_path = os.getenv('USER_CWD', os.getcwd())

    if absolute_path.is_file():
        # If it's a single file, document it
        document_single_file(absolute_path, project_path, dry_run)
    elif absolute_path.is_dir():
        if not file_types:
            print("Error: '--file-types' is required when the input is a directory.")
            return
        # If it's a directory, process files recursively
        process_directory(absolute_path, project_path, file_types, dry_run)
    else:
        print(f"Error: '{absolute_path}' is neither a file nor a directory.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Read a file or directory and optionally run in dry-run mode.")
    parser.add_argument('input_path', type=str, help="The path to the file or directory to be read.")
    parser.add_argument('--file-types', type=str, nargs='*', help="File types to process when input is a directory (e.g., 'py js jsx').")
    parser.add_argument('--dry-run', action='store_true', help="Perform a dry run without actually reading the file.")

    args = parser.parse_args()

    # Pass file types only if the input is a directory
    main(
        args.input_path,
        args.file_types,
        args.dry_run
    )

