from ..models import Folder, File
from typing import Dict, List

class FileRepository:
    def add_file(self,file,folder) -> File:
        folder = Folder.objects.filter(id = folder.id).first()
        if not folder:
            raise ValueError("Not folder {} is found".format(folder.id))
        if file.content_type == 'text/plain':
            file_content = file.read().decode('utf-8')  # Đọc file và giải mã nó thành chuỗi văn bản
        else:
            raise ValueError("only txt file")
        newFile = File(
            id_folder = folder,
            file = file,
            name = file.name,
            content = file_content
        )
        newFile.save()
        return newFile
    
    @staticmethod
    def view_file_by_id(id_file) -> Dict:
        file = File.objects.filter(id=id_file).first()
        if not file:
            raise ValueError("File is not found")
        folder = Folder.objects.filter(id=file.id_folder.id).first()
        
        data = {
            'file': file,
            'folder': folder.name
        }
        return data
    
    @staticmethod
    def find_file_by_name(search_name) -> List[File]:
        result_files = File.objects.filter(name__icontains=search_name)
        return result_files
        
