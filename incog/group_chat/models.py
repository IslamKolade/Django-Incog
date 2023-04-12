from django.db import models
from datetime import datetime
# Create your models here.
class Group_Chat(models.Model):
    group_name = models.CharField(max_length=1000)

class Group_Messages(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=1000000)
    group_name = models.CharField(max_length=1000000)



