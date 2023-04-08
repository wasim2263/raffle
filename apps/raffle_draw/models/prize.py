import uuid

from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel

from apps.raffle_draw.models.raffle import Raffle


# Create your models here.
class Prize(UUIDModel,TimeStampedModel):
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, null=True,blank=True, related_name='prizes')
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
