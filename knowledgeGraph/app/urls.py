from django.urls import path
from .api_views.ApiFolderView import *

urlpatterns = [
    path('folder/', FolderListView.as_view(), name='folder-list'),            
    path('folder/add/', FolderCreateView.as_view(), name='folder-add'),     
    path('folder/update/', FolderUpdateView.as_view(), name='folder-update'),  
    path('folder/delete/', FolderDeleteView.as_view(), name='folder-delete'),  
]