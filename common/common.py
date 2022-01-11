from rest_framework import status
from rest_framework.exceptions import APIException,AuthenticationFailed


class ValidationErrorFailed(APIException):
    status_code = status.HTTP_200_OK

    def __init__(self, detail):
        self.detail = detail