import uuid

from django.db import models

# Create your models here.
class Raffle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    winners_drawn = models.BooleanField(default=False)
