"""
This module contains the logic to document a single file.
"""

import os
import sys
import threading
import time
from pathlib import Path
from os.path import basename
from config import config
from .generate_footer import generate_footer


def spinner():
    """
    Function to show a spinner while a task is running.
    """
    spinner_chars = ["|", "/", "-", "\\"]
    idx = 0
    while not done:
        sys.stdout.write(f"\rDocumenting file {current_file} {spinner_chars[idx]}")
        sys.stdout.flush()
        idx = (idx + 1) % len(spinner_chars)
        time.sleep(0.1)


def generate_doc(file_path: Path, provider):
    """
    Document a single file and write the output to a file with suffix.
    """
    suffix = config.documentation_suffix

    global done, current_file
    done = False
    current_file = file_path
    input_path = config.input_path

    # get a path for the file_path without the input_path
    relative_path = file_path.relative_to(config.root_path)

    # Start spinner in a separate thread
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    start_time = time.time()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents = file.read()

            # Document the file using the provider
            documentation = provider.document_file(
                file_name=basename(file_path),
                project_path=(file_path.parent),
                file_contents=file_contents,
            )

            if documentation:
                footer = generate_footer(basename(file_path))
                documentation += footer

                output_file_path = config.output_path / relative_path.parent / (
                    basename(relative_path) + suffix
                )

                # create the directory if it does not exist
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                # Write the documentation to the file
                with open(output_file_path, "w", encoding="utf-8") as doc_file:
                    doc_file.write(documentation)

    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        # Stop the spinner
        done = True
        spinner_thread.join()

        # Clear the spinner line and print elapsed time
        elapsed_time = time.time() - start_time
        sys.stdout.write(
            f"\rDocumenting file {file_path} - {elapsed_time:.2f} seconds\n"
        )
