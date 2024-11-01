from rest_framework import serializers
from .models import Folder,File

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name','id_parent']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'id_folder', 'name','content','src']
        

from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'question', 'answer', 'time', 'owner']  # Bao gồm các trường bạn muốn hiển thị
        read_only_fields = ['owner']  # Thiết lập `owner` là read-only
        