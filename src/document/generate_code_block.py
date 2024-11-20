from .guess_language_for_markdown import guess_language_for_markdown


def generate_code_block(code: str, file_name):
    """
    Generate a code block with a specific language.
    """
    language = guess_language_for_markdown(file_name)

    block = f"\n# Full listing of {file_name}\n"
    block += f"```{language}\n{code}\n```\n"

    return block
