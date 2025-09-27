from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    generation_quantity = models.IntegerField(default=3)
    full_generation_quantity = models.IntegerField(default=3)
    is_consent_pop = models.BooleanField(default=False)

class QueueInfo(models.Model): 
    id = models.AutoField(primary_key=True) 
    status = models.CharField(max_length=50)  
    topic = models.CharField(max_length=150)  
    def __str__(self):
        return f"{self.topic} - {self.status}"
