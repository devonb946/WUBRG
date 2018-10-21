from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from builder.models import Deck

# Create your models here.
class WubrgUser(AbstractUser):
    decks = models.ManyToManyField(Deck)
