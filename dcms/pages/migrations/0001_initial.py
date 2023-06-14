# Generated by Django 4.2.2 on 2023-06-14 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Title",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("slug", models.SlugField(max_length=255, verbose_name="slug")),
                ("content", models.TextField()),
                ("status", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
            ],
        ),
    ]