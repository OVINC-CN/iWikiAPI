# pylint: disable=C0103

import ovinc_client.core.models
import ovinc_client.core.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CryptoConfig",
            fields=[
                (
                    "id",
                    ovinc_client.core.models.UniqIDField(
                        default=ovinc_client.core.utils.uniq_id_without_time,
                        max_length=32,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.CharField(db_index=True, max_length=255, verbose_name="Config Key")),
                ("value", models.JSONField(blank=True, null=True, verbose_name="Config Value")),
            ],
            options={
                "verbose_name": "Crypto Config",
                "verbose_name_plural": "Crypto Config",
                "ordering": ["key"],
            },
        ),
    ]
