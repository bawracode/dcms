
from django.core.management import call_command
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=(
        ('en', 'English'),
        ('es', 'Español'),
        ('fr', 'Français'),
        ('de', 'Deutsch'),
        ('it', 'Italiano'),
        ('pt', 'Português'),
        ('ru', 'Русский'),
        ('zh-hans', '简体中文'),
        ('zh-hant', '繁體中文'),
        ('ja', '日本語'),
        ('ko', '한국어'),
        ('ar', 'العربية'),
        ('hi', 'हिन्दी'),
        ('bn', 'বাংলা'),
        ('pa', 'ਪੰਜਾਬੀ'),
        ('ms', 'Bahasa Melayu'),
        ('id', 'Bahasa Indonesia'),
        ('tr', 'Türkçe'),
        ('vi', 'Tiếng Việt'),
        ('th', 'ภาษาไทย'),
        ('pl', 'Polski'),
        ('uk', 'Українська'),
        ('cs', 'Čeština'),
        ('nl', 'Nederlands'),
        ('hu', 'Magyar'),
        ('sv', 'Svenska'),
        ('da', 'Dansk'),
        ('fi', 'Suomi'),
        ('no', 'Norsk'),
        ('el', 'Ελληνικά'),
        ('he', 'עברית'),
        ('fa', 'فارسی'),
        ('bg', 'Български'),
        ('hr', 'Hrvatski'),
        ('lt', 'Lietuvių'),
        ('sk', 'Slovenčina'),
        ('sl', 'Slovenščina'),
        ('sr', 'Српски'),
        ('ro', 'Română'),
        ('eo', 'Esperanto'),
        
    ) )  # Field to store language preference

@receiver(post_save, sender=Profile)
def generate_messages(sender, instance, created, **kwargs):
    os.system("python manage.py makemessages -l {}".format(instance.language))


post_save.connect(generate_messages, sender=Profile)
