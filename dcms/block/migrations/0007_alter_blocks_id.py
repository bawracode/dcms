# Generated by Django 4.2.2 on 2023-06-15 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("block", "0006_remove_blocks_slug_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blocks",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
