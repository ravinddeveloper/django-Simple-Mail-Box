from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid

# Create your models here.
class mail_data(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    u_id=models.UUIDField(default=uuid.uuid4,unique=True,null=True)
    r_email=models.EmailField(max_length=50)
    subject=models.CharField(max_length=500,default='none')
    msg=models.TextField(default="none")
    date=models.DateField(auto_now=True)
    read=models.BooleanField(default=False)
    reply=models.BooleanField(default=False)
    reply_msg=models.TextField(default="none")
   

    def __str__(self):
        return self.user.username
    
class user_verify(models.Model):
    user=models.CharField(max_length=500,default='none',unique=True)
    verify=models.BooleanField(default=False)
