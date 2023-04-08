import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from apps.raffle_draw.models.raffle import Raffle


# Create your models here.
class Prize(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, null=True,blank=True, related_name='prizes')
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
