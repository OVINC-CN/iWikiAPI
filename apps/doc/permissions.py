from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from apps.doc.models import Doc


class DocOwnerPermission(BasePermission):
    """
    Owner Permission
    """

    def has_permission(self, request: Request, view: GenericViewSet):
        return True

    def has_object_permission(self, request: Request, view: GenericViewSet, obj: Doc):
        # Retrieve Public Inst is Allowed
        if view.action == "retrieve" and obj.is_public:
            return True
        # Check Owner
        return obj.owner == request.user
