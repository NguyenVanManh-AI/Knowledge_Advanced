from ..models.folder_model import Folder


class FolderBuilder:
    def __init__(self):
        self.name = None
        self.parent = None

    def setName(self, name):
        self.name = name
        return self

    def setParent(self, parent):
        self.parent = parent
        return self

    def build(self):
        return Folder(name=self.name, id_parent=self.parent)
