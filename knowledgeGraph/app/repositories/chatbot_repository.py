from ..Module_Final.class_QA_Neo4j import QAUsingNeo4j as qa
from ..models.chatbot_model import Chat
from django.contrib.auth.models import User


class ChatbotRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatbotRepository, cls).__new__(cls)
        return cls._instance

    def answer(self, question):
        try :
            result = qa().full_question_answer(question)
            if isinstance(result, str):
                return None
            else:
                return result
        except UnboundLocalError :
            return None

    def cypher(self, question):
        result = qa().query_to_cypher(question)
        print(type(result))
        return result

    def get_chat_by_user(self, user):
        return Chat.objects.filter(owner=user).order_by("time")

    def get_all_chat(self):
        return Chat.objects.all()
