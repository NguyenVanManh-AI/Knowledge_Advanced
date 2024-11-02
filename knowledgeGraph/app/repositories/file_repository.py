from ..models import Folder, File
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

    def add_file(self, file, id_folder):
        error = {}
        print("id_folder", id_folder)
        print("file", file)
        if id_folder is None:
            error["id_folder"] = ["Field id_folder is required"]
        elif not id_folder:
            error["id_folder"] = ["id_folder is not empty"]
        if file is None:
            error["file"] = ["Field file is required"]

        if error:
            return error

        folder = Folder.objects.filter(id=id_folder).first()
        if not folder:
            error["id_folder"] = ["Folder not found"]
        if file.name.endswith(".txt"):
            file_content = file.read()
        else:
            error["file"] = ["Format file is not support"]
        if not error:
            # print("content", file_content)
            path = default_storage.save(file.name, ContentFile(file_content))
            # src = f"/media/{file_path}"
            content_ = t2n().gen_structure_data(file_content.decode("utf-8"))
            newFile = File(
                id_folder=folder,
                name=file.name,
                name_os=file.name,
                content=content_,
                content_cypher=t2n().convert_to_cypher(content_),
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
        else:
            return error

    def get_file_by_id(self, id) -> File:
        return File.objects.filter(id=id).first()

    def update_file(self, id_file, new_name_file, id_folder):
        file = self.get_file_by_id(id_file)
        error = {}
        if not file:
            error["id"] = ["File is not found"]
        if not error:
            if new_name_file:
                file.update_name(new_name_file)
        if id_folder:
            if Folder.objects.filter(id=id_folder).first():
                if file:
                    file.update_idFolder(Folder.objects.filter(id=id_folder).first())
            else:
                error["id_folder"] = ["Folder is not found"]
        if not error:
            file.save()
            return file
        return error

    def delete_file(self, id_file):
        file = self.get_file_by_id(id_file)

        error = {}
        if not file:
            error["id"] = ["File is not found"]
        if not error:
            file.delete()
            return file
        return error

    def view_file_by_id(self, id_file) -> Dict:
        file = self.get_file_by_id(id_file)
        error = {}
        if not file:
            error["id"] = ["File is not found"]
        if not error:
            folder = Folder.objects.filter(id=file.id_folder.id).first()

            data = {"file": file, "folder": folder.name}
            return data
        else:
            return error

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
