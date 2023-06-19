from django.db import models

# Create your models here.

class CronJob(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    time_expression = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    script_path = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class CronSchedule(models.Model):
    cron_job = models.ForeignKey(CronJob, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    execute_start_datetime = models.DateTimeField()
    execute_end_datetime = models.DateTimeField()
    status = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)
    max_retries = models.IntegerField()
    retry_count = models.IntegerField()
    retry_delay = models.IntegerField()
    concurrency = models.IntegerField()

class CronLog(models.Model):
    cron_job = models.ForeignKey(CronJob, on_delete=models.CASCADE)
    execution_time = models.DateTimeField()
    status = models.BooleanField(default=False)
    output = models.TextField()
    error_message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
