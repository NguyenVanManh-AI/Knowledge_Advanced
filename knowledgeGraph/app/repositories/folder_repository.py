from ..models.folder_model import Folder
from typing import List


class FolderRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FolderRepository, cls).__new__(cls)
        return cls._instance

    def add_folder(self, folder: Folder):
        try:
            folder = Folder(name=folder.name, id_parent=folder.id_parent)
            folder.save()
            return folder
        except Exception as e:
            return e

    def get_folder_by_id(self, id_folder) -> Folder:
        return Folder.objects.filter(id=id_folder).first()

    def update_folder(self, folder: Folder, builder: Folder):
        try:
            folder.update_name(builder.name)
            folder.update_idParent(builder.id_parent)
        except Exception as e:
            return e

    def delete_folder(self, folder) -> Folder:
        try:
            folder.delete()
            return folder
        except Exception as e:
            return e

    def find_folder_by_name(self, search_name: str) -> List[Folder]:
        result_folders = Folder.objects.filter(name__icontains=search_name)
        return result_folders

    def get_all_folder(self) -> List[Folder]:
        return list(Folder.objects.all())

    def get_tree(self) -> List:
        root_folders = Folder.objects.filter(id_parent__isnull=True)
        folder_tree = [folder.get_tree() for folder in root_folders]
        return folder_tree
