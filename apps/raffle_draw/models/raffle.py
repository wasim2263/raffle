import uuid

from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel


# Create your models here.
class Raffle(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=255)
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    winners_drawn = models.BooleanField(default=False)
