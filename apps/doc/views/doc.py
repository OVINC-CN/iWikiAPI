import datetime

from django.db import transaction
from django.db.models import Q
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

from apps.doc.models import Doc, DocTag, Tag
from apps.doc.permissions import DocOwnerPermission
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

    def list(self, request: Request, *args, **kwargs):
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

        # Page
        page = NumPagination()
        queryset = page.paginate_queryset(queryset=queryset, request=request, view=self)

        # Serialize
        serializer = DocListSerializer(instance=queryset, many=True)
        return page.get_paginated_response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs):
        """
        Doc Info
        """

        inst: Doc = self.get_object()
        inst.record_read()
        inst.refresh_from_db()
        return Response(DocInfoSerializer(instance=inst).data)

    @transaction.atomic()
    def create(self, request: Request, *args, **kwargs):
        """
        Create Doc
        """

        # Validate
        serializer = EditDocSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.validated_data

        # Create Doc
        doc = Doc.objects.create(
            title=request_data["title"],
            content=request_data["content"],
            header_img=request_data["header_img"],
            is_public=request_data["is_public"],
            owner=request.user,
            updated_at=datetime.datetime.now(),
            created_at=request_data.get("created_at", datetime.datetime.now()),
        )

        # Create Doc Tag Relation
        doc.bind_tags(tags=request_data["tags"])

        return Response({"id": doc.id})

    @transaction.atomic()
    def update(self, request: Request, *args, **kwargs):
        """
        Update Doc
        """

        # Load Inst
        inst: Doc = self.get_object()

        # Validate
        serializer = EditDocSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.validated_data

        # Update Tag
        inst.bind_tags(request_data.pop("tags", []))

        # Update Doc
        for key, val in request_data.items():
            setattr(inst, key, val)
        inst.updated_at = datetime.datetime.now()
        inst.save(update_fields=[*request_data.keys(), "updated_at"])

        return Response({"id": inst.id})
