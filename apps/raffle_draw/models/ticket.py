import time
import uuid

from django.core.signing import Signer
from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel

from apps.raffle_draw.models import Raffle, Prize


def generate_verification_code():
    """Generate a unique string based on timestamps."""
    timestamp = float(time.time())
    unique_string = str(timestamp).replace('.', '')[-12:]

    return unique_string


class Ticket(UUIDModel,TimeStampedModel):
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE, related_name='tickets')
    ticket_number = models.PositiveIntegerField()
    verification_code = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=255)
    prize = models.ForeignKey(Prize, on_delete=models.SET_NULL, blank=True, null=True)
    has_won = models.BooleanField(default=False)

    class Meta:
        unique_together = (('raffle', 'verification_code'), ('raffle', 'ip_address'), ('raffle', 'ticket_number'))

    def save(self, *args, **kwargs):
        """Override the save method to generate and save verification code."""
        if not self.verification_code:
            signer = Signer()
            self.verification_code = signer.sign(generate_verification_code())
        super(Ticket, self).save(*args, **kwargs)
