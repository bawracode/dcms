import os
import sys
import django
import time

# Set up Django environment
sys.path.append('/Users/jashkakadiya/Downloads/cms/app')  # Replace with the actual path to your Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# Import your models
from molecules.cms.cms_cron.models import CronJob, CronSchedule

def load_and_run_cron_jobs():
    while True:
        # Get the current time
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Fetch the cron schedules that need to be executed
        cron_schedules = CronSchedule.objects.filter(
            scheduled_time__lte=current_time,
            status='pending'
        )

        # Iterate over the cron schedules and execute the associated cron jobs
        for cron_schedule in cron_schedules:
            cron_job = cron_schedule.cron_job
            script_path = cron_job.script_path

            # Execute the script or task associated with the cron job
            # You can use subprocess or any other method suitable for running scripts

            # Update the cron schedule status and execution times
            cron_schedule.status = 'running'
            cron_schedule.execute_start_datetime = current_time
            cron_schedule.save()

            # Perform any necessary cleanup or logging after executing the cron job

            # Update the cron schedule status and execution times after completion
            cron_schedule.status = 'completed'
            cron_schedule.execute_end_datetime = time.strftime('%Y-%m-%d %H:%M:%S')
            cron_schedule.save()

        # Sleep for the specified interval (e.g., 15 minutes)
        time.sleep(900)  # 900 seconds = 15 minutes

if __name__ == '__main__':
    load_and_run_cron_jobs()
