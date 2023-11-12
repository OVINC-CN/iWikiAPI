# pylint: disable=C0103

from django.db import migrations

import apps.bk_crypto.models


class Migration(migrations.Migration):

    dependencies = [
        ("doc", "0002_alter_comment_content_alter_commentbin_content_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doc",
            name="header_img",
            field=apps.bk_crypto.models.SymmetricTextField(
                blank=True, null=True, using="default", verbose_name="Header Image"
            ),
        ),
        migrations.AlterField(
            model_name="docbin",
            name="header_img",
            field=apps.bk_crypto.models.SymmetricTextField(
                blank=True, null=True, using="default", verbose_name="Header Image"
            ),
        ),
    ]
