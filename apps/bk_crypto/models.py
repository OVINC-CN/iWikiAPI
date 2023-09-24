from bkcrypto.contrib.django.fields import SymmetricTextField as _SymmetricTextField
from django.conf import settings
from django.db import ProgrammingError, models
from django.utils.translation import gettext_lazy
from ovinc_client.core.constants import MAX_CHAR_LENGTH
from ovinc_client.core.models import BaseModel, UniqIDField


class CryptoConfig(BaseModel):
    """
    Crypto Config
    """

    id = UniqIDField(gettext_lazy("ID"), primary_key=True)
    key = models.CharField(gettext_lazy("Config Key"), max_length=MAX_CHAR_LENGTH, db_index=True)
    value = models.JSONField(gettext_lazy("Config Value"), null=True, blank=True)

    class Meta:
        verbose_name = gettext_lazy("Crypto Config")
        verbose_name_plural = verbose_name
        ordering = ["key"]

    @classmethod
    def get(cls, key: str, default: any = None) -> (bool, any):
        try:
            config = cls.objects.filter(key=key).first()
            if config:
                return True, config.value
            return False, default
        except ProgrammingError:
            return False, default

    @classmethod
    def set(cls, key: str, value: any) -> (bool, "CryptoConfig"):
        config, is_create = cls.objects.get_or_create(key=key, defaults={"value": value})
        config.value = value
        config.save()
        return is_create, config


class SymmetricTextField(_SymmetricTextField):
    def get_decrypted_value(self, value):
        if settings.ENABLE_BKCRYPTO:
            return super().get_decrypted_value(value)
        return value

    def encrypt(self, value):
        if settings.ENABLE_BKCRYPTO:
            return super().encrypt(value)
        return value
