from ..models.chatbot_model import Chat
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = [
            "id",
            "question",
            "answer",
            "time",
            "owner",
        ]
        read_only_fields = ["owner"]
