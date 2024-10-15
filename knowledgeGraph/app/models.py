from django.db import models


class Folder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def update_name(self, new_name):
        self.name = new_name
        self.save()

    def __str__(self):
        return self.name


class File(models.Model):

    id = models.AutoField(primary_key=True)
    id_folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="files"
    )
    name = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    content_construct = models.JSONField(blank=True, null=True)
    
    def update_name(self,new_name):
        self.name = new_name
        self.save()
    
    def update_content_construct(self,new_content):
        self.content_construct = new_content
        self.save()
        
    def update_content(self,new_content):
        self.content = new_content
        self.save()
        
    def __str__(self):
        return self.name
