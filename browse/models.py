import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    data = JSONField(null=False)
