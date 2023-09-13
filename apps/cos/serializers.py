from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext
from rest_framework import serializers


class UploadFileSerializer(serializers.Serializer):
    """
    File
    """

    file = serializers.FileField()

    def validate_file(self, file: InMemoryUploadedFile) -> InMemoryUploadedFile:
        if file.size > settings.QCLOUD_COS_UPLOAD_MAX_SIZE:
            raise serializers.ValidationError(gettext("File Size Too Large"))
        return file
