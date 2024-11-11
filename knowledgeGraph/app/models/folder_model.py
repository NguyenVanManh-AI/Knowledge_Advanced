from django.db import models


class Folder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    id_parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )

    def update_name(self, new_name):
        self.name = new_name
        self.save()

    def update_idParent(self, id_parent):
        self.id_parent = id_parent
        self.save()

    def get_tree(self):
        children = [child.get_tree() for child in self.children.all()]
        files = list(self.files.values("name", "src"))

        return {"folder": self.name, "file": files, "children": children}

    def __str__(self):
        return self.name
