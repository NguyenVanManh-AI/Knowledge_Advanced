from typing import List, Dict
from django.core.paginator import Paginator
from copy import deepcopy  # Thư viện hỗ trợ sao chép sâu (deep copy)
from ..repositories.folder_repository import FolderRepository
from ..models.folder_model import Folder
from ..builders.folder_builder import FolderBuilder as fb


class FolderService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FolderService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "folderRepository"):
            self.folderRepository = FolderRepository()

    def clone(self) -> "FolderService":
        """
        Prototype pattern: Sao chép đối tượng FolderService.
        """
        return deepcopy(self)

    # Các phương thức khác không thay đổi
    def addFolder(self, name, id_parent):
        error = {}
        print("name", name)
        print("id_parent", id_parent)
        if name is None:
            error["name"] = ["Field name is required"]
        elif not name:
            error["name"] = ["name is not empty"]
        if id_parent is None:
            pass
        elif not id_parent:
            error["id_parent"] = ["id_parent is not empty"]
        if error:
            return error

        if id_parent is None:
            folder_builder = fb().setName(name).build()
        else:
            parent = self.folderRepository.get_folder_by_id(id_parent)
            if not parent:
                error["id_parent"] = ["Folder is not found"]
                return error
            folder_builder = fb().setName(name).setParent(parent).build()

        return self.folderRepository.add_folder(folder_builder)

    def updateFolder(self, idFolder, newNameFolder, id_parent):
        error = {}
        if idFolder is None:
            error["id_folder"] = ["Filed id_folder is required"]
        elif not idFolder:
            error["id_folder"] = ["id_folder is not empty"]
        if newNameFolder is None:
            error["name"] = ["Field name is not required"]
        elif not newNameFolder:
            error["name"] = ["name is not empty"]
        if idFolder and id_parent:
            if int(idFolder) == int(id_parent):
                error.setdefault("id", []).append("Child is not same parent")
                error.setdefault("id_parent", []).append("Parent is not same child")

        if idFolder:
            folder = self.folderRepository.get_folder_by_id(idFolder)
            if not folder:
                error.setdefault("id", []).append("Folder is not found")
        if id_parent:
            folder_parent = self.folderRepository.get_folder_by_id(id_parent)
            if not folder_parent:
                error.setdefault("id_parent", []).append("Folder is not found")

        if error:
            return error

        if id_parent is None:
            folder_builder = (
                fb().setName(newNameFolder).setParent(folder.id_parent).build()
            )
        elif not id_parent:
            folder_builder = fb().setName(newNameFolder).build()
        else:
            folder_builder = (
                fb().setName(newNameFolder).setParent(folder_parent).build()
            )

        return self.folderRepository.update_folder(folder, folder_builder)

    def deleteFolder(self, idFolder):
        error = {}
        print(idFolder)
        if idFolder is None:
            error["id"] = ["Param id is required"]
        elif not idFolder:
            error["id"] = ["id is not empty"]
        if error:
            return error
        folder = self.folderRepository.get_folder_by_id(idFolder)
        if not folder:
            error["id"] = ["Folder is not found"]
        if error:
            return error
        return self.folderRepository.delete_folder(folder)

    def findFolderByName(
        self,
        search_name: str,
        page: int,
        num_item: int = 20,
        order_by: str = "id",
        order_direction: str = "asc",
    ) -> Dict:
        folders = self.folderRepository.find_folder_by_name(search_name=search_name)

        if order_direction.lower() == "desc":
            folders = folders.order_by(f"-{order_by}")
        else:
            folders = folders.order_by(order_by)

        paginator = Paginator(folders, num_item)
        page = paginator.get_page(page)
        return {
            "folders": page.object_list,
            "total_pages": paginator.num_pages,
            "current_page": page.number,
            "has_next": page.has_next(),
            "has_previous": page.has_previous(),
            "total": len(folders),
        }

    def getAllFolder(self) -> List[Folder]:
        return [folder for folder in self.folderRepository.get_all_folder()]

    def getTree(self) -> List:
        return self.folderRepository.get_tree()
