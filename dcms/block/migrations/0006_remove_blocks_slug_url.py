# Generated by Django 4.2.2 on 2023-06-14 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("block", "0005_alter_blocks_slug_url"),
    ]

    operations = [
        migrations.RemoveField(model_name="blocks", name="slug_url",),
    ]