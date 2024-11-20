import os

def guess_language_for_markdown(filename):
    # Extract the file extension
    _, extension = os.path.splitext(filename)
    extension = extension.lower()

    # Define a mapping of extensions to languages for markdown
    extension_mapping = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".html": "html",
        ".css": "css",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
        ".cs": "csharp",
        ".rb": "ruby",
        ".php": "php",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "bash",
        ".go": "go",
        ".rs": "rust",
        ".swift": "swift",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".xml": "xml",
        ".sql": "sql",
        ".kt": "kotlin",
        ".m": "matlab",
        ".r": "r",
        ".pl": "perl",
        ".dockerfile": "dockerfile",
        ".ps1": "powershell",
        ".vim": "vim",
        ".lua": "lua",
        ".scala": "scala",
        ".hs": "haskell",
        ".md": "markdown"
    }

    # Return the markdown language string if found, else return plain text
    return extension_mapping.get(extension, '')
