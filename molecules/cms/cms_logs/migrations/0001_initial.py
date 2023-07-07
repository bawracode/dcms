# Generated by Django 4.2.3 on 2023-07-07 09:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlockLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255, verbose_name='user')),
                ('actions', models.CharField(max_length=255)),
                ('ip_address', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='creation date')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='updation date')),
            ],
        ),
        migrations.CreateModel(
            name='PageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255, verbose_name='user')),
                ('actions', models.CharField(max_length=255)),
                ('ip_address', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='creation date')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='updation date')),
            ],
        ),
    ]
