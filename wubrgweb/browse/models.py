from django.db import models
import uuid

# Create your models here.
class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cmc = models.DecimalField(decimal_places=3,max_digits=15)
    loyalty = models.CharField(max_length=10)
    mana_cost = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    oracle_text = models.TextField()
    power = models.CharField(max_length=10)
    reserved = models.BooleanField(default=False)
    toughness = models.CharField(max_length=10)
    type_line = models.CharField(max_length=75)
    artist = models.CharField(max_length=75)
    collector_number = models.CharField(max_length=75)
    flavor_text = models.TextField()
    image = models.URLField()
    set = models.CharField(max_length=3)
    set_name = models.CharField(max_length=50)

    RARITY_CHOICES = (
        ('1', 'Common'),
        ('2', 'Uncommon'),
        ('3', 'Rare'),
        ('4', 'Mythic'),
    )
    rarity = models.CharField(
        max_length=1,
        choices=RARITY_CHOICES,
        default='1',
    )

    FRAME_CHOICES = (
        ('1', '1993'),
        ('2', '1997'),
        ('3', '2003'),
        ('4', '2015'),
        ('F', 'Future'),
    )
    frame = models.CharField(
        max_length=1,
        choices=FRAME_CHOICES,
        default='4',
    )

    BORDER_COLOR_CHOICES = (
        ('B', 'Black'),
        ('N', 'Borderless'),
        ('G', 'Gold'),
        ('S', 'Silver'),
        ('W', 'White'),
    )
    border_color = models.CharField(
        max_length=1,
        choices=BORDER_COLOR_CHOICES,
        default='B',
    )

    LAYOUT_CHOICES = (
        ('NRML', 'Normal'),
        ('SPLT', 'Split'),
        ('FLIP', 'Flip'),
        ('TRFM', 'Transform'),
        ('MELD', 'Meld'),
        ('LVLR', 'Leveler'),
        ('SAGA', 'Saga'),
        ('PLNR', 'Planar'),
        ('SCHM', 'Scheme'),
        ('VGRD', 'Vanguard'),
        ('TOKN', 'Token'),
        ('DFTK', 'Double-Faced Token'),
        ('EMBL', 'Emblem'),
        ('AGMT', 'Augment'),
        ('HOST', 'Host'),
    )
    layout = models.CharField(
        max_length=4,
        choices=LAYOUT_CHOICES,
        default='NRML',
    )

    def __str__(self):
        return self.name


    # TODO: Make sure everything works with array-like entries
    #colors
    #color_identity
    #color_indicator
    #legalities
    #image_uris

    # TODO: Make sure everything works for cards with unuasual faces/layouts
    #multiverse_ids
    #all_parts
    #card_faces
