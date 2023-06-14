from django.db import models
from tinymce import models as tinymce_models

# Create your models here.
class Blocks(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(("title"), max_length=255)
    slug = models.SlugField(("slug"), max_length=255, db_index=True, unique=False)
    content = tinymce_models.HTMLField()
    status = models.IntegerField(default = 1,
                                   blank = True,
                                    null = True,
                                    help_text ='1->Active, 0->Inactive', 
                                    choices =(
                                    (1, 'Active'), (0, 'Inactive')
                                    ))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['slug']),
        ]
