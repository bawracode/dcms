# Generated by Django 4.2.2 on 2023-07-12 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="custompage",
            name="content",
            field=models.TextField(blank=True, null=True, verbose_name="content"),
        ),
    ]