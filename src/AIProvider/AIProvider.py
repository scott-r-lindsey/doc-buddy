import openai
from abc import ABC, abstractmethod

class AIProvider(ABC):
    """
    Base class for an AI provider. Extend this class to add support for other providers.
    """
    @abstractmethod
    def document_file(self, file_name, project_path, file_contents):
        pass
