from django.urls import path, include
from .views.folder_view import *
from .views.user_view import *
from .views.chatbot_view import *
from .views.file_view import *
from rest_framework_simplejwt.views import TokenRefreshView

# from .views import chatbot, cypher
# from .views import get_chats, logout, CustomTokenObitanPairView, CustomRefreshTokenView, is_authenticated, register, ChatViewSet

urlpatterns = [
    path("folder/", FolderListView.as_view(), name="folder-list"),
    path("folder/add/", FolderCreateView.as_view(), name="folder-add"),
    path("folder/update/", FolderUpdateView.as_view(), name="folder-update"),
    path("folder/delete/", FolderDeleteView.as_view(), name="folder-delete"),
    path("folder/tree", FolderGetTree.as_view(), name="folder-get-tree"),
    
    path("file/", FileInforView.as_view(), name="file-list"),
    path("file/add/", FileCreateView.as_view(), name="file-add"),
    path("file/update/", FileUpdateView.as_view(), name="file-update"),
    path("file/delete/", FileDeleteView.as_view(), name="file-delete"),
    path("file/download/", FileDownloadView.as_view(), name="file-download"),
    
    path("chatbot/", ChatbotAnswerView.as_view(), name="chatbot-answer"),
    path("chatbot/history/",ChatbotHistoryView.as_view(), name="chatbot-history"),
    path("chatbot/create_new/", ChatViewSet.as_view({"post": "create","get": "list"}), name="chatbot-create-new"),
    
    
    path("user/register/", RegisterView.as_view(), name="user-register"),
    path("user/login/", LoginView.as_view(), name="user-login"),
    path("user/profile/", UserProfileView.as_view(), name="user-profile"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="user-token_refresh"),
]
