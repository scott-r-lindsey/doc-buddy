"""
This file contains the base class for an AI provider.
"""

import os
import sys
from abc import ABC, abstractmethod


default_prompt = """
You are a top tier software developer skilled at docomenting and explaining code.
You have been asked to document code in a project named {project_name}.

You are not to return the code itself, but rather a detailed explanation of the code.

The file layout is as follows:
{document_tree}

{function_block}

The file you must document is: {file_name}

Make sure to include explanations for all functions, classes, and key logic in the file.
Do not wrap the output in a code block.  Do not start your document with a heading; one will automatically be added.

{file_name} Contents:
----------------------------------------
{file_contents}
"""


class AIProvider(ABC):
    """
    Base class for an AI provider. Extend this class to add support for other providers.
    """

    @abstractmethod
    def document_file(
        self,
        file_name: str,
        project_path: str,
        file_contents: str,
        notify_user_toast: str,
        tree: str,
    ):
        """
        Document a file.
        :param file_name: The name of the file.
        :param project_path: The path to the project.
        :param file_contents: The contents of the file.
        :param notify_user_toast: The toast notification to display to the user.
        :param tree: The tree structure of the project.
        :return: The document created by the AI.
        """

    @property
    def function_block(self):
        """
        The default function block that can be overridden by child classes.
        :return: The default function block as a string.
        """
        return """
        You may ask for the contents of any file in the project via function calling. Do not hesitate
        to ask for the contents of a file if it would help you document the file you are currently working on.
        """

    def generate_prompt(
        self, file_name: str, project_path: str, file_contents: str, tree: str
    ):
        """
        Generate a prompt for the user to provide documentation for a file.
        :return: The prompt.
        """
        from config import config

        custom_prompt_template = default_prompt

        if config.ai_prompt:
            custom_prompt_template = config.ai_prompt

        prompt = custom_prompt_template.format(
            project_name=config.project_name,
            document_tree=tree,
            file_name=f"{project_path}/{file_name}",
            file_contents=file_contents,
            function_block=self.function_block,
        )

        if config.prompt_debug:
            print(f"\nPrompt:\n{prompt}")
            sys.exit()

        return prompt

    def retrieve_file_contents(self, file_path: str):
        """
        Retrieve the contents of a file.
        :param file_path: The path to the file.
        :return: The contents of the file.
        """
        # validate the file path is relative
        if not os.path.isabs(file_path):
            raise ValueError("File path must be relative.")

        # validate the file path does not contain ".."
        if ".." in file_path:
            raise ValueError("File path cannot contain '..'.")

        # convert the file path to an absolute path
        file_path = os.path.abspath(file_path)

        # validate the file path is within the current directory
        if not file_path.startswith(os.getcwd()):
            raise ValueError("File path must be within the current directory.")

        with open(file_path, "r") as file:
            return file.read()
