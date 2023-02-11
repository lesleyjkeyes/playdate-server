from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    about = models.CharField(max_length=400)
    profile_image = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
