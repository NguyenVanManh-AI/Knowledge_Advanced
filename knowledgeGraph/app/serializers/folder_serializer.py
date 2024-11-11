from ..models.folder_model import Folder
from rest_framework import serializers


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ["id", "name", "id_parent"]
