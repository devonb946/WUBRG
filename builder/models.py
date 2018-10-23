import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from browse.models import Card

# Create your models here.
class Deck(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=10000, default='')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    format = models.CharField(max_length=50, default='')
    is_draft = models.BooleanField(default=True)
    card_count = models.IntegerField(default=0)
    colors = models.CharField(max_length=25, default='')
    creator = models.CharField(max_length=100, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    cards = models.ManyToManyField(Card)

# class DeckCard(models.Model):
#     deck = models.ForeignKey(Deck)
#     card = models.ForeignKey(Card)
