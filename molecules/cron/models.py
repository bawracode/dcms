from django.db import models
import pytz

# Create your models here.

class CronJob(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    time_expression = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    script_path = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class CronSchedule(models.Model):
    cron_job = models.ForeignKey(CronJob, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    execute_start_datetime = models.DateTimeField(blank=True, null=True)
    execute_end_datetime = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(default = 1,
                                   blank = True,
                                    null = True,
                                    help_text ='1->Pending, 2->Running, 3->Completed, 4->Failed', 
                                    choices =(
                                    (1, 'Pending'), (2, 'Running'),(3, "Completed"),(4,"Failed")
                                    ))
    
    TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]
    timezone = models.CharField(max_length=100, choices=TIMEZONE_CHOICES,default='UTC')

    max_retries = models.IntegerField()
    retry_count = models.IntegerField()
    retry_delay = models.IntegerField()
    concurrency = models.IntegerField()

    def __str__(self):
        return f"{self.cron_job.name} - {self.scheduled_time}"

class CronLog(models.Model):
    cron_job = models.ForeignKey(CronJob, on_delete=models.CASCADE)
    execution_time = models.DateTimeField()
    status = models.BooleanField(default=False)
    output = models.TextField(blank=True,null=True)
    error_message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cron_job.name} - {self.execution_time}"
