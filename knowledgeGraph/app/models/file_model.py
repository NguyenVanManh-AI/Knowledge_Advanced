from django.db import models
from .folder_model import Folder


class File(models.Model):

    id = models.AutoField(primary_key=True)
    id_folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="files"
    )
    name = models.CharField(max_length=100)
    name_os = models.CharField(max_length=100, null=True)
    content = models.TextField(blank=True, null=True)
    content_cypher = models.JSONField(blank=True, null=True)
    src = models.CharField(max_length=100, null=True)

    def update_name(self, new_name):
        self.name = new_name
        self.save()

    def update_idFolder(self, id_folder):
        self.id_folder = id_folder
        self.save()

    def update_content_construct(self, new_content):
        self.content_construct = new_content
        self.save()

    def update_content(self, new_content):
        self.content = new_content
        self.save()

    def update_src(self, src):
        self.src = src
        self.save()

    def __str__(self):
        return self.name
