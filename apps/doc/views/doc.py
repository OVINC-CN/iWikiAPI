import datetime

from django.db import transaction
from django.db.models import Q
from ovinc_client.core.paginations import NumPagination
from ovinc_client.core.viewsets import (
    CreateMixin,
    DestroyMixin,
    ListMixin,
    MainViewSet,
    RetrieveMixin,
    UpdateMixin,
)
from rest_framework.response import Response

from apps.doc.models import Doc, DocTag, Tag
from apps.doc.permissions import DocOwnerPermission
from apps.doc.serializers import DocInfoSerializer, DocListSerializer, EditDocSerializer


class DocViewSet(ListMixin, RetrieveMixin, CreateMixin, UpdateMixin, DestroyMixin, MainViewSet):
    """
    Doc
    """

    queryset = Doc.objects.all()
    permission_classes = [DocOwnerPermission]

    def list(self, request, *args, **kwargs):
        """
        Doc List
        """

        # Filter
        queryset = (
            Doc.objects.filter(Q(Q(owner=request.user) | Q(is_public=True)))
            .prefetch_related("owner")
            .prefetch_related("comment_set")
            .prefetch_related("doctag_set__tag")
        )

        # Page
        page = NumPagination()
        queryset = page.paginate_queryset(queryset=queryset, request=request, view=self)

        # Serialize
        serializer = DocListSerializer(instance=queryset, many=True)
        return page.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Doc Info
        """

        inst = self.get_object()
        return Response(DocInfoSerializer(instance=inst).data)

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """
        Create Doc
        """

        # Validate
        serializer = EditDocSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.validated_data

        # Create Tag
        Tag.objects.bulk_create([Tag(name=tag) for tag in request_data["tags"]], ignore_conflicts=True)
        tags = Tag.objects.filter(name__in=request_data["tags"])

        # Create Doc
        doc = Doc.objects.create(
            title=request_data["title"],
            content=request_data["content"],
            header_img=request_data["header_img"],
            is_public=request_data["is_public"],
            owner=request.user,
            updated_at=datetime.datetime.now(),
            created_at=datetime.datetime.now(),
        )

        # Create Doc Tag Relation
        DocTag.objects.bulk_create([DocTag(tag=tag, doc=doc) for tag in tags], ignore_conflicts=True)

        return Response()

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
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
        tags = request_data.pop("tags", [])
        Tag.objects.bulk_create([Tag(name=tag) for tag in tags], ignore_conflicts=True)
        tags = Tag.objects.filter(name__in=tags)
        DocTag.objects.filter(doc=inst).delete()
        DocTag.objects.bulk_create([DocTag(tag=tag, doc=inst) for tag in tags], ignore_conflicts=True)

        # Update Doc
        for key, val in request_data.items():
            setattr(inst, key, val)
        inst.save(update_fields=request_data.keys())

        return Response()
