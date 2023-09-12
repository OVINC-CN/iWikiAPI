import datetime
from typing import List

from bkcrypto.contrib.django.fields import SymmetricTextField
from django.db import models, transaction
from django.utils.translation import gettext_lazy
from ovinc_client.core.models import BaseModel, ForeignKey, UniqIDField

from apps.doc.models.tag import DocTag, Tag


class DocBase(BaseModel):
    """
    Doc Base
    """

    id = UniqIDField(gettext_lazy("ID"), primary_key=True)
    title = SymmetricTextField(gettext_lazy("Title"))
    content = SymmetricTextField(gettext_lazy("Content"))
    header_img = SymmetricTextField(gettext_lazy("Header Image"))
    is_public = models.BooleanField(gettext_lazy("Is Public"), default=False, db_index=True)
    pv = models.BigIntegerField(gettext_lazy("PV"), default=int, db_index=True)
    owner = ForeignKey(gettext_lazy("Owner"), to="account.User", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(gettext_lazy("Updated Time"), db_index=True)
    created_at = models.DateTimeField(gettext_lazy("Created Time"), db_index=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return "{} ({})".format(self.title, self.id)


class Doc(DocBase):
    """
    Doc
    """

    class Meta:
        verbose_name = gettext_lazy("Doc")
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    @transaction.atomic()
    def delete(self, *args, **kwargs) -> None:
        doc_bin = DocBin()
        for field in self._meta.fields:
            setattr(doc_bin, field.name, getattr(self, field.name))
        doc_bin.deleted_at = datetime.datetime.now()
        doc_bin.save()
        return super().delete(*args, **kwargs)

    def bind_tags(self, tags: List[dict]) -> None:
        if not tags:
            return
        Tag.objects.bulk_create([Tag(name=tag) for tag in tags], ignore_conflicts=True)
        tags = Tag.objects.filter(name__in=tags)
        DocTag.objects.bulk_create([DocTag(tag=tag, doc=self) for tag in tags], ignore_conflicts=True)
        DocTag.objects.filter(doc=self).exclude(tag__in=tags).delete()


class DocBin(DocBase):
    """
    Doc Bin
    """

    deleted_at = models.DateTimeField(gettext_lazy("Deleted Time"), db_index=True)

    class Meta:
        verbose_name = gettext_lazy("Doc Bin")
        verbose_name_plural = verbose_name
        ordering = ["-deleted_at"]
