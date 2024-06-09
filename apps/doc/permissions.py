from asgiref.sync import sync_to_async
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from apps.doc.models import Doc
from apps.permission.constants import PermissionItem
from apps.permission.models import UserPermission


class DocOwnerPermission(BasePermission):
    """
    Owner Permission
    """

    async def has_permission(self, request: Request, view: GenericViewSet):
        return True

    async def has_object_permission(self, request: Request, view: GenericViewSet, obj: Doc):
        return await sync_to_async(self._has_object_permission)(request, view, obj)

    def _has_object_permission(self, request: Request, view: GenericViewSet, obj: Doc):
        # Retrieve Public Inst is Allowed
        if view.action == "retrieve" and obj.is_public:
            return True
        # Check Owner
        return obj.owner == request.user


class CreateDocPermission(BasePermission):
    """
    Create Doc Permission
    """

    async def has_permission(self, request, view):
        return await sync_to_async(UserPermission.check_permission)(
            user=request.user, permission_item=PermissionItem.CREATE_DOC
        )
