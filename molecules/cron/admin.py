from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(CronJob)
class CronJobAdmin(admin.ModelAdmin):
    list_display = ("name","time_expression","status","script_path")


@admin.register(CronSchedule)
class CronScheduleAdmin(admin.ModelAdmin):
    list_display = ("cron_job","scheduled_time","execute_start_datetime","execute_end_datetime","status","timezone","max_retries","retry_count","retry_delay","concurrency")


admin.site.register(CronLog)