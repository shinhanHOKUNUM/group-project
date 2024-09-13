from django.db import models


# Create your models here.

class AIDictionary(models.Model):
    term = models.CharField(max_length=100)
    term_en = models.CharField(max_length=100, blank=True, null=True)
    term_kor = models.CharField(max_length=100, blank=True, null=True)
    mean = models.TextField(blank=True, null=True)
    detail_mean = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.term