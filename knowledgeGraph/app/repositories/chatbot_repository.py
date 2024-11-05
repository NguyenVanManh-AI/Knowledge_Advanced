from ..Module_Final.class_QA_Neo4j import QAUsingNeo4j as qa
from ..models import Chat
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

    def get_chat_by_user(self, id_user):
        error = {}
        if id_user is None:
            error["id_user"] = ["id_user is required"]
            return error
        if not id_user:
            error["id_user"] = ["id_user is not empty"]
            return error
        user = User.objects.filter(id=id_user).first()
        if user is None:
            error["id_user"] = ["user is not found"]
            return error
        return Chat.objects.filter(owner=user).order_by("time")

    def get_all_chat(self):
        return Chat.objects.all()
