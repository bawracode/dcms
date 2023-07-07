from django.contrib import admin
from .models import PageLog,BlockLog

from app import base_admin
# Register your models here.

@admin.register(PageLog)
class PageLogAdmin(admin.ModelAdmin):
    list_display = ['user','actions','ip_address','created_at','updated_at']

    

@admin.register(BlockLog)
class BlockLogAdmin(base_admin.BaseModelAdmin):
    pass
