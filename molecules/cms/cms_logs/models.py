from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

class PageLog(models.Model):
    user = models.CharField(_("user"), max_length=255)
    actions = models.CharField(_("action"), max_length=255)
    ip_address = models.GenericIPAddressField(_("ip address"))
    created_at = models.DateTimeField(_("creation date"), editable=False, default=timezone.now)
    updated_at = models.DateTimeField(_("updation date"), editable=False, default=timezone.now)
    def __str__(self):
        return f"{self.user} - {self.actions} - {self.created_at}"

class BlockLog(models.Model):
    user = models.CharField(_("user"), max_length=255)
    actions = models.CharField(_("action") ,max_length=255)
    ip_address = models.GenericIPAddressField(_("ip address"))
    created_at = models.DateTimeField(_("creation date"), editable=False, default=timezone.now)
    updated_at = models.DateTimeField(_("updation date"), editable=False, default=timezone.now)
    def __str__(self):
        return f"{self.user} - {self.actions} - {self.created_at}"
