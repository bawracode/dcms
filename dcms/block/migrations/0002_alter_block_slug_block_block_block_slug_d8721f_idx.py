# Generated by Django 4.2.2 on 2023-06-14 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("block", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="block",
            name="slug",
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AddIndex(
            model_name="block",
            index=models.Index(fields=["slug"], name="block_block_slug_d8721f_idx"),
        ),
    ]
