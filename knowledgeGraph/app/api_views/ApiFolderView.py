from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.folder_service import FolderService
from ..serializers import FolderSerializer
from ..response.response_success import ResponseSuccess
from ..response.response_error import ResponseError


class FolderListView(APIView):
    def post(self, request):
        # search = request.data.get('search')
        # page = request.data.get('page')
        search = request.data.get("search")
        page = request.data.get("page")
        per_page = request.data.get("per_page")
        order_by = request.data.get("order_by", "id")  # Mặc định là 'id' nếu không có
        order_direction = request.data.get(
            "order_direction", "asc"
        )  # Mặc định là 'asc' nếu không có
        try:
            if page is not None:
                folders = FolderService().findFolderByName(
                    search, page, per_page, order_by, order_direction
                )
                serializer = FolderSerializer(folders["folders"], many=True)
                return ResponseSuccess().set_response(
                    data={
                        "folders": serializer.data,
                        "total_pages": folders["total_pages"],
                        "current_page": folders["current_page"],
                        "has_next": folders["has_next"],
                        "has_previous": folders["has_previous"],
                        "total": folders["total"],
                    },
                    message=["Find folder success"],
                )()
            folders = FolderService().getAllFolder()
            serializer = FolderSerializer(folders, many=True)
            return ResponseSuccess().set_response(
                data=serializer.data, message=["Get all follder success"]
            )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class FolderCreateView(APIView):
    def post(self, request):
        name = request.data.get("name")
        id_parent = request.data.get("id_parent")
        try:
            folder = FolderService().addFolder(
                name,
                id_parent,
            )
            if isinstance(folder, dict):
                return ResponseError().set_response(
                    error=folder,
                    message=[e for values in folder.values() for e in values],
                )()
            return ResponseSuccess().set_response(
                data=FolderSerializer(folder).data, message=["Created folder success"]
            )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class FolderUpdateView(APIView):
    def put(self, request):
        id = request.data.get("id")
        name = request.data.get("name")
        id_parent = request.data.get("id_parent")
        try:
            updated_folder = FolderService().updateFolder(id, name, id_parent)
            if isinstance(updated_folder, dict):
                return ResponseError().set_response(
                    error=updated_folder,
                    message=[e for values in updated_folder.values() for e in values],
                )()
            return ResponseSuccess().set_response(message=["Updated success"])()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class FolderDeleteView(APIView):
    def delete(self, request):
        try:
            deleted = FolderService().deleteFolder(request.query_params.get("id"))
            if isinstance(deleted, dict):
                return ResponseError().set_response(
                    error=deleted, message=deleted["id"]
                )()
            return ResponseSuccess().set_response(message=["Deleted success"])()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class FolderGetTree(APIView):
    def get(self, request):
        try:
            result = FolderService().getTree()
            print(result)
            return ResponseSuccess().set_response(
                data=result, message=["Get tree folder success"]
            )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()
