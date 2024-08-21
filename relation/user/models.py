from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    user_ID = models.TextField()
    user_Password = models.TextField()

class