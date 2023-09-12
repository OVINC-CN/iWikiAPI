from django.utils.translation import gettext_lazy
from ovinc_client.core.models import TextChoices


class ConfigItem(TextChoices):
    """
    Config Item
    """

    PRIVATE_KEY = "private_key", gettext_lazy("Private Key")
