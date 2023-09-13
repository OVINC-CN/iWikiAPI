from bkcrypto import constants
from bkcrypto.asymmetric import options
from bkcrypto.asymmetric.ciphers import BaseAsymmetricCipher
from bkcrypto.contrib.basic.ciphers import get_asymmetric_cipher
from bkcrypto.contrib.django.ciphers import get_symmetric_cipher
from bkcrypto.symmetric.ciphers import BaseSymmetricCipher
from django.conf import settings

from apps.bk_crypto.constants import ConfigItem
from apps.bk_crypto.models import CryptoConfig

symmetric_cipher: BaseSymmetricCipher = get_symmetric_cipher(
    cipher_type=constants.SymmetricCipherType.SM4.value,
    common={"key": settings.APP_SECRET},
)

private_key = CryptoConfig.get(key=ConfigItem.PRIVATE_KEY.value)[1]
if private_key:
    private_key = symmetric_cipher.decrypt(private_key)
asymmetric_cipher: BaseAsymmetricCipher = get_asymmetric_cipher(
    cipher_type=constants.AsymmetricCipherType.SM2.value,
    cipher_options={
        constants.AsymmetricCipherType.SM2.value: options.SM2AsymmetricOptions(private_key_string=private_key),
        constants.AsymmetricCipherType.RSA.value: options.SM2AsymmetricOptions(private_key_string=private_key),
    },
)
