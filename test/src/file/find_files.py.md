[<< Table of Contents](../../index.md)

# AI Generated documentation for `doc-buddy/src/file/find_files.py`
---
The `find_files.py` file contains functions to locate files within a given directory, either by traversing the directory structure directly or by utilizing git commands if the directory is within a git repository.  It uses the `config` module to determine the appropriate behavior.

The primary function, `find_files(input_path: Path = None)`, orchestrates the file finding process.  If no `input_path` is provided, it defaults to the path specified in the `config.input_path` variable.  It then checks the `config.gitmode` setting. If `gitmode` is true, it calls `get_git_repo_files()` to retrieve files from the git repository, using `config.root_path` as the repository's root.  Otherwise, it uses `get_regular_folder_files()` to get files from a standard directory.  In both cases, the resulting list of strings (representing file paths) is converted to a list of `Path` objects by `convert_str_array_to_path_array()` before being returned.

The `get_regular_folder_files(folder_path)` function recursively searches the provided `folder_path` and returns a list of file paths relative to the specified folder.  It uses `os.walk` to traverse the directory structure and constructs relative paths using `os.path.relpath`.

The `get_git_repo_files(repo_path: Path, folder_path: Path = None)` function retrieves files from a git repository. It constructs a `git ls-files` command, including options for untracked, cached, and ignored files according to `.gitignore`.  If `folder_path` is provided, the command is modified to limit the search to that specific folder within the repository. The command is executed using `subprocess.run`.  The output of the command is then processed to create a list of file paths.  If `config.file_types` is defined (containing a list of file extensions), the list is further filtered to include only files with matching extensions.  Any errors during the git command execution are caught, a message is printed, and an empty list is returned.

Finally, `convert_str_array_to_path_array(str_array)` takes a list of file paths (as strings) and converts them to a list of `Path` objects. It joins each file path string from the `str_array` with the `config.input_path` and creates a `Path` object from the resulting combined path. This ensures that the returned paths are absolute paths based on the input path defined in the configuration.

# Full listing of src/file/find_files.py
```python
import os
import subprocess
from pathlib import Path
from config import config


def find_files(input_path: Path = None):

    if input_path is None:
        input_path = config.input_path

    gitmode = config.gitmode
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
Generated by **Doc-Buddy** on **November 20, 2024 15:09:53** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: 95d11f067c1bbf87e1127584466814b22ed990f2*
