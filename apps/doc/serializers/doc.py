from typing import List

from adrf.serializers import ModelSerializer, Serializer
from django.utils.translation import gettext_lazy
from ovinc_client.core.constants import SHORT_CHAR_LENGTH
from rest_framework import serializers

from apps.doc.models import Doc
from apps.doc.serializers.tag import TagInfoSerializer


class DocListSerializer(ModelSerializer):
    """
    Doc List
    """

    class TagsSerializerField(serializers.SerializerMethodField):
        async def ato_representation(self, val):
            return super().to_representation(val)

    owner_nick_name = serializers.CharField(
        label=gettext_lazy("Owner Nick Name"), read_only=True, source="owner.nick_name"
    )
    comments = serializers.IntegerField(label=gettext_lazy("Comment Count"), read_only=True, source="comment_set.count")
    tags = TagsSerializerField(label=gettext_lazy("Tags"), read_only=True)
    owner = serializers.CharField(label=gettext_lazy("Owner"), read_only=True)

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


class EditDocSerializer(ModelSerializer):
    """
    Edit Doc
    """

    title = serializers.CharField(label=gettext_lazy("Title"), max_length=SHORT_CHAR_LENGTH)
    header_img = serializers.URLField(label=gettext_lazy("Header Image"), allow_blank=True, allow_null=True)
    is_public = serializers.BooleanField(label=gettext_lazy("Is Public"))
    tags = serializers.ListField(label=gettext_lazy("Tags"), child=serializers.CharField(max_length=SHORT_CHAR_LENGTH))
    created_at = serializers.DateTimeField(label=gettext_lazy("Created Time"), required=False)

    class Meta:
        model = Doc
        fields = ["title", "content", "header_img", "is_public", "tags", "created_at"]


class DocSearchSerializer(Serializer):
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
    keywords = serializers.ListField(
        label=gettext_lazy("Keywords"),
        required=False,
        allow_null=True,
        allow_empty=True,
        child=serializers.CharField(max_length=SHORT_CHAR_LENGTH),
    )

    def to_internal_value(self, data):
        data = data.dict()
        if "tags" in data:
            data["tags"] = [t for t in data["tags"].split(",") if t]
        if "keywords" in data:
            data["keywords"] = [k for k in data["keywords"].split(",") if k]
        return super().to_internal_value(data)
