from rest_framework import serializers
from .models import Folder, File
from .models import Chat
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ["id", "name", "id_parent"]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["id", "id_folder", "name", "content", "src"]


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


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)  
    first_name = serializers.CharField(required=True)  
    last_name = serializers.CharField(required=True) 
    role = serializers.ChoiceField(choices=["admin", "user"], required=False)
    
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name", "role"]

    def create(self, validated_data):
        role = validated_data.pop("role", "user")
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user_group = Group.objects.get(name=role)
        user.groups.add(user_group)

        return user


class LoginSerializer(TokenObtainPairSerializer):
    
    role = serializers.CharField(source='groups__name', read_only=True)
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    def validate(self, attrs):
        user = super().validate(attrs)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
