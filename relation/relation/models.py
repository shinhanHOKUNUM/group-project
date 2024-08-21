from django.db import models

# Create your models here.
class Relation(models.Model):
    user_ID = models.TextField()
    user_name = models.TextField()