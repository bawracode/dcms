from typing import Dict, Optional
from django.contrib import admin
from django.http.request import HttpRequest
from django.template.response import TemplateResponse
from .models import User, Post , SystemConfig
from django.forms import ModelForm
from django import forms
from django.conf import settings
import os
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget


base_dir = settings.BASE_DIR
class ToggleSwitchWidget(forms.CheckboxInput):
    template_name = os.path.join(base_dir,'templates','widgest','toggle_switch.html')

class Sysconfigform(ModelForm):
    
    class Meta:
        model = SystemConfig
        fields = "__all__"
        widgets = {
            "config_value": DjangoToggleSwitchWidget(round=True,),
        }
# Register your models here.
admin.site.site_header = "Rest API"
admin.site.site_title = "Rest API Portal"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','body','user')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','password')
    search_fields = ('title','user')

@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    form = Sysconfigform
    list_display = ('api_name','config_value')
    search_fields = ('api_name','config_value')
    # def changelist_view(self, request, extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['title'] = SystemConfig.objects.values_list('api_name', 'config_value')
    #     return super().changelist_view(request, extra_context=extra_context)