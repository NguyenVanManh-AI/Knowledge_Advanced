from ..repositories.chatbot_repository import ChatbotRepository
from ..repositories.file_repository import FileRepository
from ..repositories.folder_repository import FolderRepository
from ..repositories.user_repository import UserRepository

class RepositoryFactory:
    @staticmethod
    def create(repository_type):
        if repository_type == "chatbot":
            return ChatbotRepository()
        elif repository_type == "file":
            return FileRepository()
        elif repository_type == "folder":
            return FolderRepository()
        elif repository_type == "user":
            return UserRepository()
        else:
            raise ValueError("Unknown repository type")
