"""
This module provides an AI provider for interacting with the OpenAI API.
"""

import os
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

    def document_file(self, file_name, project_path, file_contents):
        """
        Documents a file using the OpenAI API by providing the file path, file
        name, and its contents.

        Args:
            file_name (str): The name of the file to document.
            project_path (str): The project path where the file is located.
            file_contents (str): The contents of the file to be documented.

        Returns:
            str: The generated documentation for the file.
        """
        from config import config

        prompt = self.generate_prompt(file_name, project_path, file_contents)

        # Prepare the message for the chat completion API
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that documents code in detail.",
            },
            {"role": "user", "content": prompt},
        ]

        try:
            # Use the newer OpenAI chat completions API with raw response
            response = openai.chat.completions.with_raw_response.create(
                model=config.model,
                messages=messages,
                max_tokens=4096,
                temperature=0.7,
                n=1,
            )

            response = response.parse()

            # Extract and return the documentation from the response
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error occurred while generating documentation: {e}")
            return None
