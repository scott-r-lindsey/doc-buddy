from pathlib import Path
from config import config


def generate_preface(file_path: Path):
    """Generate a markdown preface block for documentation files.

    Args:
        file_path (Path): The path to the file being documented, relative to project root

    Returns:
        str: A markdown formatted preface block containing ToC link and file header

    Raises:
        ValueError: If file_path is not relative or has less than 2 parts
    """
    if file_path.is_absolute():
        raise ValueError("file_path must be relative to project root")
    if len(file_path.parts) < 2:
        raise ValueError("file_path must have at least 2 parts (e.g., dir/file)")

    block = ""
    block += (
        f"[<< Table of Contents](../{'../' * (len(file_path.parts) -2)}index.md)\n\n"
    )
    block += f"# AI Generated documentation for `{config.project_name}/{file_path}`\n"
    block += "---\n"

    return block
