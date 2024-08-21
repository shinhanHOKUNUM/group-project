from django.db import models

# Create your models here.
class Mypage(models.Model):
    user_ID = models.TextField()
    SavedWord = models.TextField()
    SavedWord_Mean = models.TextField()
