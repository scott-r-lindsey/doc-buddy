import os
import sys
from .ai_provider import AIProvider
from ollama import ChatResponse, Client, Message
from ollama._types import Tool
from config import config
import os.path  

"""
This module provides an AI provider for interacting with the Ollama API.
"""
class OllamaAIProvider(AIProvider):
    """
    AI provider for interacting with the Ollama API.
    """
    def __init__(self):
        self.configure_ollama()

    def configure_ollama(self):
        """
        Configures the Ollama API using the environment variables
        """
        self.client = Client(host=os.getenv("OLLAMA_HOST")) if os.getenv("OLLAMA_HOST") != "" else Client()

    def document_file(
        self, file_name, project_path, file_contents, notify_user_toast, tree
    ):
        """
        Documents a file using the Ollama API by providing the file path, file
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
        messages = []
        messages.append(Message(role="system", content="You are a helpful assistant that documents code in detail."))
        messages.append(Message(role="user", content=prompt))

        return self.get_completions(messages, notify_user_toast)

    def get_completions(self, messages: list[Message], notify_user_toast):
        get_additional_file_tool: Tool = Tool(type="function", function={
            "name": "get_additional_file",
            "description": "Retrieve the contents of an additional files required for documentation.",
            "parameters": {
                "type": "object",
                "required": ["file_path"],
                "properties": {
                    "file_path": { "type": "string", "description": "The path to the additional file."},
                },
            },
        })

        while True:
            try:
                response, message = self.chat(config, messages, get_additional_file_tool)
                if response.get("message") and response.get("message").get("tool_calls"):
                    tool_calls = response.get("message").get("tool_calls")

                    content = tool_calls[0].get("content")
                    if content is not None:
                        notify_user_toast(content)

                    messages.append(message)

                    for tool_call in tool_calls:
                        function = tool_call.get("function")
                        if function:
                            args = function.get("arguments")
                            if function.get("name") == "get_additional_file":
                                if "file_path" not in args:
                                    notify_user_toast("LLM requested additional file, but no file path was provided.")
                                    messages.append(
                                        {
                                            "role": "tool",
                                            "name": "get_additional_file",
                                            "content": None,
                                        }
                                    )
                                    continue

                                file_path = args["file_path"]
                                notify_user_toast(
                                    f"LLM requested additional file: {file_path}"
                                )

                                additional_file_contents = self.retrieve_file_contents(
                                    file_path
                                )

                                messages.append(
                                    {
                                        "role": "tool",
                                        "name": "get_additional_file",
                                        "content": additional_file_contents,
                                    }
                                )
                            else:
                                raise ValueError(f"Unknown tool call: {function.get('name')}")
                    
                elif response.get("done_reason") == "stop":
                    return message.get("content")
            except ConnectionError as e:
                print(f"Error occurred while connecting to the Ollama API: {e}")
                return None
            except ValueError as e:
                print(f"Error occurred while parsing the response from the Ollama API: {e}")
                return None
            except Exception as e:
                print(f"Error occurred while generating documentation: {e}")
                return None

    def chat(self, config, messages, get_additional_file_tool):
        response: ChatResponse = self.client.chat(
                    model=config.model,
                    messages=messages,
                    tools=[get_additional_file_tool],
                )
        message = response.get("message")
        return response, message
