"""
This module contains the logic to document a single file.
"""

import os


def document_single_file(file_path, project_path, dry_run, provider):
    """
    Document a single file and write the output to a file with '-apidoc.md' suffix.
    """
    suffix = os.getenv("DOCUMENTATION_SUFFIX", "-apidoc.md")

    try:
        if not dry_run:
            with open(file_path, "r", encoding="utf-8") as file:
                file_contents = file.read()

            # Document the file using the provider (OpenAI)
            documentation = provider.document_file(
                file_name=file_path.name,
                project_path=project_path,
                file_contents=file_contents,
            )
            if documentation:
                # Define output file path with original filename + '-apidoc.md' suffix
                output_file_path = file_path.parent / (file_path.name + suffix)

                # Write the documentation to the file
                with open(output_file_path, "w", encoding="utf-8") as doc_file:
                    doc_file.write(documentation)

                print(f"Documentation generated and saved to: {output_file_path}")
            else:
                print(f"Failed to generate documentation for: {file_path}")
        else:
            print(f"Dry run: would have documented the file '{file_path}'")

    except Exception as e:
        print(f"An error occurred during execution: {e}")
