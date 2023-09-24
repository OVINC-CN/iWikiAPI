from bkcrypto.contrib.django.fields import SymmetricTextField
from django.core.management import BaseCommand

from apps.bk_crypto.utils import DataEncryptHelper


class Command(BaseCommand):
    """
    Celery Command
    """

    field = SymmetricTextField()

    def handle(self, *args, **options):
        DataEncryptHelper().trans()
