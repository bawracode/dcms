from django.core.mail import send_mail
from .models import *
from django.core.mail import EmailMultiAlternatives
import smtplib
from nucleus.mail.cronjob.cron import send_mail_cron
import logging
import datetime,os,random

logger = logging.getLogger(__name__)

class Mail:
    @staticmethod
    def send_email(event,recipient_list):
        recipient_list = recipient_list.replace('\n','').split(',')
        
        base_dir = settings.BASE_DIR
        log_directory = os.path.join(base_dir, 'nucleus','mail','log')
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file_path = os.path.join(log_directory, current_date , f"{event}.log")
        random_number = random.randint(1, 1000)


        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        
        if Mail_template.objects.filter(event=event).exists() and Mail_template.objects.get(event=event).status == 'Active':        
            html_content = Mail_template.objects.get(event=event).body
            subject = Mail_template.objects.get(event=event).subject
            from_email = Mail_template.objects.get(event=event).from_email
            text_content = "This is an important message."
            
            cc = Mail_template.objects.get(event=event).cc.replace('\n','').split(',')
            bcc = Mail_template.objects.get(event=event).bcc.replace('\n','').split(',')
            msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list , bcc=bcc, cc=cc)
            msg.attach_alternative(html_content, "text/html") 
            if Mail_template.objects.get(event=event).send_option == "immediately":
                try:
                    msg.send()
                    log_message = f"[{datetime.datetime.now()}] [Random: {random_number}] Mail send for {event} to {recipient_list} immediately from {from_email}" 
                    with open(log_file_path, 'a') as file:
                        file.write(log_message + '\n')
                    return True 
            
                except Exception as e:
                    log_message = f"[{datetime.datetime.now()}] [Random: {random_number}] Mail --not-- send for {event} to {recipient_list} from {from_email} immediately due to {e}" 
                    with open(log_file_path, 'a') as file:
                        file.write(log_message + '\n')
                    return False 
                
            else:
                print("Mail send option is not immediately")
                Scheduled_mail.objects.create(event=event,html_content=html_content,subject=subject,from_email=from_email,recipient_list=recipient_list,cc=','.join(cc),bcc=','.join(bcc))
                return True
                
                

        else:
            print("Mail template not found or Not Active Please create mail template first")
            return False

