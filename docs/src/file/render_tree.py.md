[<< Table of Contents](../../index.md)

# AI Generated documentation for `doc-buddy/src/file/render_tree.py`
---
# File: src/file/render_tree.py

This file provides functions to render a list of file paths as a tree structure, both in plain text (suitable for Markdown) and HTML format.  It uses the `config.input_path` as the base directory to generate relative paths within the tree.

## Functions

### `render_tree(files, markdown=False)`

This function takes a list of file paths and renders them as a tree structure, similar to the output of the Unix `tree` command.

* **`files`**: A list of file paths.
* **`markdown`**: A boolean flag. If `True`, file names are rendered as Markdown links. Defaults to `False`.
* **Returns**: A string representing the tree structure.

The function first builds a nested dictionary representing the directory structure. It then uses a recursive helper function, `build_tree_string`, to generate the string representation of the tree. The `build_tree_string` function uses "├── " and "└── " to draw the tree branches, and "│   " and "    " for indentation.  When `markdown` is `True`, leaf nodes (files) are rendered as Markdown links using the relative path from `config.input_path`.

### `render_tree_html(files, extension="")`

This function renders the list of files as an HTML tree structure, enclosed within `<pre>` tags with `monospace` font styling. This provides a visually clear representation of the directory hierarchy within an HTML document.

* **`files`**: A list of file paths.
* **`extension`**:  A string representing an extension to append to each file link. This is useful for linking to specific versions or formats of files. Defaults to an empty string.
* **Returns**: A string representing the HTML tree structure.

Similar to `render_tree`, this function constructs a nested dictionary representing the file hierarchy. It then uses a recursive helper function, `build_html_string`, to generate the HTML representation.  `build_html_string` uses HTML line breaks (`<br>`) and non-breaking spaces (`&nbsp;`) for formatting the tree structure. File names are rendered as HTML links (`<a>`) with the specified `extension` appended to the `href` attribute. The links open in a new tab (`target="_blank"`). The project name from `config.project_name` is displayed at the root of the tree.  The entire tree is wrapped in a `<pre>` tag with the `monospace` font style applied.


## Key Logic and Dependencies

Both functions rely on:

* `os`: For path manipulation and splitting file paths.
* `pathlib.Path`: Although imported, it is unused in the current code.
* `config`:  A module (presumably containing project configurations) used to access `config.input_path` and `config.project_name`.  `config.input_path` provides the base directory for calculating relative paths, ensuring the tree structure represents the project's file organization relative to this input path. `config.project_name` is used as the title for the HTML tree.

The recursive helper functions (`build_tree_string` and `build_html_string`) are crucial for traversing the nested dictionary and building the string representation of the tree structure.  They handle the logic for adding prefixes, indentation, and creating links appropriately.

# Full listing of src/file/render_tree.py
```{'python'}
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
Generated by **Doc-Buddy** on **November 09, 2024 18:54:04** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: e4f5dcb09e20896907179c4446f269d9f1c93dd8*
