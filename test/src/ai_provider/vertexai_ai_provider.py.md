[<< Table of Contents](../../index.md)

# AI Generated documentation for `doc-buddy/src/ai_provider/vertexai_ai_provider.py`
---
The `vertexai_ai_provider.py` file implements the `VertexAIProvider` class, which is responsible for generating documentation using Google's Vertex AI API.  It inherits from the `AIProvider` abstract base class (not shown in this file).

The `__init__` method initializes the Vertex AI environment. It checks for the required environment variables `GOOGLE_VERTEXAI_PROJECT` and `GOOGLE_VERTEXAI_LOCATION`. If these variables are not set, it raises a `ValueError`.  If the environment variables are present, it initializes the Vertex AI API with the project ID and location.  Finally, it initializes the `_model` attribute to an empty string, presumably to be populated later with a specific generative model.

The core functionality of this class resides in the `document_file` method. This method takes the file name, project path, file contents, a `notify_user_toast` function (likely for UI updates), and the project tree as input. It then constructs a prompt using the `generate_prompt` method (not shown in this file but likely part of the parent class), and creates a list of messages to send to the Vertex AI API.  The first message is a user message containing the generated prompt. If the model hasn't been loaded into the  `_model` attribute, this method loads the model specified by `config.model` before continuing.  Finally, the method calls the `get_completions` method to interact with the Vertex AI API and generate the documentation.

The `get_completions` method handles the interaction with the Vertex AI API using the loaded generative model.  This method sets up a function declaration and tool for `get_additional_file`. This tool allows the LLM to call `get_additional_file` to retrieve the contents of other files within the project to aid in documentation generation. The method enters a loop, sending the accumulated messages to the AI model.

Inside the loop, it checks the response for function calls.  If a function call is present and is named "get_additional_file", it extracts the `file_path` argument. It then notifies the user through the `notify_user_toast` function that the LLM has requested an additional file. Subsequently, it retrieves the contents of the requested file using `retrieve_file_contents` (not defined in this file; perhaps implemented elsewhere).  It then formats this additional content and appends it to the list of messages as a function response.  If the function call is present and has another name, it causes the program to exit, writing "Unknown function call" to stderr.

If no function calls are present, the loop breaks, and the generated text from the AI model is returned.  Any exceptions raised during the interaction with the Vertex AI API are caught and wrapped in a `RuntimeError` with a descriptive message.  This indicates that this class performs its work in a loop, repeatedly querying the LLM, which is allowed to call a user-provided function to retrieve additional context from elsewhere in the project, until the LLM is ready to return its answer.

# Full listing of src/ai_provider/vertexai_ai_provider.py
```python
"""
This module provides an implementation of the AIProvider interface using the Vertex AI API.
"""

import json
import os
import sys
import vertexai
from vertexai.preview.generative_models import (
    Content,
    Part,
    Tool,
    GenerativeModel,
    FunctionDeclaration,
)
from .ai_provider import AIProvider


class VertexAIProvider(AIProvider):
    """
    An AIProvider implementation that uses the Vertex AI API to generate content.
    """

    def __init__(self):
        required_env_vars = {
            "GOOGLE_VERTEXAI_PROJECT": "Google Cloud project ID",
            "GOOGLE_VERTEXAI_LOCATION": "Vertex AI location",
        }

        missing_vars = [var for var in required_env_vars if var not in os.environ]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: "
                f"{', '.join(f'{var} ({required_env_vars[var]})' for var in missing_vars)}"
            )

        project_id = os.environ["GOOGLE_VERTEXAI_PROJECT"]
        region = os.environ["GOOGLE_VERTEXAI_LOCATION"]
        vertexai.init(project=project_id, location=region)

        if not hasattr(self, "_model"):
            self._model = ""

    def document_file(
        self, file_name, project_path, file_contents, notify_user_toast, tree
    ):
        """
        Documents a file using the Google Vertexai API by providing the file path,
        file name, and its contents.

        Args:
            file_name (str): The name of the file to document.
            project_path (str): The project path where the file is located.
            file_contents (str): The contents of the file to be documented.
            notify_user_toast (function): A function to notify the user with a toast message.
            tree (dict): The tree of the project.

        Returns:
            str: The generated documentation for the file.

        """
        from config import config

        if self._model is None or self._model == "":
            self._model = GenerativeModel(config.model)

        prompt = self.generate_prompt(file_name, project_path, file_contents, tree)

        messages = [
            Content(
                role="user",
                parts=[
                    Part.from_text(prompt),
                ],
            ),
        ]

        return self.get_completions(messages, notify_user_toast)

    def get_completions(self, messages, notify_user_toast):
        """
        Get completions for the given messages using the Google Vertexai API.

        Args:
            messages (list): A list of messages to generate completions for.
            notify_user_toast (function): A function to notify the user with a toast message.

        Returns:
            list: A list of completions generated by the AI model.

        """

        get_additional_file = FunctionDeclaration(
            name="get_additional_file",
            description="Retrieve the contents of an additional file required for documentation.",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                },
                "required": ["file_path"],
            },
        )

        get_additional_file_tool = Tool(
            function_declarations=[get_additional_file],
        )

        while True:
            try:

                response = self._model.generate_content(
                    contents=messages,
                    tools=[get_additional_file_tool],
                )

                if response.candidates[0].content.parts[0].function_call is not None:
                    # one or more function calls

                    messages.append(response.candidates[0].content)
                    parts = response.candidates[0].content.parts

                    function_return_parts = []

                    for part in parts:
                        function_name = part.function_call.name

                        if function_name == "get_additional_file":
                            file_path = part.function_call.args["file_path"]

                            notify_user_toast(
                                f"LLM requested additional file: {file_path}"
                            )

                            additional_file_contents = self.retrieve_file_contents(
                                file_path
                            )

                            function_return_parts.append(
                                Part.from_function_response(
                                    name="get_additional_file",
                                    response={
                                        "content": {
                                            "contents": additional_file_contents
                                        }
                                    },
                                )
                            )

                        else:
                            sys.exit("Unknown function call")

                    messages.append(
                        Content(
                            role="function",
                            parts=function_return_parts,
                        ),
                    )

                else:
                    return response.candidates[0].content.parts[0].text

            except Exception as e:
                raise RuntimeError(f"Failed to generate documentation: {str(e)}") from e

```
<br>
<br>


---
### Automatically generated Documentation for `doc-buddy/src/ai_provider/vertexai_ai_provider.py`
This documentation is generated automatically from the source code. Do not edit this file directly.
Generated by **Doc-Buddy** on **November 20, 2024 15:08:27** via **gemini-1.5-pro-002**

For more information, visit the [Doc-Buddy on GitHub](https://github.com/scott-r-lindsey/doc-buddy).  
*doc-buddy Commit Hash: 95d11f067c1bbf87e1127584466814b22ed990f2*
