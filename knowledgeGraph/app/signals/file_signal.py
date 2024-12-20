from django.db.models.signals import post_delete
from django.dispatch import receiver
from ..models.file_model import File
from django.conf import settings
from ..Module_Final.class_text2neo4j import Text2Neo4j as t2n
import os

@receiver(post_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    print("receive delete file")
    if instance.name_os is None:
        name = instance.name
    else :
        name = instance.name_os 
    file_path = os.path.join(settings.BASE_DIR, "media","uploads", name)
    print("delete path", file_path)
    if instance.content_cypher:
        t2n().del_to_neo4j(instance.content_cypher)
    else:
        print("File have not cypher")
    if os.path.isfile(file_path):
        print("delete file system")
        os.remove(file_path)