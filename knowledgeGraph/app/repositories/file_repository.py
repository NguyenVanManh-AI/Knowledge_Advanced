from ..models import Folder, File
from typing import Dict, List

class FileRepository:
    def add_file(self,file,folder) -> File:
        folder = Folder.objects.filter(id = folder.id).first()
        if not folder:
            raise ValueError("Not folder {} is found".format(folder.id))
        if file.content_type == 'text/plain':
            file_content = file.read().decode('utf-8')  
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
    
    def get_file_by_id(self,id) -> File:
        return File.objects.filter(id=id).first()
    
    def update_name_file(self,id_file,new_name_file) -> File:
        file = self.get_file_by_id(id_file)
        if not file:
            return None
        file.update_name(new_name_file)
        file.save()
        return file
    
    def delete_file(self,id_file) -> File:
        file = self.get_file_by_id(id_file)
        if not file:
            return None
        file.delete()
        return file
        
    
    def view_file_by_id(self,id_file) -> Dict:
        file = self.get_file_by_id(id_file)
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
        
