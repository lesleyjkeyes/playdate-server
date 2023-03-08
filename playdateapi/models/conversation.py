from django.db import models
from .user import User

class Conversation(models.Model):
    user_one = models.ForeignKey(User, related_name='user_one', on_delete=models.CASCADE)
    user_two = models.ForeignKey(User, related_name='user_two', on_delete=models.CASCADE)
