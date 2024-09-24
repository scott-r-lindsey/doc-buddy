import os
from pathlib import Path

def get_absolute_path(file_path):
    """
    Returns the absolute path of the file, taking into account the USER_CWD environment variable.
    If USER_CWD is set, it uses that as the base directory; otherwise, it resolves the file path
    from the current working directory.
    """
    user_cwd = os.getenv('USER_CWD')

    if user_cwd:
        base_path = Path(user_cwd).resolve()
        absolute_path = (base_path / file_path).resolve()
    else:
        absolute_path = Path(file_path).resolve()

    return absolute_path

def read_file(file_path, dry_run=False):
    # Get the absolute path using the separate function
    absolute_path = get_absolute_path(file_path)

    if dry_run:
        print(f"Dry run: Would read file '{absolute_path}'")
        return

    try:
        with open(absolute_path, 'r') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: File '{absolute_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")
