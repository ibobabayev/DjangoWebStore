from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/',verbose_name='аватар',null=True,blank=True)
    phone = models.CharField(max_length=20,verbose_name='номер телефона',null=True,blank=True)
    country = models.CharField(max_length=40,verbose_name='страна',null=True,blank=True)

    username = None
    email = models.EmailField(unique=True,verbose_name='почта')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
