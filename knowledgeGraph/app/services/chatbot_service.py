from ..repositories.chatbot_repository import ChatbotRepository
from ..repositories.user_repository import UserRepository
class ChatbotService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatbotService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "chatbotRepository"):
            self.chatbotRepository = ChatbotRepository()

    def answer(self, question):
        return self.chatbotRepository.answer(question)

    def cypher(self, question):
        return self.chatbotRepository.cypher(question)
    
    def get_chat_by_user(self,id_user):
        error = {}
        if id_user is None:
            error["id_user"] = ["id_user is required"]
            return error
        if not id_user:
            error["id_user"] = ["id_user is not empty"]
            return error
        user = UserRepository().get_user_by_id(id_user)
        if user is None:
            error["id_user"] = ["user is not found"]
            return error
        return self.chatbotRepository.get_chat_by_user(user)
    
    def get_all_chat(self):
        return self.chatbotRepository.get_all_chat()