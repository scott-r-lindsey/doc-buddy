import os
from config import config


def render_tree(files, markdown=False, include_size=False):
    """
    Renders the list of files as a tree structure, similar to the Unix 'tree' command.

    :param files: List of file paths to be rendered as a tree.
    :param markdown: Boolean indicating whether to render file names as Markdown links.
    :param include_size: Boolean indicating whether to include the file size in bytes.
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

            # Determine if we need to add file size
            size_str = ""
            if include_size and not current[key]:  # Only files, not directories
                file_size = os.path.getsize(full_path)
                size_str = f" [{file_size} bytes]"

            if markdown and not current[key]:
                # Render as markdown link if markdown is enabled and it's a file
                tree_str += f"{indent}{prefix}[{key}]({full_path}){size_str}\n"
            else:
                tree_str += f"{indent}{prefix}{key}{size_str}\n"

            new_indent = indent + ("    " if is_last else "│   ")
            tree_str += build_tree_string(current[key], full_path, new_indent)
        return tree_str

    return build_tree_string(tree)


def render_tree_html(files, extension=""):
    """
    Renders the list of files as an HTML tree structure, using monospace font for display.

    :param files: List of file paths to be rendered as a tree.
    :param extension: String to be added as an extension to each file link.
    :return: A string representing the HTML tree structure.
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

    def build_html_string(current, path="", indent=""):
        html_str = ""
        keys = sorted(current.keys())
        for index, key in enumerate(keys):
            is_last = index == len(keys) - 1
            prefix = "└── " if is_last else "├── "
            full_path = os.path.join(path, key)
            if not current[key]:
                # Apply the extension only to the final file link
                full_path_with_extension = full_path + extension
                # Render as an HTML link if it's a file
                html_str += f'{indent}{prefix}<a href="{full_path_with_extension}" target="_blank">{key}</a><br>'
            else:
                html_str += f"{indent}{prefix}{key}<br>"
            new_indent = indent + (
                "&nbsp;&nbsp;&nbsp;&nbsp;" if is_last else "│&nbsp;&nbsp;&nbsp;"
            )
            html_str += build_html_string(current[key], full_path, new_indent)
        return html_str

    html_output = '<pre style="font-family: monospace;">'
    html_output += f"{config.project_name}<br>"
    html_output += build_html_string(tree)
    html_output += "</pre>"
    return html_output
