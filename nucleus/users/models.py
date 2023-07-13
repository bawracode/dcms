from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserPrefrenceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    json_data = models.JSONField()
    model_path=models.CharField(max_length=100)
    def __str__(self) -> str:
        return str(self.user) + "\t-\t" +str(self.model_path)