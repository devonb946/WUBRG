import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField

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
    data = JSONField(null=False, default=list)
