from rest_framework.response import Response
from rest_framework import status


class ResponseSuccess:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResponseSuccess, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.data = {}
        self.message = []
        self.status = status.HTTP_200_OK

    def set_response(self, data=None, message=None, status=status.HTTP_200_OK):
        self.data = data if data is not None else {}
        self.message = message if message is not None else []
        self.status = status
        return self

    def __call__(self) -> Response:
        return Response(
            {"data": self.data, "messages": self.message, "status": self.status},
            status=self.status,
        )
