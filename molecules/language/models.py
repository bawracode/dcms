
from django.contrib.auth.models import User
from django.db import models
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
    def save_model(self, request, obj, form, change):
        os.system("python manage.py makemessages -l {}".format(self.language))

# class Translate(models.Model):
#     msgid = models.CharField(max_length=200)
#     msgstr = models.CharField(max_length=200)

#     def __str__(self):
#         return self.msgid
