from ..repositories.file_repository import FileRepository
from django.core.paginator import Paginator
from ..models import File
from typing import Dict

class FileService:
    def __init__(self):
        self.fileReposiroty = FileRepository()
    
    def addFile(self,file,folder):
        return self.fileReposiroty.add_file(file,folder)
    
    @staticmethod
    def viewFileById(id_file):
        return FileRepository.view_file_by_id(id_file)
    
    @staticmethod
    def findFileByName(search,page,num_item = 20) -> Dict:
        files = FileRepository.find_file_by_name(search)
        paginator = Paginator(files, num_item)
        
        page = paginator.get_page(page)
        return {
            'files': page.object_list,
            'total_pages': paginator.num_pages,
            'current_page': page.number,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
        }
        