from django.db import models

from apps.raffle.models.raffle import Raffle


# Create your models here.
class Prize(models.Model):
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
