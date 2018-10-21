import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Deck(models.Model):
    name = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    format = models.CharField(max_length=50)
    is_draft = models.BooleanField(default=True)
    colors = models.CharField(max_length=25)
    creator = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    data = JSONField(null=False)
