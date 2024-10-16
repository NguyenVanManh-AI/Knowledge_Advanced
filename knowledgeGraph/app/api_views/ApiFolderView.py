from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.folder_service import FolderService
from ..serializers import FolderSerializer

class FolderListView(APIView):
    def get(self, request):
        search = request.GET.get('search')
        page = request.GET.get('page')
        
        if search!=None and page!=None:
            folders = FolderService.findFolderByName(search, page)
            if not folders['folders']:
                return Response(
                    {"error": "No folders found matching the search criteria."}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = FolderSerializer(folders['folders'], many=True)  
            return Response(
                {
                'folders': serializer.data,
                'total_pages': folders['total_pages'],
                'current_page': folders['current_page'],
                'has_next': folders['has_next'],
                'has_previous': folders['has_previous'],
                'total': folders['total']
                },
                status=status.HTTP_200_OK
            )

        folders = FolderService.getAllFolder()
        serializer = FolderSerializer(folders, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
class FolderCreateView(APIView):
    def post(self, request):
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            folder = FolderService().addFolder(serializer.validated_data['name'])
            return Response(
                FolderSerializer(folder).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
class FolderUpdateView(APIView):
    def put(self, request):
        id = request.data.get("id")
        name = request.data.get("name")
        updated_folder = FolderService().updateNameFolder(
            id,
            name
        )
        if not updated_folder:
            return Response(
                {
                    "error":"Folder is not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "message":"Update success"
            }, 
            status=status.HTTP_200_OK
        )
class FolderDeleteView(APIView):
    def delete(self, request):
        deleted = FolderService().deleteFolder(request.data.get('id'))
        if not deleted:
            return Response(
                {
                    "error": "Folder is not found."
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "message","Delete success"
            },
            status=status.HTTP_204_NO_CONTENT
        )

    