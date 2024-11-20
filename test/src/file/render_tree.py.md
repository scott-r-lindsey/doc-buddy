[<< Table of Contents](../../index.md)

# AI Generated documentation for `doc-buddy/src/file/render_tree.py`
---
The `src/file/render_tree.py` file provides functions to render a list of file paths as a tree structure, either in plain text (Markdown compatible) or HTML format.  It uses the `config.input_path` variable to display paths relative to the input directory.

The `render_tree` function takes a list of file paths (`files`), a boolean `markdown` flag, and a boolean `include_size` flag as input. It constructs a dictionary representing the tree structure and then converts it to a string representation.  If the `markdown` flag is True, file names are rendered as Markdown links. If the `include_size` flag is True, file sizes are appended to the file names. The tree is constructed by splitting each file path into parts based on the operating system's path separator and recursively building nested dictionaries.  The inner `build_tree_string` function recursively traverses the tree dictionary and generates the string representation using appropriate prefixes for branches ("├── " or "└── ") and indentation. File sizes are displayed in bytes when `include_size` is True.

The `render_tree_html` function takes a list of file paths (`files`) and an optional `extension` string.  It generates an HTML representation of the directory tree. Similar to `render_tree`, it creates a nested dictionary structure. The `build_html_string` inner function generates the HTML string. File names are rendered as HTML links pointing to the respective files with the provided `extension` appended to the filename.  The HTML output uses `<pre>` tags with `monospace` font for displaying the tree structure, improving readability, and includes the project name from `config.project_name` at the top.  Notably, the indentation in the HTML output is handled using HTML non-breaking spaces (`&nbsp;`) and the vertical line character (`│`). Each file is a clickable link that opens in a new tab.

# Full listing of src/file/render_tree.py
```python
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

```
<br>
<br>


---
### Automatically generated Documentation for `doc-buddy/src/file/render_tree.py`
This documentation is generated automatically from the source code. Do not edit this file directly.
Generated by **Doc-Buddy** on **November 20, 2024 15:10:02** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: 95d11f067c1bbf87e1127584466814b22ed990f2*
