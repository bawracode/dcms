from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Profile)
class UserPrefrenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'language')

# @admin.register(Translate)
# class TranslateAdmin(admin.ModelAdmin):
#     list_display = ('msgid', 'msgstr')
