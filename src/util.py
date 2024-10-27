"""
This module contains utility functions that are used by the main script.
"""

import os
import sys
from pathlib import Path
from ai_provider.open_ai_provider import OpenAIProvider
from ai_provider.google_gen_ai_provider import GoogleGenAIProvider
from ai_provider.vertexai_ai_provider import VertexAIProvider


def get_absolute_path(file_path: str):
    """
    Returns the absolute path of the file, taking into account the USER_CWD
    environment variable.  If USER_CWD is set, it uses that as the base
    directory; otherwise, it resolves the file path from the current working
    directory.
    """
    user_cwd = os.getenv("USER_CWD")

    if user_cwd:
        base_path = Path(user_cwd).resolve()
        absolute_path = (base_path / file_path).resolve()
    else:
        absolute_path = Path(file_path).resolve()

    return absolute_path


def read_file(file_path: str, dry_run=False):
    """
    Reads the content of the file at the given path.
    If the dry_run flag is set, it only prints the file path and does not read the file.
    """
    # Get the absolute path using the separate function
    absolute_path = get_absolute_path(file_path)

    if dry_run:
        print(f"Dry run: Would read file '{absolute_path}'")
        return

    try:
        with open(absolute_path, "r", encoding="utf-8") as file:
            content = file.read()
            print(content)

    except FileNotFoundError:
        print(f"Error: File '{absolute_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")


def initialize_provider():
    """
    Initialize the AI provider.
    """

    provider_name = os.getenv("AI_PROVIDER").upper()

    # should work uppercase and lowercase, convert to uppercase
    if provider_name == "GOOGLE-GEMINI":
        print("Using Google Gemini AI provider")
        provider = GoogleGenAIProvider()

    elif provider_name == "GOOGLE-VERTEXAI":
        print("Using Vertex AI provider")
        provider = VertexAIProvider()

    elif provider_name == "OPENAI":
        print("Using OpenAI provider")
        provider = OpenAIProvider()

    else:
        print("Error: AI provider not found.")
        sys.exit(1)

    return provider
