from urllib.parse import quote

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from ovinc_client.account.models import User
from qcloud_cos import CosConfig, CosS3Client

from apps.cos.exceptions import UploadFailed
from apps.cos.models import COSLog

USER_MODEL: User = get_user_model()


class Client:
    """
    COS Client
    """

    def __init__(self, user: USER_MODEL):
        self.user = user
        self.config = CosConfig(
            Region=settings.QCLOUD_COS_REGION, SecretId=settings.QCLOUD_SECRET_ID, SecretKey=settings.QCLOUD_SECRET_KEY
        )
        self.client = CosS3Client(self.config)

    def upload(self, file: InMemoryUploadedFile) -> str:
        # Record Log
        try:
            cos_log = COSLog.objects.create(
                filename=file.name, key=COSLog.build_key(file.name), resp={}, owner=self.user
            )
        except IntegrityError:
            return self.upload(file)
        # Upload
        try:
            resp = self.client.put_object(
                Bucket=settings.QCLOUD_COS_BUCKET,
                Body=file,
                Key=cos_log.key,
            )
        except Exception as err:
            cos_log.resp = getattr(err, "_digest_msg", {})
            cos_log.save(update_fields=["resp"])
            raise UploadFailed(detail=cos_log.resp.get("message"))
        # Update Log
        cos_log.resp = resp
        cos_log.save(update_fields=["resp"])
        # Check Success
        if "ETag" in resp:
            return f"{settings.QCLOUD_COS_URL}/{quote(cos_log.key)}"
        raise UploadFailed()
