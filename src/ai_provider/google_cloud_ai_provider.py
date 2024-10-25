
import os
from google.cloud import aiplatform
from .ai_provider import AIProvider

class GoogleCloudAIProvider(AIProvider):

    def __init__(self, project_id, location):
        aiplatform.init(
            project=os.environ.get("GCP_PROJECT"),
            location=os.environ.get("GCP_LOCATION"),
            credentials=os.environ.get("GCP_CREDENTIALS"),
        );

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

        prompt = self.generate_prompt(file_name, project_path, file_contents)


