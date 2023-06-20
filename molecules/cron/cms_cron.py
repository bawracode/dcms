import sys, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

import time
import croniter
import threading
import importlib
from django.utils import timezone
from datetime import datetime
from molecules.cron.models import CronJob, CronSchedule, CronLog


#function to convert cron expression to datetime
def convert_cron_to_datetime(cron_expression):
    cron = croniter.croniter(cron_expression)
    next_datetime = cron.get_next(datetime)
    return next_datetime


def return_class_name(script_path):
    class_name = script_path.split(".")[-1]
    return class_name


#function to schedule cron jobs
def schedule(wait_time_in_minutes):
    while True:
        pass
        cronjob = CronJob.objects.filter(status=True).values_list("name","time_expression","script_path")


        current_time = timezone.make_naive(timezone.localtime(timezone.now())) + timezone.timedelta(minutes=15)


        print("\nUTC TIME:",current_time)

        for cron in cronjob:

            next_datetime = convert_cron_to_datetime(cron[1])

            if(current_time > next_datetime):


                tempCron = CronJob.objects.get(name=cron[0])
                
                print(tempCron.time_expression)
                print(convert_cron_to_datetime(cron[1]))

                CronSchedule(cron_job=tempCron,scheduled_time=convert_cron_to_datetime(cron[1]),execute_start_datetime=timezone.now(),status=1,timezone="UTC",max_retries=0,retry_count=0,retry_delay=0,concurrency=0).save()

        time.sleep(wait_time_in_minutes*60)



#function to run cron jobs
def run():
    pending_cron =  CronSchedule.objects.filter(status=1).values_list("id","cron_job__name","cron_job__script_path","cron_job__time_expression","scheduled_time","execute_start_datetime","max_retries","retry_count","retry_delay","concurrency","timezone")

    for cron in pending_cron:
        cron_path = cron[2]

        tempCron = CronJob.objects.get(name=cron[1])

        tempCronSchedule = CronSchedule.objects.get(id=cron[0])

        cron_log = CronLog()

        try:
            module = importlib.import_module(cron_path)
            class_name = return_class_name(cron_path)
            class_obj = getattr(module, class_name)

            instance = class_obj()

            tempCronSchedule.status = 2
            tempCronSchedule.save()

            result = instance.execute()

            print("Running")

            cron_log.cron_job = tempCron
            cron_log.execution_time = timezone.now()
            cron_log.status = 1
            cron_log.output = result


        except (ImportError, AttributeError) as e:
            error_message = f"Failed to import class: {cron_path} from module: {class_name} \n Error: {e}"
            cron_log.error_message = error_message

            tempCronSchedule.status = 4 
            tempCronSchedule.save()

        tempCronSchedule.status = 3
        tempCronSchedule.save()
        
        cron_log.save()


#function for running cronjob
def main():
    pass
    # while True:
    #     thread1 = threading.Thread(target=schedule, args=(1,))
    #     thread1.start()

    #     # Wait for 15 seconds to ensure function1 has started
    #     time.sleep(5)

    #     # Run function2 after waiting
    #     run()

    #     # Wait for thread1 to finish
    #     thread1.join()

    #     # Delay before starting the loop again
    #     time.sleep(5)


try:
    run()

except (KeyboardInterrupt, SystemExit):
    tempCronSchedule = CronSchedule.objects.filter(status=1)  

    for i in tempCronSchedule:
        i.delete()
    print("Pendding Cron is Deleted!!!")
    print("CronJon STOP.......")
