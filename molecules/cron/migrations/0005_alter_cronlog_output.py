# Generated by Django 4.2.2 on 2023-06-20 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cron", "0004_alter_cronschedule_execute_end_datetime_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cronlog", name="output", field=models.TextField(blank=True),
        ),
    ]
