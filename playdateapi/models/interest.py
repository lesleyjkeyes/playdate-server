from django.db import models

class Interest(models.Model):
    title = models.CharField(max_length=50)
