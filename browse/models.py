from django.db import models

# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=150)
    set = models.CharField(max_length=4)
    collector_number = models.CharField(max_length=75)

    def __str__(self):
        return self.name

class image_uris(models.Model):
    small = models.URLField()
    normal = models.URLField()
    large = models.URLField()
    png = models.URLField()
    art_crop = models.URLField()
    border_crop = models.URLField()

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
