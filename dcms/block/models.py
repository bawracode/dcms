from django.db import models

# Create your models here.
class Block(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=200,unique=True)
    content = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['slug']),
        ]
