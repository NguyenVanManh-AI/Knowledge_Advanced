from ..repositories.user_repository import UserRepository
from rest_framework.exceptions import AuthenticationFailed
from ..serializers.user_serializer import (
    RegisterSerializer,
    UserProfileSerializer,
    LoginSerializer,
)


class UserService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "userRepository"):
            self.userRepository = UserRepository()

    def login(self, serializer, data):
        try:
            if not serializer.is_valid():
                error = serializer.errors
                for key in error.keys():
                    for i, e in enumerate(error[key]):
                        error[key][i] = e.replace("This field", f"Field {key}")
                return error
            token_data = serializer.validated_data
            user_serializer = UserProfileSerializer(serializer.user)
            role = serializer.user.groups.values_list("name", flat=True)
            data_user = user_serializer.data
            data_user["role"] = role[0]
            return [token_data, data_user]
        except AuthenticationFailed as e:
            username = data.get("username")
            password = data.get("password")
            error = {}
            user = self.userRepository.get_user_by_username(username)
            if isinstance(user, str):
                error["username"] = ["username is wrong"]
            else:
                if not user.check_password(password):
                    error["password"] = ["password is wrong"]
            return error
        except Exception as e:
            return str(e)

    def register(self, serializer, view):
        if not serializer.is_valid():
            error = serializer.errors
            for key in error.keys():
                for i, e in enumerate(error[key]):
                    error[key][i] = e.replace("This field", f"Field {key}")
            return error
        view.perform_create(serializer)
        headers = view.get_success_headers(serializer.data)
        return [serializer.data]
