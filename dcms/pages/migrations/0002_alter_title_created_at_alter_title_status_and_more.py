# Generated by Django 4.2.2 on 2023-06-14 10:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="title",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="creation date",
            ),
        ),
        migrations.AlterField(
            model_name="title",
            name="status",
            field=models.BooleanField(default=True, verbose_name="status"),
        ),
        migrations.AlterField(
            model_name="title",
            name="updated_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="updation date",
            ),
        ),
    ]