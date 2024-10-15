from ..repositories.file_repository import FileRepository
from django.core.paginator import Paginator
from ..models import File
from typing import Dict

class FileService:
    def __init__(self):
        self.fileReposiroty = FileRepository()
    
    def addFile(self,file,folder):
        return self.fileReposiroty.add_file(file,folder)
    
    def updateNameFile(self,id_file,new_name_file):
        return self.fileReposiroty.update_name_file(id_file,new_name_file)
    
    def deleteFile(self,id_file):
        return self.fileReposiroty.delete_file(id_file)
    
    def viewFileById(self,id_file):
        return self.fileReposiroty.view_file_by_id(id_file)
    
    @staticmethod
    def findFileByName(id_folder,search,page,num_item = 20) -> Dict:
        files = FileRepository.find_file_by_name(id_folder,search)
        paginator = Paginator(files, num_item)
        
        page = paginator.get_page(page)
        return {
            'files': page.object_list,
            'total_pages': paginator.num_pages,
            'current_page': page.number,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
        }
        