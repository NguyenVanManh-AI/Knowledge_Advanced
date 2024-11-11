from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model


class UserRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserRepository, cls).__new__(cls)
        return cls._instance

    def get_user_by_id(self, id_user):
        return User.objects.filter(id=id_user).first()

    def get_user_by_username(self, username):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist as e:
            return str(e)
