from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class List(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, default="")
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False, blank=True, null=True)
    parent = models.ForeignKey(List, on_delete=models.CASCADE, null=True, related_name="tasks")

    def __str__(self):
        return self.title


