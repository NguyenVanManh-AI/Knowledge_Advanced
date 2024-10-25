from ..models import Folder
from typing import List


class FolderRepository:
    def add_folder(self, new_name, id_parent) -> Folder:
        if id_parent:
            folder = Folder(
                name=new_name, id_parent=self.get_folder_by_id(id_parent.id)
            )
            if id_parent == folder.id:
                return None
        else:
            folder = Folder(name=new_name)
        folder.save()
        return folder

    def get_folder_by_id(self, id_folder) -> Folder:
        return Folder.objects.filter(id=id_folder).first()

    def update_folder(self, id_folder, new_name_folder, id_parent) -> Folder:
        folder = self.get_folder_by_id(id_folder)
        if not folder:
            return None

        # Chỉ kiểm tra nếu id_parent không phải None
        if id_parent is not None and int(folder.id) == int(id_parent):
            return None

        if new_name_folder:
            folder.update_name(new_name_folder)
        
        # Kiểm tra nếu id_parent không phải None trước khi cập nhật
        if id_parent is not None:
            parent_folder = Folder.objects.filter(id=id_parent).first()
            if parent_folder:
                folder.update_idParent(parent_folder)
            else:
                return None

        folder.save()
        return folder

    def delete_folder(self, id_folder) -> Folder:
        folder = self.get_folder_by_id(id_folder)

        if folder:
            folder.delete()
        return folder

    @staticmethod
    def find_folder_by_name(search_name: str) -> List[Folder]:
        result_folders = Folder.objects.filter(name__icontains=search_name)
        return result_folders

    @staticmethod
    def get_all_folder() -> List[Folder]:
        return list(Folder.objects.all())

    @staticmethod
    def get_tree() -> List:
        root_folders = Folder.objects.filter(id_parent__isnull=True)
        folder_tree = [folder.get_tree() for folder in root_folders]
        return folder_tree
