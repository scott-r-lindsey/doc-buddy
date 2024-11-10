[<< Table of Contents](../../index.md)

# AI Generated documentation for `doc-buddy/src/file/render_tree.py`
---
# `render_tree.py`

This file provides functions for rendering a list of file paths as a tree structure, similar to the output of the Unix `tree` command. It offers two rendering methods: one for plain text/Markdown output and another for HTML.  The tree structure is generated relative to the `config.input_path` defined in the `config.py` file.

## Functions

### `render_tree(files, markdown=False)`

This function renders the given file paths as a tree structure in plain text or Markdown format.

* **`files`**: A list of file paths.
* **`markdown`**: A boolean flag. If `True`, file names are rendered as Markdown links; otherwise, plain text is used.
* **Returns**: A string representing the tree structure.

The function builds a nested dictionary representing the directory structure. It then traverses this dictionary recursively to build the string representation of the tree, using appropriate prefixes ("├── " and "└── ") to indicate the tree branches and indentation to visualize the hierarchy.  When the `markdown` flag is set to `True`, leaf nodes (files) are rendered as Markdown links using the relative path from the `config.input_path`.


### `render_tree_html(files, extension="")`

This function renders the given file paths as an HTML tree structure, enclosed within `<pre>` tags with `monospace` font styling for consistent display.

* **`files`**: A list of file paths.
* **`extension`**: A string representing an extension to be added to each file link.  This is useful for linking to generated documentation files, for example.
* **Returns**: A string representing the HTML tree structure.

Similar to `render_tree`, this function builds a nested dictionary representing the directory structure. It then traverses this dictionary recursively, generating HTML output.  File names are rendered as HTML links, with the `extension` appended to the link target.  Non-leaf nodes (directories) are rendered as plain text. The output uses HTML non-breaking spaces (`&nbsp;`) and line breaks (`<br>`) to maintain the tree structure and uses a monospace font within `<pre>` tags to ensure proper alignment. The project name from `config.project_name` is also included at the beginning of the output.


## Key Logic and Concepts

* **Relative Paths**:  Both functions calculate relative paths using `os.path.relpath(file_path, config.input_path)`. This ensures the tree structure is displayed relative to the input directory specified in the configuration.
* **Recursive Tree Building**:  Both functions use a recursive helper function (`build_tree_string` and `build_html_string` respectively) to build the tree structure string.  This approach effectively handles arbitrary directory depths and nesting.
* **Markdown Links**:  The `render_tree` function supports generating Markdown links when `markdown=True`.
* **HTML Formatting**: The `render_tree_html` function uses `<pre>` tags with `monospace` font styling to ensure the tree is rendered correctly in HTML, handling whitespace and indentation appropriately. It also adds an optional `extension` to the file links and displays the `project_name`.


## Dependencies

* `os`: Used for path manipulation and operating system related functionalities.
* `pathlib`: Although imported, `Path` is not explicitly used in this current version of the code.
* `config`:  A custom module (presumably `config.py`) containing configuration parameters, specifically `config.input_path` and `config.project_name`. This module is responsible for providing the root path against which relative paths are calculated and the name of the project to be displayed.

# Full listing of src/file/render_tree.py
```python
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
Generated by **Doc-Buddy** on **November 09, 2024 19:45:34** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: b01f9573f01b626efe9b415f7392e374029af615*
