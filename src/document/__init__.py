# file/__init__.py
from .generate_toc import generate_toc
from .generate_doc import generate_doc
from .generate_footer import generate_footer
from .guess_language_for_markdown import guess_language_for_markdown
from .generate_preface import generate_preface
from .generate_code_block import generate_code_block

__all__ = [
    "generate_toc",
    "generate_doc",
    "generate_footer",
    "guess_language_for_markdown",
    "generate_preface",
    "generate_code_block",
]
