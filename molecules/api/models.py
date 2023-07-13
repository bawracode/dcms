from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.CharField(max_length=100)
    def __str__(self):
        return self.title
    
class SystemConfig(models.Model):
    api_name = models.CharField(max_length=100)
    config_value = models.BooleanField(default=False)
    def __str__(self):
        return self.api_name