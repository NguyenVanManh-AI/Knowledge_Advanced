from ..Module_Final.class_QA_Neo4j import QAUsingNeo4j as qa
from ..models import Chat


class ChatbotRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatbotRepository, cls).__new__(cls)
        return cls._instance

    def answer(self, question):
        result = qa().full_question_answer(question)
        print(type(result))
        if isinstance(result, str):
            return None
        else:
            return result
            
    def cypher(self, question):
        result = qa().query_to_cypher(question)
        print(type(result))
        return result
    
    def get_chat_by_user(self,user):
        return Chat.objects.filter(owner=user).order_by('time')
    
    def get_all_chat(self):
        return Chat.objects.all()
    
        
            
