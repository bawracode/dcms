from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from nucleus.middelware.middleware import get_current_request
from molecules.cms.cms_logs.models import *


# Create your models here.
class Blocks(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255, db_index=True, unique=False)
    content = models.TextField()
    status = models.IntegerField(default = 1,
                                   blank = True,
                                    null = True,
                                    help_text ='1->Active, 0->Inactive', 
                                    choices =(
                                    (1, 'Active'), (0, 'Inactive')
                                    ))
    block_status = models.IntegerField(default = 1,
                                   blank = True,
                                    null = True,
                                    help_text ='1 - system_define, 0 - custom_define', 
                                    choices =(
                                    (1, 'system_define'), (0, 'custom_define')
                                    ))
    created_at = models.DateTimeField(_("creation date"), editable=False, default=timezone.now)
    updated_at = models.DateTimeField(_("updation date"), editable=False, default=timezone.now)
    class Meta:
        indexes = [
            models.Index(fields=['slug']),
        ]

        
    def save(self, *args, **kwargs):
        request = get_current_request()
        if request and request.user.is_staff:
            # Create a Blocklog instance when the current model is created by an admin
            admin_username = request.user.username
            BlockLog.objects.create(user=admin_username, action=f"Block {self.slug} created", ip_address=request.META.get('REMOTE_ADDR'))

        super().save(*args, **kwargs)
    def formatted_full_url(self):
        full_url = f"http://127.0.0.1:8000/cms/block/{self.slug}"
        return format_html('<a href="{}">{}</a>', full_url, full_url)