from django.db import models

class ITKeyword(models.Model):
    term = models.CharField(max_length=255)
    term_en = models.CharField(max_length=255)
    term_ko = models.CharField(max_length=255)
    mean = models.TextField()

    def __str__(self):
        return self.term