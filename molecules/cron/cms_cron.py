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

from django.core.signals import request_finished
from django.dispatch import receiver


#function to convert cron expression to datetime
def convert_cron_to_datetime(cron_expression):
    cron = croniter.croniter(cron_expression)
    next_datetime = cron.get_next(datetime)

    aware_datetime = timezone.make_aware(next_datetime, timezone.get_current_timezone())
    return aware_datetime

#function to return class name from script path
def return_class_name(script_path):
    class_name = script_path.split(".")[-1]
    return class_name


#function to schedule cron jobs
def schedule(schedule_time_in_minutes,next_time_in_minutes):      

    while True:
        available_cron = CronSchedule.objects.filter(status=1,scheduled_time__gt=timezone.localtime(timezone.now())).values_list("cron_job__name","cron_job__time_expression")
        cron_name_available = set([f"{i[0]}_{convert_cron_to_datetime(i[1])}" for i in available_cron])

        cronjob = CronJob.objects.filter(status=True).values_list("name","time_expression","script_path")
        print(cronjob)

        current_time = timezone.localtime(timezone.now()) + timezone.timedelta(minutes=next_time_in_minutes)


        print("\nUTC TIME:",current_time)

        for cron in cronjob:

            next_datetime = convert_cron_to_datetime(cron[1])

            if(current_time >= next_datetime and f"{cron[0]}_{next_datetime}" not in cron_name_available):
                print("current_time :",current_time)
                print("next_datetime :",next_datetime)

                tempCron = CronJob.objects.get(name=cron[0])
                

                CronSchedule(cron_job=tempCron,scheduled_time=convert_cron_to_datetime(cron[1]),status=1,timezone="UTC",max_retries=0,retry_count=0,retry_delay=0,concurrency=0).save()

        time.sleep(schedule_time_in_minutes*60)



#function to run cron jobs
def run():
    while True:
        print("CronJob START.......")
            
        pending_cron =  CronSchedule.objects.filter(status=1).values_list("id","cron_job__name","cron_job__script_path","cron_job__time_expression","scheduled_time","execute_start_datetime","max_retries","retry_count","retry_delay","concurrency","timezone")

        for cron in pending_cron:

            cron_path = cron[2]

            tempCron = CronJob.objects.get(name=cron[1])

            tempCronSchedule = CronSchedule.objects.get(id=cron[0])

            current_time = timezone.localtime(timezone.now())

            print("\nCurrent Time:",current_time)
            print("Scheduled Time:",tempCronSchedule.scheduled_time)

            try:
                module = importlib.import_module(cron_path)
                class_name = return_class_name(cron_path)
                class_obj = getattr(module, class_name)

                instance = class_obj()

                current_date = current_time.date()
                current_hour = current_time.hour
                current_minute = current_time.minute

                scheduled_date = tempCronSchedule.scheduled_time.date()
                scheduled_hour = tempCronSchedule.scheduled_time.hour
                scheduled_minute = tempCronSchedule.scheduled_time.minute

                if(current_date == scheduled_date and current_hour == scheduled_hour and current_minute == scheduled_minute):
                    cron_log = CronLog.objects.create(cron_job=tempCron,execution_time=tempCronSchedule.scheduled_time,status=True,output="",error_message="")
                    
                    tempCronSchedule.execute_start_datetime = timezone.localtime(timezone.now())

                    tempCronSchedule.status = 2
                    tempCronSchedule.save()


                    result = instance.execute()


                    tempCronSchedule.status = 3
                    tempCronSchedule.save()

                    tempCronSchedule.execute_end_datetime = timezone.localtime(timezone.now())
                    tempCronSchedule.save()
                    
                
                    cron_log.execution_time = timezone.localtime(timezone.now())

                    cron_log.status = 1
                    cron_log.output = result

                    cron_log.save()

            except (ImportError, AttributeError) as e:
                error_message = f"Failed to import class: {cron_path} from module: {class_name} \n Error: {e}"
                cron_log.error_message = error_message

                tempCronSchedule.status = 4 
                tempCronSchedule.save()

                cron_log.save()

            tempCronSchedule.save()
            


#function for running cronjob
def main():
    while True:
        try:

            thread1 = threading.Thread(target=schedule, args=(10,15))
            thread1.start()

            # Wait for 15 seconds to ensure function1 has started
            time.sleep(5)

            # Run function2 after waiting
            run()

            # Wait for thread1 to finish
            thread1.join()

            # Delay before starting the loop again
            time.sleep(5)

            # schedule(10,15)
            # run()
            # time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            tempCronSchedule = CronSchedule.objects.filter(status=1)  

            for i in tempCronSchedule:
                i.delete()
            
            print("Pendding Cron is Deleted!!!")
            print("CronJon STOP.......")
            break


try:

    main()

except (KeyboardInterrupt, SystemExit):
    tempCronSchedule = CronSchedule.objects.filter(status=1)  

    for i in tempCronSchedule:
        i.delete()
    print("Pendding Cron is Deleted!!!")
    print("CronJon STOP.......")



@receiver(request_finished)
def cleanup_handler(sender, **kwargs):
    tempCronSchedule = CronSchedule.objects.filter(status=1)  

    for i in tempCronSchedule:
        i.delete()
