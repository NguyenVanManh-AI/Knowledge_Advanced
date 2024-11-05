from ..repositories.chatbot_repository import ChatbotRepository

class ChatbotService:
    def __init__(self):
        self.chatbotRepository = ChatbotRepository()

    def answer(self, question):
        return self.chatbotRepository.answer(question)

    def cypher(self, question):
        return self.chatbotRepository.cypher(question)
    
    def get_chat_by_user(self,id_user):
        return self.chatbotRepository.get_chat_by_user(id_user)
    
    def get_all_chat(self):
        return self.chatbotRepository.get_all_chat()