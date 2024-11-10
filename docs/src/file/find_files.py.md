[<< Table of Contents](../../index.md)

# AI Generated documentation for `doc-buddy/src/file/find_files.py`
---
# File: find_files.py

This file is responsible for finding files within a given directory, optionally using git to respect `.gitignore` and filtering by file extensions specified in a configuration file.

## Functions

### `find_files()`

This function is the main entry point for file discovery. It determines whether to use git based on the `config.gitmode` setting.  If `gitmode` is true, it utilizes `get_git_repo_files()` to retrieve files from the git repository. Otherwise, it uses `get_regular_folder_files()` to retrieve files from a regular directory. The returned file list is always converted from strings to `Path` objects using `convert_str_array_to_path_array()`.


### `get_regular_folder_files(folder_path)`

This function recursively searches for all files within the specified `folder_path`. It uses `os.walk()` to traverse the directory structure and builds a list of file paths relative to the provided `folder_path`.

### `get_git_repo_files(repo_path: Path, folder_path: Path = None)`

This function retrieves files within a git repository, respecting `.gitignore` and optionally filtering by file extensions defined in `config.file_types`. It uses the `git ls-files` command to achieve this.

- `repo_path`: The path to the root of the git repository.
- `folder_path`: An optional path to a subdirectory within the repository. If provided, only files within this subdirectory will be returned.

The function constructs a `git ls-files` command with the following options:
- `--others`: Includes untracked files.
- `--cached`: Includes staged files.
- `--exclude-standard`: Excludes files ignored by the standard .gitignore and .gitattributes files.

If `folder_path` is provided, it's added to the command to limit the scope of the search.

The output of the command is captured, split into individual file paths, and filtered to remove empty strings. If `config.file_types` is populated, the list is further filtered to include only files with the specified extensions.

Any errors encountered while executing the git command are caught and printed, and an empty list is returned.


### `convert_str_array_to_path_array(str_array)`

This function converts a list of file paths represented as strings to a list of `Path` objects.  It joins the `config.input_path` with each file name in the input array using `os.path.join` before creating the `Path` object. This ensures absolute paths are generated if a relative input path was provided in the config.


## Dependencies

- `os`: Used for file system operations.
- `subprocess`: Used for running git commands.
- `pathlib`: Used for path manipulation.
- `config`: A custom module assumed to contain configuration settings like `gitmode`, `input_path`, `root_path`, and `file_types`.

# Full listing of src/file/find_files.py
```python
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
Generated by **Doc-Buddy** on **November 09, 2024 19:45:17** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: b01f9573f01b626efe9b415f7392e374029af615*
