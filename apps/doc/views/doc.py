from asgiref.sync import sync_to_async
from django.conf import settings
from django.db import transaction
from django.db.models import Q, QuerySet
from django.utils import timezone
from ovinc_client.core.auth import SessionAuthenticate
from ovinc_client.core.paginations import NumPagination
from ovinc_client.core.viewsets import (
    CreateMixin,
    DestroyMixin,
    ListMixin,
    MainViewSet,
    RetrieveMixin,
    UpdateMixin,
)
from rest_framework.request import Request
from rest_framework.response import Response

from apps.doc.constants import DocSearchType
from apps.doc.exceptions import DocSearchTypeInvalid
from apps.doc.models import Doc, DocTag, Tag
from apps.doc.permissions import CreateDocPermission, DocOwnerPermission
from apps.doc.serializers import (
    DocInfoSerializer,
    DocListSerializer,
    DocSearchSerializer,
    EditDocSerializer,
)


class DocViewSet(ListMixin, RetrieveMixin, CreateMixin, UpdateMixin, DestroyMixin, MainViewSet):
    """
    Doc
    """

    queryset = Doc.objects.all()
    permission_classes = [DocOwnerPermission]

    def get_authenticators(self):
        if self.action_map[self.request.method.lower()] in ["list", "retrieve"]:
            return [SessionAuthenticate()]
        return super().get_authenticators()

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action in ["create"]:
            permissions.append(CreateDocPermission())
        return permissions

    # pylint: disable=R0914
    async def list(self, request: Request, *args, **kwargs):
        """
        Doc List
        """

        # Validate
        serializer = DocSearchSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.validated_data

        # QuerySet
        queryset = (
            Doc.objects.filter(Q(Q(owner=request.user) | Q(is_public=True)))
            .prefetch_related("owner")
            .prefetch_related("comment_set")
            .prefetch_related("doctag_set__tag")
        )

        # Tags Filter
        tags = request_data.get("tags", [])
        if tags:
            tags = Tag.objects.filter(name__in=tags)
            doc_tag = DocTag.objects.filter(tag__in=tags)
            queryset = queryset.filter(id__in=doc_tag.values("doc"))

        # Content Filter
        keywords = request_data.get("keywords", [])
        if keywords:
            match settings.DOC_SEARCH_TYPE:
                # Title
                case DocSearchType.TITLE:
                    search_keys = ["title"]
                # Content
                case DocSearchType.CONTENT:
                    search_keys = ["content"]
                # All
                case DocSearchType.ALL:
                    search_keys = ["title", "content"]
                # Default
                case _:
                    raise DocSearchTypeInvalid()
            # Any search key contains all keyword -> match
            q = Q()  # pylint: disable=C0103
            for search_key in search_keys:
                search_filter = Q()
                for keyword in keywords:
                    search_filter &= Q(**{f"{search_key}__contains": keyword})
                q |= search_filter  # pylint: disable=C0103
            queryset = queryset.filter(q)

        # Page
        page = NumPagination()
        queryset = await sync_to_async(page.paginate_queryset)(queryset=queryset, request=request, view=self)

        # Serialize
        serializer = DocListSerializer(instance=queryset, many=True)
        return page.get_paginated_response(await serializer.adata)

    async def retrieve(self, request: Request, *args, **kwargs):
        """
        Doc Info
        """

        inst: QuerySet = await sync_to_async(self.get_and_incr_read)()
        serializer = DocInfoSerializer(instance=inst, many=True)
        data = await serializer.adata
        return Response(data[0])

    def get_and_incr_read(self) -> QuerySet:
        inst: Doc = self.get_object()
        inst.record_read()
        return (
            Doc.objects.filter(pk=inst.pk)
            .prefetch_related("owner")
            .prefetch_related("comment_set")
            .prefetch_related("doctag_set__tag")
        )

    async def create(self, request: Request, *args, **kwargs):
        """
        Create Doc
        """

        # Validate
        serializer = EditDocSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.validated_data

        # Create
        doc = await sync_to_async(self.create_and_bind_tag)(request, request_data)

        return Response({"id": doc.id})

    @transaction.atomic()
    def create_and_bind_tag(self, request: Request, request_data: dict) -> Doc:
        # Create Doc
        doc = Doc.objects.create(
            title=request_data["title"],
            content=request_data["content"],
            header_img=request_data["header_img"],
            is_public=request_data["is_public"],
            owner=request.user,
            updated_at=timezone.now(),
            created_at=request_data.get("created_at", timezone.now()),
        )

        # Create Doc Tag Relation
        doc.bind_tags(tags=request_data["tags"])

        return doc

    async def update(self, request: Request, *args, **kwargs):
        """
        Update Doc
        """

        # Load Inst
        inst: Doc = await sync_to_async(self.get_object)()

        # Validate
        serializer = EditDocSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.validated_data

        # Update
        await sync_to_async(self.update_and_bind_tag)(inst, request_data)

        return Response({"id": inst.id})

    @transaction.atomic()
    def update_and_bind_tag(self, inst: Doc, request_data):
        # Update Tag
        inst.bind_tags(request_data.pop("tags", []))

        # Update Doc
        for key, val in request_data.items():
            setattr(inst, key, val)
        inst.updated_at = timezone.now()
        inst.save(update_fields=[*request_data.keys(), "updated_at"])

    async def destroy(self, request, *args, **kwargs):
        """
        Delete Doc
        """

        inst = await sync_to_async(self.get_object)()
        await sync_to_async(inst.delete)()
        return Response()
