from django.utils.translation import gettext_lazy
from ovinc_client.core.models import TextChoices


class DocSearchType(TextChoices):
    """
    Doc Search Type
    """

    TITLE = "title", gettext_lazy("Title")
    CONTENT = "content", gettext_lazy("Content")
    ALL = "all", gettext_lazy("All")
