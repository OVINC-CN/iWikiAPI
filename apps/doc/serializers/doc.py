from typing import List

from django.utils.translation import gettext_lazy
from ovinc_client.core.constants import SHORT_CHAR_LENGTH
from rest_framework import serializers

from apps.doc.models import Doc
from apps.doc.serializers.tag import TagInfoSerializer


class DocListSerializer(serializers.ModelSerializer):
    """
    Doc List
    """

    owner_nick_name = serializers.CharField(
        label=gettext_lazy("Owner Nick Name"), read_only=True, source="owner.nick_name"
    )
    comments = serializers.IntegerField(label=gettext_lazy("Comment Count"), read_only=True, source="comment_set.count")
    tags = serializers.SerializerMethodField(label=gettext_lazy("Tags"), read_only=True)

    class Meta:
        model = Doc
        exclude = ["content"]

    def get_tags(self, instance: Doc) -> List[dict]:
        tags = [TagInfoSerializer(instance=dt.tag).data["name"] for dt in instance.doctag_set.all()]
        tags.sort()
        return tags


class DocInfoSerializer(DocListSerializer):
    """
    Doc Info
    """

    class Meta:
        model = Doc
        fields = "__all__"


class EditDocSerializer(serializers.ModelSerializer):
    """
    Edit Doc
    """

    title = serializers.CharField(label=gettext_lazy("Title"), max_length=SHORT_CHAR_LENGTH)
    header_img = serializers.URLField(label=gettext_lazy("Header Image"))
    is_public = serializers.BooleanField(label=gettext_lazy("Is Public"))
    tags = serializers.ListField(label=gettext_lazy("Tags"), child=serializers.CharField(max_length=SHORT_CHAR_LENGTH))
    created_at = serializers.DateTimeField(label=gettext_lazy("Created Time"), required=False)

    class Meta:
        model = Doc
        fields = ["title", "content", "header_img", "is_public", "tags", "created_at"]


class DocSearchSerializer(serializers.Serializer):
    """
    Search Doc
    """

    tags = serializers.ListField(
        label=gettext_lazy("Tags"),
        required=False,
        allow_null=True,
        allow_empty=True,
        child=serializers.CharField(max_length=SHORT_CHAR_LENGTH),
    )

    def to_internal_value(self, data):
        data = data.dict()
        if "tags" in data:
            data["tags"] = [t for t in data["tags"].split(",") if t]
        return super().to_internal_value(data)
