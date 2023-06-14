from django.contrib import admin
from .models import Blocks

# Register your models here.
@admin.register(Blocks)
class BlockAdmin(admin.ModelAdmin):
    pass
