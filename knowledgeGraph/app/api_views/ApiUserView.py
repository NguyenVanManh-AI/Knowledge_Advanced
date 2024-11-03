from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import RegisterSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..response.response_success import ResponseSuccess
from ..response.response_error import ResponseError
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)

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


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
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

            token_data = serializer.validated_data
            user_serializer = UserProfileSerializer(serializer.user)
            
            return ResponseSuccess().set_response(
                data={"token": token_data, "user": user_serializer.data}
                    , message=["User login success"]
            )()
        except AuthenticationFailed as e:
            username = request.data.get("username")
            password = request.data.get("password")
            
            User = get_user_model()

            try:
                user = User.objects.get(username=username)
                if not user.check_password(password):
                    return ResponseError().set_response(
                        error = {"password":"password is wrong"},
                    )()
            except User.DoesNotExist:
                return ResponseError().set_response(
                        error = {"username":"username is wrong"},
                    )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self,request):
        try :
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
