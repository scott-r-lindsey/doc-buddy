import os
import subprocess
from pathlib import Path
from config import config


def find_files(input_path: Path = None, limit_by_extensions_if_git=True):

    if input_path is None:
        input_path = config.input_path

    gitmode = config.gitmode
    git_root = config.targets_root_path

    if gitmode:
        return convert_str_array_to_path_array(
            get_git_repo_files(git_root, input_path, limit_by_extensions_if_git),
            config.targets_root_path,
        )

    return convert_str_array_to_path_array(
        get_regular_folder_files(input_path), input_path
    )


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


def get_git_repo_files(
    repo_path: Path, folder_path: Path = None, limit_by_extensions=True
):
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
        if (len(config.file_types) > 0) and limit_by_extensions:
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


def convert_str_array_to_path_array(str_array, input_path=config.input_path):
    return [Path(os.path.join(input_path, file)) for file in str_array]
