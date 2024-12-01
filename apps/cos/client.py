import traceback
from urllib.parse import quote

from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from ovinc_client.account.models import User
from ovinc_client.core.logger import logger
from qcloud_cos import CosConfig, CosS3Client
from sts.sts import Sts

from apps.cos.exceptions import TempKeyGenerateFailed, UploadFailed
from apps.cos.models import COSCredential, COSLog
from apps.cos.utils import TCloudUrlParser

USER_MODEL: User = get_user_model()


class STSClient:
    """
    STS Client
    """

    @classmethod
    async def generate_cos_upload_credential(cls, user: USER_MODEL, filename: str) -> COSCredential:
        try:
            cos_log = await database_sync_to_async(COSLog.objects.create)(
                filename=filename, key=COSLog.build_key(filename), resp={}, owner=user
            )
        except IntegrityError:
            return await cls.generate_cos_upload_credential(user=user, filename=filename)
        tencent_cloud_api_domain = settings.QCLOUD_API_DOMAIN_TMPL.format("sts")
        config = {
            "domain": tencent_cloud_api_domain,
            "url": f"{settings.QCLOUD_API_SCHEME}://{tencent_cloud_api_domain}",
            "duration_seconds": settings.QCLOUD_STS_EXPIRE_TIME,
            "secret_id": settings.QCLOUD_SECRET_ID,
            "secret_key": settings.QCLOUD_SECRET_KEY,
            "bucket": settings.QCLOUD_COS_BUCKET,
            "region": settings.QCLOUD_COS_REGION,
            "allow_prefix": [cos_log.key],
            "allow_actions": [
                "cos:PutObject",
                "cos:ListMultipartUploads",
                "cos:ListParts",
                "cos:InitiateMultipartUpload",
                "cos:UploadPart",
                "cos:CompleteMultipartUpload",
            ],
        }
        response = {}
        try:
            sts = Sts(config)
            response = sts.get_credential()
            return COSCredential(
                cos_url=settings.QCLOUD_COS_URL,
                cos_bucket=settings.QCLOUD_COS_BUCKET,
                cos_region=settings.QCLOUD_COS_REGION,
                key=cos_log.key,
                secret_id=response["credentials"]["tmpSecretId"],
                secret_key=response["credentials"]["tmpSecretKey"],
                token=response["credentials"]["sessionToken"],
                start_time=response["startTime"],
                expired_time=response["expiredTime"],
                cdn_sign=TCloudUrlParser.sign("/" + quote(cos_log.key.lstrip("/"), safe="")),
            )
        except Exception as err:
            logger.exception("[TempKeyGenerateFailed] %s", err)
            response = {"err": str(err), "traceback": traceback.format_exc()}
            raise TempKeyGenerateFailed() from err
        finally:
            cos_log.resp = response
            await database_sync_to_async(cos_log.save)(update_fields=["resp"])


class COSClient:
    """
    COS Client
    """

    def __init__(self, user: USER_MODEL = None):
        self.user = user
        self.config = CosConfig(
            Region=settings.QCLOUD_COS_REGION, SecretId=settings.QCLOUD_SECRET_ID, SecretKey=settings.QCLOUD_SECRET_KEY
        )
        self.client = CosS3Client(self.config)

    async def upload(self, file: InMemoryUploadedFile, path: str, *args, **kwargs) -> None:
        try:
            resp = self.client.put_object(Bucket=settings.QCLOUD_COS_BUCKET, Body=file, Key=path, *args, **kwargs)
        except Exception as err:
            detail = getattr(err, "_digest_msg", {})
            raise UploadFailed(detail=detail.get("message")) from err
        # Check Success
        if "ETag" in resp:
            return
        raise UploadFailed()
