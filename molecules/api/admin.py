from typing import Dict, Optional
from django.contrib import admin
from django.http.request import HttpRequest
from django.template.response import TemplateResponse
from .models import User, Post , SystemConfig
from django.forms import ModelForm
from django import forms
from django.conf import settings
import os
from django.contrib import admin
from django_cron.models import CronJobLog
from django.utils.html import format_html

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
    list_display = ('api_name','render_toggle_switch')
    search_fields = ('api_name','config_value')
    def render_toggle_switch(self, obj):
        change = ""
         
        if obj.config_value:
            change = "checked"
        # print(obj.config_value,"self")
        return format_html('''
        <label class="switch">
<input type="checkbox" class="toggle-switch" {} onclick="toggleSwitchChanged({})">
  <span class="slider round"></span>
</label>
        
        '''.format(change,obj.id))


    render_toggle_switch.short_description = 'Toggle Switch'



# class CronJobLogAdmin(admin.ModelAdmin):
#     list_display = ('code', 'is_success', 'start_time', 'end_time')

# admin.site.register(CronJobLog, CronJobLogAdmin)
 