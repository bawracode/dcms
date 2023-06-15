from django.contrib import admin
from .models import PageLog,BlockLog

# Register your models here.
admin.site.register(PageLog)
admin.site.register(BlockLog)