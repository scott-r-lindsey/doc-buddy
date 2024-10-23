"""
This file contains the base class for an AI provider.
"""

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """
    Base class for an AI provider. Extend this class to add support for other providers.
    """

    @abstractmethod
    def document_file(self, file_name, project_path, file_contents):
        """
        Document a file.
        :param file_name: The name of the file.
        :param project_path: The path to the project.
        :param file_contents: The contents of the file.
        :return: The document ID.
        """
        pass
