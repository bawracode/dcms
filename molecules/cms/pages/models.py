from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.html import format_html
from nucleus.middelware.middleware import get_current_request

from molecules.cms.cms_logs.models import *



# Create your models here.
# id
# title
# slug
# content
# status
# created_at
# updated_at

class CustomPage(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255, db_index=True, unique=False)
    content = models.TextField(_('content'), blank=True, null=True)
    status = models.IntegerField(default = 1,
                                   blank = True,
                                    null = True,
                                    help_text ='1->Active, 0->Inactive', 
                                    choices =(
                                    (1, 'Active'), (0, 'Inactive')
                                    ))
    created_at = models.DateTimeField(_("creation date"), editable=False, default=timezone.now)
    updated_at = models.DateTimeField(_("updation date"), editable=False, default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        request = get_current_request()
        if request and request.user.is_staff:
            # Create a PageLog instance when the current model is created by an admin
            admin_username = request.user.username
            PageLog.objects.create(user=admin_username, action=f"Page {self.slug} created", ip_address=request.META.get('REMOTE_ADDR'))

        super().save(*args, **kwargs)

    def formatted_full_url(self):
        full_url = f"http://127.0.0.1:8000/cms/pages/{self.slug}"
        return format_html('<a href="{}">{}</a>', full_url, full_url)