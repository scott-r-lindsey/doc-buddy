import os
from pathlib import Path
from config import config


def render_tree(files, markdown=False):
    """
    Renders the list of files as a tree structure, similar to the Unix 'tree' command.

    :param files: List of file paths to be rendered as a tree.
    :param markdown: Boolean indicating whether to render file names as Markdown links.
    :return: A string representing the tree structure.
    """
    tree = {}
    for file_path in files:
        # get the path relative to config.input_path
        file = os.path.relpath(file_path, config.input_path)

        parts = file.split(os.sep)
        current = tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    def build_tree_string(current, path="", indent=""):
        tree_str = ""
        keys = sorted(current.keys())
        for index, key in enumerate(keys):
            is_last = index == len(keys) - 1
            prefix = "└── " if is_last else "├── "
            full_path = os.path.join(path, key)
            if markdown and not current[key]:
                # Render as markdown link if markdown is enabled and it's a file
                tree_str += f"{indent}{prefix}[{key}]({full_path})\n"
            else:
                tree_str += f"{indent}{prefix}{key}\n"
            new_indent = indent + ("    " if is_last else "│   ")
            tree_str += build_tree_string(current[key], full_path, new_indent)
        return tree_str

    return build_tree_string(tree)
