import re
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.chatbot_service import ChatbotService
from ..serializers import ChatSerializer
from rest_framework.permissions import IsAuthenticated
from ..response.response_success import ResponseSuccess
from ..response.response_error import ResponseError


class ChatbotAnswerView(APIView):
    def format_answer(self, answer):
        sentences = re.split(r"\s*\n\s*|\s*\*\*\s*", answer)
        return [
            re.sub(r"[^\w\s]", "", sentence).strip()
            for sentence in sentences
            if sentence.strip()
        ]

    def post(self, request):
        question = request.data.get("question")
        print("question: ", question)
        try:
            if not question:
                return ResponseError().set_response(
                    error={"question": "Missing question in request"},
                    message=["Missing question in request"],
                )()
            if question is None:
                return ResponseError().set_response(
                    error={"question": "No question"},
                    message=["No question"],
                )()

            try:
                answer = ChatbotService().answer(question)
                cypher = ChatbotService().cypher(question)

            except Exception as e:
                return ResponseError().set_response(
                    message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )()

            if answer is None:
                return ResponseSuccess().set_response(
                    data={"answer": "No answer for this question"},
                    message=["No answer for this question"],
                )()
            return ResponseSuccess().set_response(
                data={"answer": answer.text, "cypher": cypher},
                message=["Answer success"],
            )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class ChatbotHistoryView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        id_user = request.GET.get("id_user")
        try:
            chats = ChatbotService().get_chat_by_user(id_user)
            if isinstance(chats, dict):
                return ResponseError().set_response(
                    error=chats, message=chats["id_user"]
                )()
            serializer = ChatSerializer(chats, many=True)
            return ResponseSuccess().set_response(
                data=serializer.data, message=["Get history success"]
            )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


from rest_framework import viewsets


class ChatViewSet(viewsets.ModelViewSet):
    queryset = ChatbotService().get_all_chat()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Thiết lập `owner` là người dùng hiện tại khi tạo mới
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return ChatbotService().get_chat_by_user(self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        try:
            if not serializer.is_valid():
                return ResponseError().set_response(
                    error=serializer.errors,
                    message=[
                        e.replace("This field", keys)
                        for keys, values in serializer.errors.items()
                        for e in values
                    ],
                )()

            self.perform_create(serializer)

            headers = self.get_success_headers(serializer.data)
            return ResponseSuccess().set_response(
                data=serializer.data, message=["User registered success"]
            )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()
