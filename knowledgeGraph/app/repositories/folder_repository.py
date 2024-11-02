from ..models import Folder
from typing import List


class FolderRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FolderRepository, cls).__new__(cls)
        return cls._instance

    def add_folder(self, new_name, id_parent):
        error = {}
        print("name", new_name)
        print("id_parent", id_parent)
        if new_name is None:
            error["name"] = ["Field name is required"]
        if error:
            return error

        if not new_name:
            error["name"] = ["name is not empty"]

        if id_parent is None and not error:
            folder = Folder(name=new_name)
            folder.save()
            return folder

        if not id_parent:
            error["id_parent"] = ["id_parent is not empty"]
            return error

        if self.get_folder_by_id(id_parent) is None:
            error["id_parent"] = ["id parent is not found"]
            return error

        folder = Folder(name=new_name, id_parent=self.get_folder_by_id(id_parent))
        folder.save()
        return folder

    def get_folder_by_id(self, id_folder) -> Folder:
        return Folder.objects.filter(id=id_folder).first()

    def update_folder(self, id_folder, new_name_folder, id_parent):
        folder = self.get_folder_by_id(id_folder)
        error = {}
        if not folder:
            error["id"] = ["Folder is not found"]
        if id_parent is not None:

            if int(id_folder) == int(id_parent):
                error.setdefault("id", []).append("Child is not same parent")
                error["id_parent"] = ["Parent is not same child"]

            parent_folder = self.get_folder_by_id(id_parent)
            if not parent_folder:
                error.setdefault("id_parent", []).append("Parent is not found")
            elif not error:
                folder.update_idParent(parent_folder)

        if folder:
            if new_name_folder:
                folder.update_name(new_name_folder)
        if not error:
            folder.save()
            return folder
        return error

    def delete_folder(self, id_folder) -> Folder:
        folder = self.get_folder_by_id(id_folder)
        error = {}
        if not folder:
            error["id"] = ["id folder is not found"]
        if not error:
            folder.delete()
            return folder
        return error

    def find_folder_by_name(self, search_name: str) -> List[Folder]:
        result_folders = Folder.objects.filter(name__icontains=search_name)
        return result_folders

    def get_all_folder(self) -> List[Folder]:
        return list(Folder.objects.all())

    def get_tree(self) -> List:
        root_folders = Folder.objects.filter(id_parent__isnull=True)
        folder_tree = [folder.get_tree() for folder in root_folders]
        return folder_tree
