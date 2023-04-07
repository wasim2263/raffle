from django.db import models

# Create your models here.
class Raffle(models.Model):
    name = models.CharField(max_length=255)
    total_tickets = models.PositiveIntegerField()
    remaining_tickets = models.PositiveIntegerField()
    verification_codes = models.JSONField(default=dict)
    winners_drawn = models.BooleanField(default=False)
