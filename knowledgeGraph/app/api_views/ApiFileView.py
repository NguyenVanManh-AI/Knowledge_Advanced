from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..services.file_service import FileService
from ..serializers import FileSerializer
from ..response.response_success import ResponseSuccess
from ..response.response_error import ResponseError


class FileCreateView(APIView):
    def post(self, request):
        try:
            id_folder = request.data.get("id_folder")
            file = request.FILES.get("file")
            file = FileService().addFile(file, id_folder)
            if isinstance(file, dict):
                return ResponseError().set_response(
                    error=file, message=[e for values in file.values() for e in values]
                )()
            if isinstance(file, Exception):
                return ResponseError().set_response(
                    message=[str(file)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )()
            return ResponseSuccess().set_response(
                data=FileSerializer(file).data, message=["Create file success"]
            )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class FileInforView(APIView):
    def post(self, request):
        search = request.data.get("search")
        page = request.data.get("page")
        id_folder = request.data.get("id_folder")
        per_page = request.data.get("per_page")
        order_by = request.data.get("order_by", "id")  # Mặc định là 'id' nếu không có
        order_direction = request.data.get(
            "order_direction", "asc"
        )  # Mặc định là 'asc' nếu không có
        # search = request.query_params.get('search')
        # page = request.query_params.get('page')
        # id_folder = request.query_params.get('id_folder')
        try:
            if search != None and page != None:
                files = FileService().findFileByName(
                    id_folder, search, page, per_page, order_by, order_direction
                )
                # if not files['files']:
                #     return Response(
                #         {
                #             "error": "No file found matching the search criteria."
                #         },
                #         status=status.HTTP_404_NOT_FOUND
                #     )
                serializer = FileSerializer(files["files"], many=True)
                return ResponseSuccess().set_response(
                    data={
                        "files": serializer.data,
                        "total_pages": files["total_pages"],
                        "current_page": files["current_page"],
                        "has_next": files["has_next"],
                        "has_previous": files["has_previous"],
                        "total": files["total"],
                    },
                    message=["Find file success"],
                )()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()
            # id = request.query_params.get('id')
        id = request.data.get("id")
        try:
            if id != None:
                file_data = FileService().viewFileById(id)
                if "id" in file_data.keys():
                    return ResponseError().set_response(
                        error=file_data, message=file_data["id"]
                    )()
                serializer = FileSerializer(file_data["file"])
                return ResponseSuccess().set_response(
                    data={"file": serializer.data, "folder": file_data["folder"]},
                    message=["Get id file success"],
                )()
            return ResponseError().set_response(message=["Bad request"])()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class FileUpdateView(APIView):
    def put(self, request):
        name = request.data.get("name")
        id = request.data.get("id")
        id_folder = request.data.get("id_folder")
        try:
            update_file = FileService().updateFile(id, name, id_folder)
            if isinstance(update_file, dict):
                return ResponseError().set_response(
                    error=update_file,
                    message=[value[0] for value in update_file.values()],
                )()
            return ResponseSuccess().set_response(message=["Update file success"])()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class FileDeleteView(APIView):
    def delete(self, request):
        try:
            deleted = FileService().deleteFile(request.query_params.get("id"))
            if isinstance(deleted, dict):
                return ResponseError().set_response(
                    error=deleted, message=[deleted["id"]]
                )()
            return ResponseSuccess().set_response(message=["Updated success"])()
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()


class FileDownloadView(APIView):
    def get(self, request):
        id_file = request.GET.get("id")
        try:
            path = FileService().download_file(id_file)
            print("path os api view", path)
            if isinstance(path, dict):
                return ResponseError().set_response(error=path)()
            response = FileResponse(open(path, "rb"), as_attachment=True)
            return response
        except Exception as e:
            return ResponseError().set_response(
                message=[str(e)], status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )()
