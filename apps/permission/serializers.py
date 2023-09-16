from rest_framework import serializers

from apps.permission.models import UserPermission


class UserPermissionListSerializer(serializers.ModelSerializer):
    """
    User Permission
    """

    class Meta:
        model = UserPermission
        fields = ["permission_item", "expired_at"]
