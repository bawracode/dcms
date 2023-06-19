from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CronJob)
admin.site.register(CronSchedule)
admin.site.register(CronLog)