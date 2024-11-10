"""
This module provides an AI provider for interacting with the Google GenAI API.
"""

import os
import google.generativeai as genai
from .ai_provider import AIProvider


class GoogleGenAIProvider(AIProvider):
    """
    AI provider for interacting with the Google GenAI API.
    """

    def __init__(self):
        self.configure_genai()

    def configure_genai(self):
        """
        Configures the GenAI API using the environment variable GOOGLE_GENAI_API_KEY.
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)

    def document_file(self, file_name, project_path, file_contents):
        """
        Documents a file using the Google GenAI API by providing the file path,
        file name, and its contents.

        Args:
            file_name (str): The name of the file to document.
            project_path (str): The project path where the file is located.
            file_contents (str): The contents of the file to be documented.

        Returns:
            str: The generated documentation for the file.
        """
        from config import config

        prompt = self.generate_prompt(file_name, project_path, file_contents)

        # Prepare the request payload for the chat API
        try:
            model = genai.GenerativeModel(config.model)

            response = model.generate_content(prompt)

            # Extract and return the documentation from the response
            return response.text

        except Exception as e:
            print(f"Error occurred while generating documentation: {e}")
            return None
