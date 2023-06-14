from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from static.tinymce import models as tinymce_models



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
    content = tinymce_models.HTMLField()
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
