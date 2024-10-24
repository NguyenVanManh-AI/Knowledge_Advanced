from ..models import Folder, File
from typing import Dict, List
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os


class FileRepository:
    def add_file(self, file, folder) -> File:
        folder = Folder.objects.filter(id=folder.id).first()
        if not folder:
            return None
        if file.content_type == "text/plain":
            file_content = file.read()
        else:
            return None

        file_path = default_storage.save(
            f"uploads/{file.name}", ContentFile(file_content)
        )
        src = f"/media/{file_path}"
        newFile = File(
            id_folder=folder,
            name=file.name,
            content=file_content.decode("utf-8"),
            src=src,
        )

        newFile.save()
        return newFile

    def get_file_by_id(self, id) -> File:
        return File.objects.filter(id=id).first()

    def update_file(self, id_file, new_name_file, id_folder) -> File:
        file = self.get_file_by_id(id_file)
        if not file:
            return None
        if new_name_file:
            file.update_name(new_name_file)
        if id_folder:
            if Folder.objects.filter(id=id_folder).first():
                file.update_idFolder(Folder.objects.filter(id=id_folder).first())
            else:
                return None
        file.save()
        return file

    def delete_file(self, id_file) -> File:
        file = self.get_file_by_id(id_file)
        if not file:
            return None
        file.delete()
        return file

    def view_file_by_id(self, id_file) -> Dict:
        file = self.get_file_by_id(id_file)
        if not file:
            return None
        folder = Folder.objects.filter(id=file.id_folder.id).first()

        data = {"file": file, "folder": folder.name}
        return data

    @staticmethod
    def find_file_by_name(id_folder=None, search_name="") -> List[File]:
        result_files = File()
        if not id_folder:
            result_files = File.objects.filter(name__icontains=search_name)
        else:
            result_files = File.objects.filter(
                name__icontains=search_name, id_folder=id_folder
            )
        return result_files
    
