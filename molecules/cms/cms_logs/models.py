from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class PageLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(_("creation date"), editable=False, default=timezone.now)
    updated_at = models.DateTimeField(_("updation date"), editable=False, default=timezone.now)
    def __str__(self):
        return f"{self.user.username} - {self.action}"

class BlockLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(_("creation date"), editable=False, default=timezone.now)
    updated_at = models.DateTimeField(_("updation date"), editable=False, default=timezone.now)
    def __str__(self):
        return f"{self.user.username} - {self.action}"
