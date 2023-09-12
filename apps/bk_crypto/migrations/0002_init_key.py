from django.db import migrations

from apps.bk_crypto.ciphers import asymmetric_cipher, symmetric_cipher
from apps.bk_crypto.constants import ConfigItem
from apps.bk_crypto.models import CryptoConfig


def init_key(*args, **kwargs) -> None:
    """
    init private key
    """

    private_key = asymmetric_cipher.export_private_key()
    encoded_key = symmetric_cipher.encrypt(private_key)
    CryptoConfig.set(key=ConfigItem.PRIVATE_KEY.value, value=encoded_key)


class Migration(migrations.Migration):
    dependencies = [
        ("bk_crypto", "0001_initial"),
    ]

    operations = [migrations.RunPython(init_key)]
