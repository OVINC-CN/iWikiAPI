from django.utils.translation import gettext_lazy
from rest_framework import status
from rest_framework.exceptions import APIException


class UploadFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = gettext_lazy("Upload Failed")
