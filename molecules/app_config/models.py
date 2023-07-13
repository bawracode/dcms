from django.db import models

# Create your models here.
class app_config(models.Model):
    title = models.CharField(max_length=255)
    store = models.IntegerField(default=0)
    key = models.CharField(max_length=255)
    value = models.TextField()
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
