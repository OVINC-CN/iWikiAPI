from asgiref.sync import sync_to_async
from ovinc_client.core.auth import SessionAuthenticate
from ovinc_client.core.viewsets import ListMixin, MainViewSet
from rest_framework.response import Response

from apps.permission.models import UserPermission
from apps.permission.serializers import UserPermissionListSerializer


class UserPermissionViewSet(ListMixin, MainViewSet):
    """
    User Permission
    """

    queryset = UserPermission.objects.all()
    authentication_classes = [SessionAuthenticate]

    async def list(self, request, *args, **kwargs):
        """
        List Current User Permissions
        """

        queryset = await sync_to_async(UserPermission.load_permissions)(request.user)
        serializer = UserPermissionListSerializer(queryset, many=True)
        return Response(await serializer.adata)
