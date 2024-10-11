from ..models import Folder, File
from django.db.models import QuerySet
from typing import List

class FolderRepository:
    def add_folder(self,new_name)  -> Folder:
        folder = Folder(name = new_name)
        folder.save()
        return folder
    
    def get_folder_by_id(self,id_folder) -> Folder:
        return Folder.objects.filter(id=id_folder).first()
    
    def update_name_folder(self,id_folder,new_name_folder) -> Folder:
        folder = self.get_folder_by_id(id_folder)
        if not folder :
            return None
        folder.update_name(new_name_folder)
        folder.save()
        return folder
    
    def delete_folder(self,id_folder) -> Folder:
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
             
    
    