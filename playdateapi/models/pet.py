from django.db import models
from .user import User

class Pet(models.Model):
    name = models.CharField(max_length=200)
    about = models.TextField()
    profile_image = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    breed = models.CharField(max_length=10)
