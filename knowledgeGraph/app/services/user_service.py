from ..repositories.user_repository import UserRepository
from rest_framework.exceptions import AuthenticationFailed
from ..serializers.user_serializer import (
    RegisterSerializer,
    UserProfileSerializer,
    LoginSerializer,
)

import functools
import logging
from datetime import datetime
from pathlib import Path

LOG_FILE_PATH = Path("user_service.log")

def log_to_file(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        method_name = func.__name__

        log_message = (
            f"[{datetime.now()}] Method '{method_name}' was called.\n"
            f"Arguments: {args[1:]}, {kwargs}\n"
        )

        with open(LOG_FILE_PATH, "a") as file:
            file.write(log_message)

        logging.info(log_message)

        result = func(*args, **kwargs)

        result_message = f"[{datetime.now()}] Result of '{method_name}': {result}\n"
        with open(LOG_FILE_PATH, "a") as file:
            file.write(result_message)

        return result

    return wrapper

class UserService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "userRepository"):
            self.userRepository = UserRepository()

    @log_to_file
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

    @log_to_file
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
