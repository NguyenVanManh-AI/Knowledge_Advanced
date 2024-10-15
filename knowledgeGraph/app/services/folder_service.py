from typing import List, Dict
from django.core.paginator import Paginator
from ..repositories.folder_repository import FolderRepository
from ..models import Folder

class FolderService:
    def __init__(self):
        self.repository = FolderRepository()
    
    def addFolder(self,name):
        return self.repository.add_folder(name)
    
    def updateNameFolder(self,idFolder,newNameFolder):
        return self.repository.update_name_folder(idFolder,newNameFolder)
    
    def deleteFolder(self,idFolder):
        return self.repository.delete_folder(idFolder)
    
    @staticmethod
    def findFolderByName(search_name: str, page: int, num_item: int = 20) -> Dict:
        folders = FolderRepository.find_folder_by_name(search_name=search_name)
        paginator = Paginator(folders, num_item)
        
        page = paginator.get_page(page)
        return {
            'folders': page.object_list,
            'total_pages': paginator.num_pages,
            'current_page': page.number,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
        }
        
    @staticmethod
    def getAllFolder() -> List[Folder]:
        return [folder for folder in FolderRepository.get_all_folder()]