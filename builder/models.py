import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from browse.models import Card

class DeckManager(models.Manager):
    def create_deck(self, name, description, format, card_count, sideboard_card_count, colors, creator, date_created, cards, sideboard_cards, art_card):
        deck = self.create(
            name=name,
            description=description,
            id=uuid.uuid4(),
            format=format,
            is_draft=True,
            card_count=card_count,
            sideboard_card_count=sideboard_card_count,
            colors=colors,
            creator=creator,
            date_created=date_created,
            art_card=art_card)

        # to copy cards over, we must create a new relationship model
        # for each one
        for card in cards:
            try:
                dc = DeckCard.objects.get(deck=deck, card=card)
            except DeckCard.DoesNotExist:
                dc = DeckCard(deck=deck, card=card, count=0)
            dc.count += 1
            dc.save()

        for sideboard_card in sideboard_cards:
            try:
                sc = SideboardCard.objects.get(deck=deck, card=card)
            except SideboardCard.DoesNotExist:
                sc = SideboardCard(deck=deck, card=card, count=0)
            sc.count += 1
            sc.save()

        return deck

class Deck(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=10000, default='')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    format = models.CharField(max_length=50, default='')
    is_draft = models.BooleanField(default=True)
    card_count = models.IntegerField(default=0)
    sideboard_card_count = models.IntegerField(default=0)
    colors = models.CharField(max_length=25, default='')
    creator = models.CharField(max_length=100, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    cards = models.ManyToManyField(Card, through='DeckCard')
    sideboard_cards = models.ManyToManyField(Card, related_name='sideboard_cards', through='SideboardCard')
    art_card = models.ForeignKey(Card, related_name='art_card', on_delete=models.CASCADE, null=True)
    objects = DeckManager()

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

class SideboardCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
