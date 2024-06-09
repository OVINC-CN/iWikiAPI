from channels.db import database_sync_to_async
from django.db.models import QuerySet
from ovinc_client.core.auth import SessionAuthenticate
from ovinc_client.core.viewsets import ListMixin, MainViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.doc.models import DocTag, Tag
from apps.doc.serializers.tag import TagInfoSerializer


class TagViewSet(ListMixin, MainViewSet):
    """
    Tag
    """

    queryset = Tag.objects.all()
    authentication_classes = [SessionAuthenticate]

    async def list(self, request: Request, *args, **kwargs):
        """
        Tag List
        """

        tags = await database_sync_to_async(self.list_tags)()
        serializer = TagInfoSerializer(instance=tags, many=True)
        return Response(data=await serializer.adata)

    def list_tags(self) -> QuerySet:
        return Tag.objects.all().order_by("name")

    @action(methods=["GET"], detail=False)
    async def bound(self, request: Request, *args, **kwargs):
        """
        Bound Tags
        """

        tags = await database_sync_to_async(self.filter_tags)()
        serializer = TagInfoSerializer(instance=tags, many=True)
        return Response(data=await serializer.adata)

    def filter_tags(self) -> QuerySet:
        return Tag.objects.filter(id__in=DocTag.objects.all().values("tag_id")).order_by("name")
