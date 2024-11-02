from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import RegisterSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from ..response.response_success import ResponseSuccess
from ..response.response_error import ResponseError


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    pass  # Sử dụng mặc định của TokenObtainPairView để xử lý login


class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class Dashboard(APIView):
    permission_classes = [IsAuthenticated]  # Yêu cầu đăng nhập (sử dụng JWT)

    def get(self, request):
        user = request.user  # Lấy đối tượng người dùng từ request

        # Lấy thông tin người dùng
        return ResponseSuccess().set_response(
            data={
                "status": "Dashboard (Must Login)",
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            message=["Get Dashboard success"],
        )()
