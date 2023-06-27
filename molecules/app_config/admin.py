from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from .models import *
import json

# Register your models here.
@admin.register(app_config)
class app_configAdmin(admin.ModelAdmin):
    change_list_template = "pages/admin/app_config/app_config_change_list.html"
    list_display = ("title","store","key","value","update_date")

    def changelist_view(self, request: HttpRequest, extra_context=None):
        extra_context = extra_context or {}

        # Load JSON data from file
        with open('C:/Users/jigne/Desktop/django_cms/molecules/app_config/app_config.json') as json_file:
            json_data = json.load(json_file)

        result = []

        for i in json_data:
            print(i.get('section'))
            result.append(i.get('section'))

        print(result)
        

        # Pass JSON data to template context
        extra_context['json_data'] = json_data
        extra_context['result'] = result

        return super().changelist_view(request, extra_context)