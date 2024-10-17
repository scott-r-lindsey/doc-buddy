import os
import google.generativeai as genai
import json
from .AIProvider import AIProvider

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
        api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        genai.configure(api_key=api_key)

    def document_file(self, file_name, project_path, file_contents):
        """
        Documents a file using the Google GenAI API by providing the file path, file name, and its contents.

        Args:
            file_name (str): The name of the file to document.
            project_path (str): The project path where the file is located.
            file_contents (str): The contents of the file to be documented.

        Returns:
            str: The generated documentation for the file.
        """
        # Source the model and custom prompt from environment variables
        genai_model = os.getenv("GOOGLE_GENAI_MODEL", "models/chat-bison-001")  # Default to "models/chat-bison-001" if not set
        custom_prompt_template = os.getenv("AI_PROMPT")

        # Default prompt if no custom prompt is provided
        default_prompt = (
            f"Please provide detailed documentation for the following file:\n\n"
            f"File Path: {project_path}/{file_name}\n\n"
            f"File Contents:\n{file_contents}\n\n"
            f"Make sure to include explanations for all functions, classes, and key logic in the file."
        )

        # If a custom prompt template is provided, use it with variable substitution
        if custom_prompt_template:
            prompt = custom_prompt_template.format(
                file_name=file_name,
                project_path=project_path,
                file_contents=file_contents
            )
        else:
            prompt = default_prompt

        # Prepare the request payload for the chat API
        try:
            response = genai.generate_message(
                model=genai_model,
                prompt=prompt,
                temperature=0.7,  # Creativity level
                max_output_tokens=4096  # Adjust token limit based on file size and required detail
            )

            # Extract and return the documentation from the response
            return response.messages[0].content

        except Exception as e:
            print(f"Error occurred while generating documentation: {e}")
            return None

