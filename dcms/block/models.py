from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Blocks(models.Model):
    id = models.IntegerField(primary_key=True)
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
    created_at = models.DateTimeField(_("creation date"),auto_now_add=True)
    updated_at = models.DateTimeField(_("updation date"),auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['slug']),
        ]

        
    def formatted_full_url(self):
        full_url = f"http://127.0.0.1:8000/block/cms/{self.slug}"
        return format_html('<a href="{}">{}</a>', full_url, full_url)