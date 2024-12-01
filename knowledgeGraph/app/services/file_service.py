from ..repositories.repository_factory import RepositoryFactory
# from ..repositories.file_repository import FileRepository
from django.core.paginator import Paginator
from ..models.file_model import File
from ..models.folder_model import Folder
# from ..repositories.folder_repository import FolderRepository as fr
from ..builders.file_builder import FileBuilder as fb
from typing import Dict
from django.conf import settings
from ..Module_Final.class_text2neo4j import Text2Neo4j as t2n


class FileService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "repositoryFactory"):
            self.repositoryFactory = RepositoryFactory()

    def addFile(self, file, id_folder):
        error = {}
        print("id_folder", id_folder)
        print("file", file)
        if id_folder is None:
            error.setdefault("id_folder", []).append("Field id_folder is required")
        elif not id_folder:
            error.setdefault("id_folder", []).append("id_folder is not empty")
        if not file:
            error.setdefault("file", []).append("Field file is required")
        elif not file.name.endswith(".txt"):
            error.setdefault("file", []).append("Format file is not support")
        if id_folder:
            folder = RepositoryFactory.create("folder").get_folder_by_id(id_folder)
            if not folder:
                error.setdefault("id_folder", []).append("Folder not found")

        if error:
            return error

        file_builder = fb().setFolder(folder).setFile(file).build()
        file_content = file.read()
        content_struct = t2n().gen_structure_data(file_content.decode("utf-8"))
        content_cypher = t2n().convert_to_cypher(content_struct)
        return self.repositoryFactory.create("file").add_file(
            file_builder, file_content, content_struct, content_cypher
        )

    def updateFile(self, id_file, new_name_file, id_folder):
        error = {}
        if id_file is None:
            error.setdefault("id", []).append("Field id is required")
        elif not id_file:
            error.setdefault("id", []).append("id is not empty")
        if new_name_file is None:
            error.setdefault("name", []).append("Field name is required")
        elif not new_name_file:
            error.setdefault("name", []).append("name is not empty")
        if id_folder is None:
            pass
        elif not id_folder:
            error.setdefault("id_folder", []).append("id_folder is not empty")
        if id_file:
            file = self.repositoryFactory.create("file").get_file_by_id(id_file)
            if not file:
                error["id"] = ["File is not found"]
        if id_folder:
            folder = Folder.objects.filter(id=id_folder).first()
            if not folder:
                error["id_folder"] = ["Folder is not found"]
        if error:
            return error
        if new_name_file:
            self.repositoryFactory.create("file").update_name_file(file, new_name_file)
        if id_folder:
            if folder:
                self.repositoryFactory.create("file").update_folder(file, folder)

        return self.repositoryFactory.create("file").get_file_by_id(id_file)

    def deleteFile(self, id_file):
        error = {}
        print(id_file)
        if id_file is None:
            error["id"] = ["Param id is required"]
        elif not id_file:
            error["id"] = ["id is not empty"]
        if error:
            return error
        file = self.repositoryFactory.create("file").get_file_by_id(id_file)
        if not file:
            error["id"] = ["File is not found"]
        if error:
            return error
        return self.repositoryFactory.create("file").delete_file(file)

    def viewFileById(self, id_file):
        error = {}
        if id_file is None:
            error["id"] = ["Field id is required"]
        elif not id_file:
            error["id"] = ["id is not empty"]
        if error:
            return error
        file = self.repositoryFactory.create("file").get_file_by_id(id_file)
        if not file:
            error["id"] = ["File is not found"]
        if error:
            return error
        return self.repositoryFactory.create("file").view_file_by_id(file)

    def findFileByName(
        self,
        id_folder: int,
        search: str,
        page: int,
        num_item: int = 20,
        order_by: str = "id",
        order_direction: str = "asc",
    ) -> Dict:
        files = self.repositoryFactory.create("file").find_file_by_name(id_folder, search)

        if order_direction.lower() == "desc":
            files = files.order_by(f"-{order_by}")
        else:
            files = files.order_by(order_by)

        paginator = Paginator(files, num_item)
        page = paginator.get_page(page)
        return {
            "files": page.object_list,
            "total_pages": paginator.num_pages,
            "current_page": page.number,
            "has_next": page.has_next(),
            "has_previous": page.has_previous(),
            "total": len(files),
        }

    def download_file(self, id_file):
        return self.repositoryFactory.create("file").download_file(id_file)
