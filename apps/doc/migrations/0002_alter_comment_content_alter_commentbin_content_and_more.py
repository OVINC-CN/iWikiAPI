# pylint: disable=C0103

from django.db import migrations

import apps.bk_crypto.models


class Migration(migrations.Migration):

    dependencies = [
        ("doc", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=apps.bk_crypto.models.SymmetricTextField(verbose_name="Content"),
        ),
        migrations.AlterField(
            model_name="commentbin",
            name="content",
            field=apps.bk_crypto.models.SymmetricTextField(verbose_name="Content"),
        ),
        migrations.AlterField(
            model_name="doc",
            name="content",
            field=apps.bk_crypto.models.SymmetricTextField(verbose_name="Content"),
        ),
        migrations.AlterField(
            model_name="doc",
            name="header_img",
            field=apps.bk_crypto.models.SymmetricTextField(verbose_name="Header Image"),
        ),
        migrations.AlterField(
            model_name="doc",
            name="title",
            field=apps.bk_crypto.models.SymmetricTextField(verbose_name="Title"),
        ),
        migrations.AlterField(
            model_name="docbin",
            name="content",
            field=apps.bk_crypto.models.SymmetricTextField(verbose_name="Content"),
        ),
        migrations.AlterField(
            model_name="docbin",
            name="header_img",
            field=apps.bk_crypto.models.SymmetricTextField(verbose_name="Header Image"),
        ),
        migrations.AlterField(
            model_name="docbin",
            name="title",
            field=apps.bk_crypto.models.SymmetricTextField(verbose_name="Title"),
        ),
    ]
