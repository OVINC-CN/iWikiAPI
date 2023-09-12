from ovinc_client.core.viewsets import CreateMixin, MainViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.cos.client import Client
from apps.cos.models import COSLog
from apps.cos.serializers import UploadFileSerializer


class COSViewSet(CreateMixin, MainViewSet):
    """
    COS
    """

    queryset = COSLog.objects.all()

    @action(methods=["POST"], detail=False)
    def upload(self, request: Request, *args, **kwargs):
        """
        Upload File
        """

        # Validate
        serializer = UploadFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]

        # Upload
        client = Client(user=request.user)
        resp = client.upload(file)

        # Response
        return Response({"name": file.name, "url": resp})
