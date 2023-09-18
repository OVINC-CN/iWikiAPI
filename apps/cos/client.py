import traceback

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from ovinc_client.account.models import User
from ovinc_client.core.logger import logger
from sts.sts import Sts

from apps.cos.exceptions import TempKeyGenerateFailed
from apps.cos.models import COSCredential, COSLog

USER_MODEL: User = get_user_model()


class STSClient:
    """
    STS Client
    """

    @classmethod
    def generate_cos_upload_credential(cls, user: USER_MODEL, filename: str) -> COSCredential:
        try:
            cos_log = COSLog.objects.create(filename=filename, key=COSLog.build_key(filename), resp={}, owner=user)
        except IntegrityError:
            return cls.generate_cos_upload_credential(user=user, filename=filename)
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
            "allow_actions": ["name/cos:PutObject"],
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
            )
        except Exception as err:
            logger.exception("[TempKeyGenerateFailed] %s", err)
            response = {"err": str(err), "traceback": traceback.format_exc()}
            raise TempKeyGenerateFailed() from err
        finally:
            cos_log.resp = response
            cos_log.save(update_fields=["resp"])
