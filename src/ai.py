import openai
import os
import json

def configure_openai():
    """
    Configures the OpenAI API using the environment variables OPENAI_API_KEY and OPENAI_API_URL.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_URL")


def document_file_via_openai(file_name, project_path, file_contents):
    """
    Documents a file using the OpenAI API by providing the file path, file name, and its contents.

    Args:
        file_name (str): The name of the file to document.
        project_path (str): The project path where the file is located.
        file_contents (str): The contents of the file to be documented.

    Returns:
        str: The generated documentation for the file.
    """
    # Source the OpenAI model and custom prompt from environment variables
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")  # Default to "gpt-4o" if not set
    custom_prompt_template = os.getenv("OPENAI_PROMPT")

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

    # Prepare the message for the chat completion API
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that documents code in detail."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        # Use the newer OpenAI chat completions API with raw response
        response = openai.chat.completions.with_raw_response.create(
            model=openai_model,
            messages=messages,
            max_tokens=4096,  # Adjust token limit based on file size and required detail
            temperature=0.7,  # Creativity level
            n=1
        )

        response = response.parse()

        # Extract and return the documentation from the response
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error occurred while generating documentation: {e}")
        return None

