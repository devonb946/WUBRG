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
    cards = models.ManyToManyField(Card, through='DeckCard')
    sideboard_cards = models.ManyToManyField(Card, related_name='sideboard_cards', through='SideboardCard')
    art_card = models.ForeignKey(Card, related_name='art_card', on_delete=models.CASCADE, null=True)

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

class SideboardCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
