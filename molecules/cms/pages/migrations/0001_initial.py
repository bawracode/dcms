# Generated by Django 4.2.2 on 2023-06-15 12:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomPage",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("slug", models.SlugField(max_length=255, verbose_name="slug")),
                ("content", models.TextField()),
                (
                    "status",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, "Active"), (0, "Inactive")],
                        default=1,
                        help_text="1->Active, 0->Inactive",
                        null=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="creation date",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="updation date",
                    ),
                ),
            ],
        ),
    ]
