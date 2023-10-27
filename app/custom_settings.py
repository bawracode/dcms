from app.settings import *
from nucleus.mail.models import Configure_SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = Configure_SMTP.objects.get(active=True).host
EMAIL_PORT = Configure_SMTP.objects.get(active=True).port
EMAIL_HOST_USER = Configure_SMTP.objects.get(active=True).username
EMAIL_HOST_PASSWORD = Configure_SMTP.objects.get(active=True).password

