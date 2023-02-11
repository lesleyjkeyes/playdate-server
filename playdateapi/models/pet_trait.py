from django.db import models
from .trait import Trait
from .pet import Pet

class PetTrait(models.Model):
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
