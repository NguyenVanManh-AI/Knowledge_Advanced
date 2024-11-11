from django.db.models.signals import post_delete
from django.dispatch import receiver
from ..models.file_model import Folder
from django.conf import settings
import os


@receiver(post_delete, sender=Folder)
def delete_files_on_folder_delete(sender, instance, **kwargs):
    print("receive delete folder")
    files = instance.files.all()
    if files:
        for file in files:
            file_path = os.path.join(settings.BASE_DIR, file.src.lstrip("/"))
            if os.path.isfile(file_path):
                os.remove(file_path)
            file.delete()
