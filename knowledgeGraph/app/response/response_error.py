from rest_framework.response import Response
from rest_framework import status


class ResponseError:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResponseError, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.error = {}
        self.message = []
        self.status = status.HTTP_400_BAD_REQUEST
    
    def set_response(self, error=None, message=None, status=status.HTTP_400_BAD_REQUEST):
        self.error = error if error is not None else {}
        self.message = message if message is not None else []
        self.status = status 
        return self

    def __call__(self) -> Response:
        return Response(
            {"errors": self.error, "messages": self.message, "status": self.status},
            status=self.status,
        )
