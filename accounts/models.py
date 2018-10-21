from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class WubrgUser(AbstractUser):

    decks = models.JSONField()

    def __str__(self):
        return self.email

    def get_decks(self):
        return self.decks
