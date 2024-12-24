from ovinc_client.core.lock import task_lock
from ovinc_client.core.logger import celery_logger

from apps.cel import app
from apps.home.utils import Sitemap


@app.task(bind=True)
@task_lock()
def generate_sitemap(self):
    celery_logger.info(f"[GenerateSitemap] Start {self.request.id}")
    Sitemap().upload_cos()
    celery_logger.info(f"[GenerateSitemap] End {self.request.id}")
