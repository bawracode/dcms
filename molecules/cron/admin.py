from django.contrib import admin
from .models import *
from django.forms import ModelForm
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

class CronJobForm(ModelForm):
    
    class Meta:
        model = CronJob
        fields = "__all__"
        widgets = {
            "status": DjangoToggleSwitchWidget(round=True,),
        }

@admin.register(CronJob)
class CronJobAdmin(admin.ModelAdmin):
    form = CronJobForm
    list_display = ("name","time_expression","status","script_path")


@admin.register(CronSchedule)
class CronScheduleAdmin(admin.ModelAdmin):
    list_display = ("cron_job","scheduled_time","execute_start_datetime","execute_end_datetime","status","timezone","max_retries","retry_count","retry_delay","concurrency")


@admin.register(CronLog)
class CronLogAdmin(admin.ModelAdmin):
    list_display = ("cron_job","execution_time","status","output","error_message","created_date")


