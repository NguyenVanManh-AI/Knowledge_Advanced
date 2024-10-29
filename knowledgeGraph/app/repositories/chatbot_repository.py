from ..Module_Final.class_QA_Neo4j import QAUsingNeo4j as qa
class ChatbotRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatbotRepository, cls).__new__(cls)
        return cls._instance
    
    def answer(self,question):
        if question :
            return qa().full_question_answer(question)
        else:
            return None