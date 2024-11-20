"""
This module provides an AI provider for interacting with the OpenAI API.
"""

import json
import os
import sys
import openai
from .ai_provider import AIProvider


class OpenAIProvider(AIProvider):
    """
    AI provider for interacting with the OpenAI API.
    """

    def __init__(self):
        self.configure_openai()

    def configure_openai(self):
        """
        Configures the OpenAI API using the environment variables
        OPENAI_API_KEY and OPENAI_API_URL.
        """
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.base_url = os.getenv("OPENAI_API_URL")

    def document_file(
        self, file_name, project_path, file_contents, notify_user_toast, tree
    ):
        """
        Documents a file using the OpenAI API by providing the file path, file
        name, and its contents.

        Args:
            file_name (str): The name of the file to document.
            project_path (str): The project path where the file is located.
            file_contents (str): The contents of the file to be documented.
            notify_user_toast (function): A function to notify the user with a toast message.
            tree (dict): The tree structure of the project.

        Returns:
            str: The generated documentation for the file.
        """

        prompt = self.generate_prompt(file_name, project_path, file_contents, tree)

        # Prepare the message for the chat completion API
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that documents code in detail.",
            },
            {"role": "user", "content": prompt},
        ]

        return self.get_competions(messages, notify_user_toast)

    def get_competions(self, messages, notify_user_toast):
        from config import config

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_additional_file",
                    "description": "Retrieve the contents of an additional files required for documentation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                            },
                        },
                        "required": ["file_paths"],
                        "additionalProperties": False,
                    },
                },
            }
        ]

        while True:
            try:
                response = openai.chat.completions.create(
                    model=config.model,
                    messages=messages,
                    tools=tools,
                    max_tokens=4096,
                    temperature=0.7,
                    n=1,
                )

                if response.choices[0].finish_reason == "tool_calls":
                    message = response.choices[0].message

                    if message.content is not None:
                        notify_user_toast(message.content)

                    # let the llm know what it requested
                    messages.append(response.choices[0].message.model_dump())

                    tool_calls = response.choices[0].message.tool_calls

                    for tool_call in tool_calls:
                        if tool_call.function.name == "get_additional_file":
                            args = json.loads(tool_call.function.arguments)
                            file_path = args["file_path"]
                            notify_user_toast(
                                f"LLM requested additional file: {file_path}"
                            )

                            additional_file_contents = self.retrieve_file_contents(
                                file_path
                            )

                            # send the additional file contents to the llm
                            messages.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "name": "get_additional_file",
                                    "content": json.dumps(additional_file_contents),
                                }
                            )
                        else:
                            sys.exit("Unknown tool call")

                elif response.choices[0].finish_reason == "stop":
                    return response.choices[0].message.content

            except Exception as e:
                print(f"Error occurred while generating documentation: {e}")
                return None
