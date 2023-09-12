from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class BkCryptoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bk_crypto"
    verbose_name = gettext_lazy("BK Crypto")
