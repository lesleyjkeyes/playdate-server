from django.db import models
from .interest import Interest
from .pet import Pet

class PetInterest(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
