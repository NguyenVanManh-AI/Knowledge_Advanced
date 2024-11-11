from ..models.file_model import File
from ..models.folder_model import Folder
from typing import Dict, List
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from ..Module_Final.class_text2neo4j import Text2Neo4j as t2n


class FileRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileRepository, cls).__new__(cls)
        return cls._instance

    def add_file(self, file: File, file_content, content_struct, content_cypher):
        # print("content", file_content)
        path = default_storage.save(file.name, ContentFile(file_content))
        # src = f"/media/{file_path}"
        newFile = File(
            id_folder=file.id_folder,
            name=file.name,
            name_os=file.name_os,
            content=content_struct,
            content_cypher=content_cypher,
        )
        try:
            t2n().push_to_neo4j(newFile.content_cypher)
            print("Push to neo4j")

            newFile.save()
            print("url:", settings.BASE_URL_DOWNLOAD)
            print("id:", newFile.id)
            newFile.update_src(f"{settings.BASE_URL_DOWNLOAD}{newFile.id}")
            print("src", newFile.src)
            return newFile

        except Exception as e:
            return e

    def get_file_by_id(self, id) -> File:
        return File.objects.filter(id=id).first()

    def update_name_file(self, file: File, name):
        try:
            file.update_name(name)
        except Exception as e:
            return e

    def update_folder(self, file: File, folder):
        try:
            file.update_idFolder(folder)
        except Exception as e:
            return e

    def delete_file(self, file):
        try:
            file.delete()
            return file
        except Exception as e:
            return e

    def view_file_by_id(self, file) -> Dict:
        try:
            folder = Folder.objects.filter(id=file.id_folder.id).first()
            data = {"file": file, "folder": folder.name}
            return data
        except Exception as e:
            return e

    def find_file_by_name(self, id_folder=None, search_name="") -> List[File]:
        result_files = File()
        if not id_folder:
            result_files = File.objects.filter(name__icontains=search_name)
        else:
            result_files = File.objects.filter(
                name__icontains=search_name, id_folder=id_folder
            )
        return result_files

    def download_file(self, id_file):
        file = File.objects.filter(id=id_file).first()
        error = {}
        if not file:
            error["id"] = ["File is not found"]
        if not error:
            path_file = os.path.join(
                settings.BASE_DIR, "media", "uploads", file.name_os
            )
            print("path os: ", path_file)
            if os.path.exists(path_file):

                return path_file
        return error
