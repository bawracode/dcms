from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django_quill.fields import QuillField
from django.utils import timezone
from django.conf import settings
import os
from nucleus.middelware.middleware import get_current_request
from django.contrib import messages


# Create your models here.

class Mail_template_log(models.Model):
    id = models.AutoField(primary_key=True)
    mail_template = models.CharField(_('mail_template'),max_length=250)
    action = models.CharField(_('action'),max_length=250)
    created_at = models.DateTimeField( default=timezone.now ,editable=False)
    class Meta:
        db_table = "mail_template_log"
        verbose_name = _("Mail template log")
        verbose_name_plural = _("Mail template logs")

    def __str__(self):
        return self.mail_template
    
    

class FromOption(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now,editable=False)
    updated_at = models.DateTimeField(default=timezone.now,editable=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

            
    
class Mail_template(models.Model):
    CHOICES_SEND = (
        ('cron', 'Cron'),
        ('immediately', 'Immediately'),
    )
    create_type = models.CharField(_('create type'), max_length=12, choices=(
        ('New', 'New'),
        ('Existing', 'Existing'),
    ), default='New')
    name = models.CharField(_('name'),max_length=250)
    code = models.CharField(_('code'),max_length=250,unique=True)
    subject = models.CharField(_('subject'),max_length=250)
    body = QuillField()
    status = models.CharField( _('status'), default=True ,choices=(('Active', 'Active'), ('Inactive', 'Inactive')), max_length=255)
    from_option = models.ForeignKey(FromOption, on_delete=models.SET_NULL, null=True,default=1)
    other = models.BooleanField(default=False)
    from_email = models.EmailField(_('from_email'),max_length=250,blank=True, null=True)
    cc = models.CharField(max_length=255, blank=True)
    bcc = models.CharField(max_length=255, blank=True)
    event = models.CharField(_('event'),max_length=250)
    send_option = models.CharField(max_length=12, choices=CHOICES_SEND, default='cron')
    created_at = models.DateTimeField(default=timezone.now,editable=False)
    updated_at = models.DateTimeField(default=timezone.now,editable=False)

    class Meta:
        db_table = "mail_template"
        verbose_name = _('Mail Templates')
        verbose_name_plural = _('Mail Templates')

    def __str__(self):
        return self.event
    
    def save(self, *args, **kwargs):
        # update updated_at
        print(self.from_option)
        self.updated_at = timezone.now()
        if self.other == False:
            self.from_email = FromOption.objects.get(name=self.from_option).email
        print(self.from_email)
        super().save(*args, **kwargs)
        if self.create_type == 'New':
            Mail_template_log.objects.create(mail_template=self.event,action='create')
        else:
            Mail_template_log.objects.create(mail_template=self.event,action='update')
        # base_dir = settings.BASE_DIR
        # mail_templates_dir = os.path.join(base_dir, 'templates' , 'mail')
        # if os.path.exists(mail_templates_dir):
        #     if not os.path.exists(mail_templates_dir + '/{}.html'.format(self.event)):
        #         with open(mail_templates_dir + '/{}.html'.format(self.event), 'w') as f:
        #             f.write(self.body)
        #     else:
        #         with open(mail_templates_dir + '/{}.html'.format(self.event), 'w') as f:
        #             f.write(self.body)
        # else:
        #     print('mail_templates_dir not exists')
        #     os.mkdir(mail_templates_dir)
        #     with open(mail_templates_dir + '/{}.html'.format(self.event), 'w') as f:
        #         f.write(self.body)

    def delete(self, *args, **kwargs):
        Mail_template_log.objects.create(mail_template=self.event,action='delete')
        base_dir = settings.BASE_DIR
        mail_templates_dir = os.path.join(base_dir, 'templates' , 'mail' , self.event + '.html')
        if os.path.exists(mail_templates_dir):
            os.remove(mail_templates_dir)
        
        Mail_template.objects.filter(id=self.id).delete()
        return

class Configure_SMTP(models.Model):
    host = models.EmailField(_('host'),max_length=250)
    port = models.IntegerField(_('port'),default=587)
    username = models.CharField(_('username'),max_length=250)
    password = models.CharField(_('password'),max_length=250)
    active = models.BooleanField(_('active'),default=True)
    created_at = models.DateTimeField(default=timezone.now,editable=False)
    updated_at = models.DateTimeField(default=timezone.now,editable=False)

    class Meta:
        db_table = "configure_smtp"

    def save(self, *args, **kwargs):
        if not self.pk and Configure_SMTP.objects.exists():
            messages.error(get_current_request(), "Creation of the SMTP configuration is not allowed.")
            return
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        messages.error(get_current_request(), "Deletion of the SMTP configuration is not allowed.")
        return

    class Meta:
        verbose_name = _('SMTP Configuration')
        verbose_name_plural = _('SMTP Configurations')

    def __str__(self):
        return self.host


class Scheduled_mail(models.Model):
    event = models.CharField(_('event'),max_length=250)
    html_content = models.TextField( _('html_content'),blank=True, null=True)
    subject = models.CharField(_('subject'),max_length=250)
    from_email = models.EmailField(_('from_email'),max_length=250,blank=True, null=True)
    recipient_list = models.TextField(_('recipient_list'),blank=True, null=True)
    cc = models.CharField(max_length=255, blank=True)
    bcc = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "scheduled_mail"
        verbose_name = _('Scheduled Mail')
        verbose_name_plural = _('Scheduled Mails')