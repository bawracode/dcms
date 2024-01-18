from django.core.mail import EmailMultiAlternatives
import logging
from django.core.mail import EmailMultiAlternatives
import logging
import datetime,os,random
from django.conf import settings
from nucleus.mail.models import *

logger = logging.getLogger(__name__)

def send_mail_cron(event,html_content,subject,from_email,recipient_list,cc,bcc):
    base_dir = settings.BASE_DIR
    log_directory = os.path.join(base_dir, 'nucleus','mail','log')
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join(log_directory, current_date , f"{event}.log")
    random_number = random.randint(1, 1000)
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    msg = EmailMultiAlternatives(subject, html_content, from_email, [recipient_list] , bcc=[bcc], cc=[cc])
    msg.attach_alternative(html_content, "text/html")
    try:

        msg.send()
        log_message = f"[{datetime.datetime.now()}] [Random: {random_number}] Mail send for {event} to {recipient_list} by cron"
        with open(log_file_path, 'a') as file:
            file.write(log_message + '\n')
        return True

    except Exception as e:
        # print error of mail
        log_message = f"[{datetime.datetime.now()}] [Random: {random_number}] Mail --not-- send for {event} to {recipient_list} by cron due to {e}"
        with open(log_file_path, 'a') as file:
            file.write(log_message + '\n')
        return False

def execute_cron_job():
    if Scheduled_mail.objects.all().exists() and Scheduled_mail.objects.all().count() > 0: 
        for object in Scheduled_mail.objects.all():
            print("cron job is running for email...")
            send_mail_cron(object.event,object.html_content,object.subject,object.from_email,object.recipient_list.split(',') ,object.cc.split(','),object.bcc.split(','))
            object.delete() 