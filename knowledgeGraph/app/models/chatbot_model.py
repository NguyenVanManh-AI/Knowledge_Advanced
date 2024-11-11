from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    question = models.TextField()
    answer = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
