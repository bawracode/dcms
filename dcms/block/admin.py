from django.contrib import admin
from .models import Blocks

# Register your models here.
@admin.register(Blocks)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("id",'slug', 'status', "content",'created_at', 'updated_at',"formatted_full_url")