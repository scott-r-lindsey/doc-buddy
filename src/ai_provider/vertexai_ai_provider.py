"""
This module provides an implementation of the AIProvider interface using the Vertex AI API.
"""

import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from .ai_provider import AIProvider


class VertexAIProvider(AIProvider):
    """
    An AIProvider implementation that uses the Vertex AI API to generate content.
    """

    def __init__(self):
        project_id = os.environ['GOOGLE_VERTEXAI_PROJECT']
        region = os.environ['GOOGLE_VERTEXAI_LOCATION']
        vertexai.init(project=project_id, location=region)

    def document_file(self, file_name, project_path, file_contents):
        """
        Documents a file using the Google Vertexai API by providing the file path,
        file name, and its contents.

        Args:
            file_name (str): The name of the file to document.
            project_path (str): The project path where the file is located.
            file_contents (str): The contents of the file to be documented.

        Returns:
            str: The generated documentation for the file.

        """

        prompt = self.generate_prompt(file_name, project_path, file_contents)

        generative_multimodal_model = GenerativeModel(os.environ['GOOGLE_VERTEXAI_MODEL'])
        response = generative_multimodal_model.generate_content([prompt])

        return response.candidates[0].content.parts[0].text
