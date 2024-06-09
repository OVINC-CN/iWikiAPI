from asgiref.sync import sync_to_async
from rest_framework.permissions import BasePermission

from apps.permission.constants import PermissionItem
from apps.permission.models import UserPermission


class UploadFilePermission(BasePermission):
    """
    Upload File Permission
    """

    async def has_permission(self, request, view):
        return await sync_to_async(UserPermission.check_permission)(
            user=request.user, permission_item=PermissionItem.UPLOAD_FILE
        )
