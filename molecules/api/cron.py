from django_cron import CronJobBase, Schedule
from pathlib import Path
import os

class ClearAPILogsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Run once a day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'molecules.api.clear_api_logs_cron_job'  # A unique code for the cron job

    def do(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        # Add your logic to clear the API logs here
        # This code will run at the specified schedule
        log_dir = os.path.join(base_dir, 'data','logs')
        if os.path.exists(log_dir):
            # delete all folders and its files
            for folder in os.listdir(log_dir):
                folder_path = os.path.join(log_dir, folder)
                if os.path.isdir(folder_path):
                    for file in os.listdir(folder_path):
                        os.remove(os.path.join(folder_path, file))
                    os.rmdir(folder_path)

        pass
