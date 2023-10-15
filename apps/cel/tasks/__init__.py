from apps.cel.tasks.debug import celery_debug
from apps.cel.tasks.doc import remove_unused_tags
from apps.cel.tasks.home import generate_sitemap

__all__ = [
    "celery_debug",
    "remove_unused_tags",
    "generate_sitemap",
]
