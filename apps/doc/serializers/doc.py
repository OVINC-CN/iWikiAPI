from typing import List

from django.utils.translation import gettext_lazy
from ovinc_client.core.constants import SHORT_CHAR_LENGTH
from rest_framework import serializers

from apps.doc.models import Doc
from apps.doc.serializers.tag import TagInfoSerializer


class DocInfoSerializer(serializers.ModelSerializer):
    """
    Doc Info
    """

    class Meta:
        model = Doc
        fields = "__all__"


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
        return [TagInfoSerializer(instance=tag.tag).data for tag in instance.doctag_set.all()]


class EditDocSerializer(serializers.ModelSerializer):
    """
    Edit Doc
    """

    title = serializers.CharField(label=gettext_lazy("Title"), max_length=SHORT_CHAR_LENGTH)
    header_img = serializers.URLField(label=gettext_lazy("Header Image"))
    is_public = serializers.BooleanField(label=gettext_lazy("Is Public"))
    tags = serializers.ListField(label=gettext_lazy("Tags"), child=serializers.CharField(max_length=SHORT_CHAR_LENGTH))

    class Meta:
        model = Doc
        fields = ["title", "content", "header_img", "is_public", "tags"]
