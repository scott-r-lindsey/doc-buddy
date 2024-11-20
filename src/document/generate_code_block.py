from .guess_language_for_markdown import guess_language_for_markdown


def generate_code_block(code: str, file_name: str) -> str:
    """
    Generate a Markdown code block with language syntax highlighting.

    Args:
        code: The source code to be wrapped in a code block.
        file_name: The name of the file, used to determine the language for syntax highlighting.

    Returns:
        A formatted string containing the code wrapped in a Markdown code block with appropriate
        language specification.

    Example:
        >>> generate_code_block("print('hello')", "example.py")
        '\n# Full listing of example.py\n```python\nprint('hello')\n```\n'
    """
    language = guess_language_for_markdown(file_name)

    block = f"\n# Full listing of {file_name}\n"
    block += f"```{language}\n{code}\n```\n"

    return block
