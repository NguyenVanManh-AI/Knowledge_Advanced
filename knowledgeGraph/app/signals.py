from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Folder, File
from django.conf import settings
import os


@receiver(post_delete, sender=Folder)
def delete_files_on_folder_delete(sender, instance, **kwargs):
    files = instance.files.all()
    if files:
        for file in files:
            file_path = os.path.join(settings.BASE_DIR, file.src.lstrip("/"))
            if os.path.isfile(file_path):
                os.remove(file_path)
            file.delete()


@receiver(post_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    file_path = os.path.join(settings.BASE_DIR, instance.src.lstrip("/"))
    if os.path.isfile(file_path):
        os.remove(file_path)
