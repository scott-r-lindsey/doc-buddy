[<< Table of Contents](../../index.md)

# AI Generated documentation for `doc-buddy/src/ai_provider/ai_provider.py`
---
The `ai_provider.py` file defines the abstract base class `AIProvider` for interacting with AI documentation providers.  It lays out the blueprint for concrete AI provider implementations, such as OpenAI, Google Vertex AI, etc., ensuring they all adhere to a consistent interface.  This design promotes modularity and extensibility, allowing for easy integration of new AI providers without modifying core code.

**Class: AIProvider**

This abstract base class defines the common interface for all AI documentation providers.  It uses the `abc` module to enforce the implementation of specific methods in derived classes.

*   **`document_file` (Abstract Method):** This method is the core functionality of any AI provider.  It takes the file name, project path, file contents, a notification message, and the project's directory tree structure as input.  It's responsible for sending these details to the AI model and returning the generated documentation.  Each specific AI provider (e.g., OpenAI, VertexAI) must implement this method to handle the interaction with their respective APIs.

*   **`function_block` (Property):** This property defines a default prompt segment that instructs the AI about its ability to request additional file contents.  This segment guides the AI to use the available API for retrieving more context if needed. Child classes can override this property to provide a customized prompt segment.

*   **`generate_prompt` (Method):** This method constructs the complete prompt sent to the AI model.  It incorporates various pieces of information, including the project name (from the `config` module), the directory tree structure, the file name, file contents, and the `function_block`.  It utilizes a default prompt template but allows customization via a configurable `config.ai_prompt`. It also includes a debugging feature controlled by `config.prompt_debug` which, when enabled, prints the generated prompt and exits the program. This aids in inspecting the prompt during development and troubleshooting.

*   **`retrieve_file_contents` (Method):** This crucial method allows the AI to access the contents of other files within the project directory.  It takes a relative file path as input and returns the file's content.  It performs several security checks:
    *   Ensures the path is relative, preventing access to files outside the project.
    *   Prohibits the use of ".." in the path, further restricting directory traversal attempts.
    *   Confirms the absolute path of the requested file is within the current working directory, adding another layer of security.
    *   Finally, it reads and returns the file contents. This controlled file access allows the AI to request relevant context from other project files for generating more comprehensive documentation.



**Global Variables:**

*   **`default_prompt`:**  This string variable stores the default prompt template.  It contains placeholders for dynamic information, such as project name, file contents, and the directory tree. This template instructs the AI on its role and how to generate documentation.  The use of a template allows flexibility and maintainability, separating the prompt structure from the code that populates it.

# Full listing of src/ai_provider/ai_provider.py
```python
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

```
<br>
<br>


---
### Automatically generated Documentation for `doc-buddy/src/ai_provider/ai_provider.py`
This documentation is generated automatically from the source code. Do not edit this file directly.
Generated by **Doc-Buddy** on **November 20, 2024 15:07:46** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: 95d11f067c1bbf87e1127584466814b22ed990f2*
