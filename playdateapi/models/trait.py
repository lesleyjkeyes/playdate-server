from django.db import models

class Trait(models.Model):
    title = models.CharField(max_length=50)
