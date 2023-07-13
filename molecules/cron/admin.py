from django.contrib import admin
from .models import *
from django.forms import ModelForm
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django.utils.html import format_html

from django import forms

class CronJobForm(forms.ModelForm):
    
    class Meta:
        model = CronJob
        fields = "__all__"
        widgets = {
            "status": DjangoToggleSwitchWidget(round=True,),
        }

@admin.register(CronJob)
class CronJobAdmin(admin.ModelAdmin):
    form = CronJobForm
    list_display = ("name","time_expression","display_status","script_path")

    class Media:
        js = ('js/admin/cron/script.js',)


    def display_status(self, obj):
        toggle_class = 'django-toggle-switch-on' if obj.status else 'django-toggle-switch-off'
        object_status = obj.id
        return format_html(
            '<label class="django-toggle-switch {0}" >'
                
            '<input type="checkbox" name="status" id="{1}" {2}>'
            '<span class="django-toggle-switch-slider round"></span>'
            '</label>',
            toggle_class,
            object_status,
            ' checked' if obj.status else ''
        )

    display_status.short_description = 'Status'
    display_status.admin_order_field = 'status'



@admin.register(CronSchedule)
class CronScheduleAdmin(admin.ModelAdmin):
    list_display = ("cron_job","scheduled_time","execute_start_datetime","execute_end_datetime","status","timezone","max_retries","retry_count","retry_delay","concurrency")


@admin.register(CronLog)
class CronLogAdmin(admin.ModelAdmin):
    list_display = ("cron_job","execution_time","status","output","error_message","created_date")


