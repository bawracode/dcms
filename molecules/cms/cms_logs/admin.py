from django.contrib import admin
from .models import PageLog,BlockLog

# Register your models here.

@admin.register(PageLog)
class PageLogAdmin(admin.ModelAdmin):
    list_display = ['user','action','ip_address','created_at','updated_at']

    list_per_page = 20

@admin.register(BlockLog)
class BlockLogAdmin(admin.ModelAdmin):
    list_display = ['user','action','ip_address','created_at','updated_at']

    list_per_page = 20