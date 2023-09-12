from rest_framework import serializers

from apps.doc.models import Tag


class TagInfoSerializer(serializers.ModelSerializer):
    """
    Tag Info
    """

    class Meta:
        model = Tag
        fields = ["id", "name"]
