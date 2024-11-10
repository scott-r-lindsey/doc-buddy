[<< Table of Contents](../../index.md)

# AI Generated documentation for `doc-buddy/src/file/find_files.py`
---
# File: src/file/find_files.py

This file provides functionality for finding files within a given directory, with support for both regular folders and git repositories. It uses the `config` module for configuration settings, particularly regarding whether to use git and the input path.

## Functions

### `find_files()`

This function is the main entry point for finding files.  It determines whether to operate in "git mode" based on the `config.gitmode` setting.

- If `gitmode` is True, it uses `get_git_repo_files()` to retrieve files from the git repository, respecting `.gitignore` and file extension filters.
- If `gitmode` is False, it uses `get_regular_folder_files()` to retrieve all files within the specified folder.

The function returns a list of `Path` objects representing the found files.

### `get_regular_folder_files(folder_path)`

This function recursively searches a given `folder_path` and returns a list of file paths relative to the provided folder path.  It uses `os.walk` to traverse the directory structure and constructs relative paths using `os.path.relpath`.

### `get_git_repo_files(repo_path: Path, folder_path: Path = None)`

This function retrieves files within a git repository, optionally limited to a specific `folder_path` within the repository.  It uses the `git ls-files` command to get a list of tracked, cached, and untracked files while respecting `.gitignore`.

- `repo_path`: The path to the root of the git repository.
- `folder_path`: An optional path to a subdirectory within the repository.

The function constructs a `git ls-files` command with appropriate flags (e.g., `--others`, `--cached`, `--exclude-standard`). If a `folder_path` is provided, it's added to the command to restrict the results. The command is executed using `subprocess.run`.

The output from `git ls-files` is parsed, and the file list is optionally filtered based on file extensions defined in `config.file_types`. The function returns a list of file paths relative to the git repository root.  Error handling is included to catch `subprocess.CalledProcessError` in case the `git` command fails.

### `convert_str_array_to_path_array(str_array)`

This helper function takes a list of strings representing file paths and converts them into a list of `Path` objects. It uses `config.input_path` to construct the absolute path for each file. This ensures that the returned paths are absolute paths based on the input directory specified in the configuration, even though the file paths from git or the regular file search are relative.

# Full listing of src/file/find_files.py
```{'python'}
import os
import subprocess
from pathlib import Path
from config import config


def find_files():

    gitmode = config.gitmode
    input_path = config.input_path
    git_root = config.root_path

    if gitmode:
        return convert_str_array_to_path_array(get_git_repo_files(git_root, input_path))

    return convert_str_array_to_path_array(get_regular_folder_files(input_path))


def get_regular_folder_files(folder_path):
    """
    Recursively finds all files in a regular folder (not a git repository).

    :param folder_path: Path to the folder to list files from.
    :return: A list of file paths relative to the root of the folder.
    """
    files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.relpath(os.path.join(root, filename), start=folder_path)
            files.append(file_path)
    return files


def get_git_repo_files(repo_path: Path, folder_path: Path = None):
    """
    Finds all the files in a specific folder within a git repository, honoring
    .gitignore and filtering by extensions.

    :param repo_path: Path to the root of the git repository.
    :param folder_path: Specific folder within the repository to list files from.
    :param extensions: List of file extensions to filter by (e.g., ['.py', '.txt']).
    :return: A list of file paths relative to the root of the repository.
    """
    try:
        # Construct the command to run 'git ls-files'
        cmd = [
            "git",
            "-C",
            repo_path,
            "ls-files",
            "--others",
            "--cached",
            "--exclude-standard",
        ]

        # If a folder path is provided, restrict the output to that folder
        if folder_path:
            cmd.append(folder_path)

        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Split the output into individual file paths and filter out any empty strings
        files = [file.strip() for file in result.stdout.split("\n") if file.strip()]

        # If extensions are provided via config.file_types, filter the files by the given extensions
        if len(config.file_types) > 0:
            extensions = [
                ext if ext.startswith(".") else f".{ext}" for ext in config.file_types
            ]
            filtered_files = []
            for file in files:
                for ext in extensions:
                    if file.endswith(ext):
                        filtered_files.append(file)
                        break

            files = filtered_files

        return files

    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        return []


def convert_str_array_to_path_array(str_array):
    return [Path(os.path.join(config.input_path, file)) for file in str_array]

```
<br>
<br>


---
### Automatically generated Documentation for `doc-buddy/src/file/find_files.py`
This documentation is generated automatically from the source code. Do not edit this file directly.
Generated by **Doc-Buddy** on **November 09, 2024 18:53:49** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: e4f5dcb09e20896907179c4446f269d9f1c93dd8*
