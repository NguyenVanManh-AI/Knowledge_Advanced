from django.contrib.auth.models import User, Group
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..serializers.user_serializer import (
    RegisterSerializer,
    UserProfileSerializer,
    LoginSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from ..response.response_success import ResponseSuccess
from ..response.response_error import ResponseError
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from ..services.user_service import UserService


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            data_register = UserService().register(serializer, self)
            print(data_register)
            if isinstance(data_register, dict):
                return ResponseError().set_response(
                    error=data_register,
                    message=[value[0] for value in data_register.values()],
                )()

            return ResponseSuccess().set_response(
                data=data_register[0], message=["User registered success"]
            )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            data_login = UserService().login(serializer, request.data)
            if isinstance(data_login, dict):
                return ResponseError().set_response(
                    error=data_login,
                    message=[value[0] for value in data_login.values()],
                )()
            elif isinstance(data_login, str):
                return ResponseError().set_response(
                    message=[data_login], status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            else:
                return ResponseSuccess().set_response(
                    data={"token": data_login[0], "user": data_login[1]},
                    message=["User login success"],
                )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        try:
            user = request.user
            return ResponseSuccess().set_response(
                data={
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                message=["Get Dashboard success"],
            )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()
