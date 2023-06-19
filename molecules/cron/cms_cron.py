import time

import sys, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from django.utils import timezone

import croniter
from datetime import datetime

def convert_cron_to_datetime(cron_expression):
    cron = croniter.croniter(cron_expression)
    next_datetime = cron.get_next(datetime)
    return next_datetime


from molecules.cron.models import CronJob, CronSchedule

def schedule():
    cronjob = CronJob.objects.filter(status=True).values_list("name","time_expression","script_path")


    current_time = timezone.make_naive(timezone.localtime(timezone.now())) + timezone.timedelta(minutes=5)

    for cron in cronjob:
        if(current_time > convert_cron_to_datetime(cron[1])):
            tempCron = CronJob.objects.get(name=cron[0])

            CronSchedule(cron_job=tempCron,scheduled_time=convert_cron_to_datetime(cron[1]),execute_start_datetime=timezone.now(),status=1,timezone="UTC",max_retries=0,retry_count=0,retry_delay=0,concurrency=0).save()




def run():
    count2 = 1
    while count2 < 10:
        print("run", count2)
        count2 += 1
        time.sleep(1)

   
def main():
    pass

schedule()


