from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    @staticmethod
    def success(message, data=None, status_code=status.HTTP_200_OK):
        response_data = {"message": message}
        response_data["status_code"] = status_code
        response_data["success"] = True
        if data is not None:
            response_data["data"] = data

        return Response(response_data, status=status_code)

    @staticmethod
    def error(message, data=None, status_code=status.HTTP_400_BAD_REQUEST):
        response_data = {"message": message}
        response_data["data"] = {}
        response_data["success"] = False
        response_data["status_code"] = status_code
        if data is not None:
            response_data["data"] = data

        return Response(response_data, status=status_code)
