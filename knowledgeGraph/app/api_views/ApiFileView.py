from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.file_service import FileService
from ..serializers import FileSerializer


class FileCreateView(APIView):
    def post(self, request):
        data = request.data.copy()
        file = request.FILES.get('file')
        data['file'] = file
        data['name'] = file.name
        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            file = FileService().addFile(
                serializer.validated_data['file'],
                serializer.validated_data['id_folder']
            )
            return Response(
                FileSerializer(file).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

class FileInforView(APIView):
    def get(self,request):
        search = request.data.get('search')
        page = request.data.get('page')
        if search and page :
            files = FileService.findFileByName(search,page)
            if not files['files']:
                return Response(
                    {
                        "error": "No folders found matching the search criteria."
                    }, 
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = FileSerializer(files['files'],many = True)
            return Response(
                {
                'files': serializer.data,
                'total_pages': files['total_pages'],
                'current_page': files['current_page'],
                'has_next': files['has_next'],
                'has_previous': files['has_previous'],
                },
                status=status.HTTP_200_OK
            )
            
        id = request.data.get('id')
        print("id",id)
        file_data = FileService().viewFileById(id)
        serializer = FileSerializer(file_data['file'])
        return Response(
            {
                "file" : serializer.data,
                "folder" : file_data['folder']
            },
            status=status.HTTP_200_OK
        )

class FileUpdateView(APIView):
    def put(self,request):
        name = request.data.get('name')
        id = request.data.get('id')
        update_file = FileService().updateNameFile(
                id,
                name
            )
        if not update_file:
                return Response(
                    {
                        "error":"File is not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {
                "message":"Update success"
            }, 
            status=status.HTTP_200_OK
        )
       
class FileDeleteView(APIView):
    def delete(self,request):
        deleted = FileService().deleteFile(request.data.get('id'))
        if not deleted:
            return Response(
                {
                    "error": "File is not found."
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "message":"Delete success"
            },
            status=status.HTTP_204_NO_CONTENT
        )