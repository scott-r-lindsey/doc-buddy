"""
This file contains the base class for an AI provider.
"""

import os
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """
    Base class for an AI provider. Extend this class to add support for other providers.
    """

    @abstractmethod
    def document_file(self, file_name: str, project_path: str, file_contents: str):
        """
        Document a file.
        :param file_name: The name of the file.
        :param project_path: The path to the project.
        :param file_contents: The contents of the file.
        :return: The document ID.
        """

    def generate_prompt(self, file_name: str, project_path: str, file_contents: str):
        """
        Generate a prompt for the user to provide documentation for a file.
        :return: The prompt.
        """

        custom_prompt_template = os.getenv("AI_PROMPT")

        # Default prompt if no custom prompt is provided
        default_prompt = (
            f"Please create a document which explains the following file:\n\n"
            f"File Path: {project_path}/{file_name}\n\n"
            f"File Contents:\n{file_contents}\n\n"
            f"Make sure to include explanations for all functions, classes, and key"
            f" logic in the file."
            f" Do not wrap the output in a code block."
        )

        # If a custom prompt template is provided, use it with variable substitution
        if custom_prompt_template:
            prompt = custom_prompt_template.format(
                file_name=file_name,
                project_path=project_path,
                file_contents=file_contents,
            )
        else:
            prompt = default_prompt

        return prompt
