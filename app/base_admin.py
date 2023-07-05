from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http.request import HttpRequest
from django.conf import settings

class BaseModelAdmin(admin.ModelAdmin):
    def action(self, obj):
        return mark_safe(f'''
                         <a href="{obj.id}/change/"><img src="/static/admin/img/icon-changelink.svg" alt="True"></a> \t\t
                         <a href="{obj.id}/delete/"><img src="/static/admin/img/icon-deletelink.svg" alt="True"></a>''')
    action.short_description = 'Actions'
    def get_column_names(self):
        model = self.model
        
        column_names = [field.name for field in model._meta.get_fields()]
        return column_names
    def changelist_view(self, request, extra_context=None):
        
        extra_context = extra_context or {}

        column_names = self.get_column_names()
        # column_names.insert(0,'action_checkbox')
        # column_names.insert(1,'action')

        extra_context['column_names'] = column_names

        return super().changelist_view(request, extra_context)

    
    