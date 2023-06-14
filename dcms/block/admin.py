from django.contrib import admin
from .models import Block

# Register your models here.
@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("id",'slug', 'status', "content",'created_at', 'updated_at')