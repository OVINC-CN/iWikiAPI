from io import BytesIO

import PyRSS2Gen
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from ovinc_client.core.lock import task_lock
from ovinc_client.core.logger import celery_logger, logger

from apps.cel import app
from apps.cos.client import COSClient
from apps.doc.models import Doc, DocTag, Tag


@app.task(bind=True)
@task_lock()
@transaction.atomic()
def remove_unused_tags(self):
    celery_logger.info("[RemoveUnusedTags] Start %s", self.request.id)
    doc_tags = DocTag.objects.select_for_update().all().values("tag")
    to_delete = Tag.objects.select_for_update().exclude(id__in=doc_tags)
    celery_logger.info(
        "[RemoveUnusedTags] ToDelete %s", ";".join([t.name for t in to_delete]) if to_delete.count() else "<Empty>"
    )
    to_delete.delete()
    celery_logger.info("[RemoveUnusedTags] End %s", self.request.id)


@app.task(bind=True)
@task_lock()
def build_rss(self):
    celery_logger.info("[BuildRSS] Start %s", self.request.id)
    try:
        rss = PyRSS2Gen.RSS2(
            title=settings.DOC_RSS_BUILD_TITLE,
            link=settings.FRONTEND_URL,
            description=settings.DOC_RSS_BUILD_DESCRIPTION,
            lastBuildDate=timezone.now(),
            items=[
                PyRSS2Gen.RSSItem(
                    title=doc.title,
                    link=f"{settings.FRONTEND_URL.rstrip(" / ")}/doc/{doc.id}/",
                    categories=list(doc.doctag_set.all().values_list("tag__name", flat=True)),
                    guid=f"{settings.FRONTEND_URL.rstrip(" / ")}/doc/{doc.id}/",
                    pubDate=doc.created_at,
                )
                for doc in Doc.objects.filter(is_public=True).order_by("-created_at")[: settings.DOC_RSS_BUILD_SIZE]
            ],
        )
        output = BytesIO()
        rss.write_xml(output, encoding="utf-8")
        COSClient().upload(file=output.getbuffer(), path=settings.DOC_RSS_BUILD_PATH)
        logger.info("[BuildRSS] Success: %s %s", rss.title, rss.link)
    except Exception as e:  # pylint: disable=W0718
        logger.exception("[BuildRSS] Failed %s", e)
