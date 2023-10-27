from django.contrib import admin
from .models import *
from django import forms
from django.conf import settings
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django.forms import ModelForm
from nucleus.mail.mail import Mail
from ckeditor.widgets import CKEditorWidget




base_dir = settings.BASE_DIR
class ToggleSwitchWidget(forms.CheckboxInput):
    template_name = os.path.join(base_dir,'templates','widgest','toggle_switch.html')

class Smtpform(ModelForm):
    
    class Meta:
        model = Configure_SMTP
        fields = "__all__"
        widgets = {
            "active": DjangoToggleSwitchWidget(round=True,),
        }



class mail_form(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Mail_template
        fields = '__all__'
    # body = forms.CharField(
    #     widget=forms.Textarea(attrs={'rows': 30, 'cols': 100}),
    # )

    # class Meta:
    #     model = Mail_template
    #     fields = '__all__'
    #     # widgets = {
    #     #     "other": DjangoToggleSwitchWidget(round=True,),
    #     # }


@admin.register(Mail_template)
class Mail_templateAdmin(admin.ModelAdmin):
    # form = mail_form
    actions = None 
    change_form_template = 'admin/mail_template_change_form.html'
    list_display = ('name','code','subject','status','from_option','from_email','cc','bcc','event','send_option','created_at','updated_at')
    prepopulated_fields = {'event': ('name',)}

@admin.register(Mail_template_log)
class Mail_template_logAdmin(admin.ModelAdmin):
    # actions = None
    list_display = ('mail_template','action','created_at')
    list_filter = ('mail_template','action','created_at')

# Register your models here.
@admin.register(FromOption)
class FromOptionAdmin(admin.ModelAdmin):
    actions = None 
    list_display = ('name','email','created_at','updated_at')

@admin.register(Configure_SMTP)
class Configure_SMTPAdmin(admin.ModelAdmin):
    form = Smtpform
    actions = None
    list_display = ('host','port','username','password','active','created_at','updated_at')

# Mail.send_email('order','jashkk5@gmail.com') 

@admin.register(Scheduled_mail)
class Scheduled_mailAdmin(admin.ModelAdmin):
    actions = None 
    list_display = ('event','html_content','subject','from_email','recipient_list','cc','bcc')
    list_filter = ('event','html_content','subject','from_email','recipient_list','cc','bcc')

