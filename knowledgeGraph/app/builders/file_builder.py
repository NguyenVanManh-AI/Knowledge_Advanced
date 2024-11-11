from ..models.file_model import File


class FileBuilder:
    def __init__(self):
        self.folder = None
        self.file = None

    def setFolder(self, folder):
        self.folder = folder
        return self

    def setFile(self, file):
        self.file = file
        return self

    def build(self):
        return File(
            id_folder=self.folder,
            name=self.file.name,
            name_os=self.file.name,
        )
