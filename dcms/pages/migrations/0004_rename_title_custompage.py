# Generated by Django 4.2.2 on 2023-06-14 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_alter_title_status"),
    ]

    operations = [
        migrations.RenameModel(old_name="Title", new_name="CustomPage",),
    ]
