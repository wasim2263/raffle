import time
import uuid

from django.core.signing import Signer
from django.db import models

from apps.raffle_draw.models import Raffle, Prize


def generate_verification_code():
    """Generate a unique string based on timestamps."""
    # Get the current timestamp
    timestamp = float(time.time())

    # Convert the timestamp to a string
    unique_string = str(timestamp).replace('.', '')[-12:]

    return unique_string


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    ticket_number = models.PositiveIntegerField()
    verification_code = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=255)
    prize = models.ForeignKey(Prize, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        unique_together = ('raffle', 'verification_code')

    def save(self, *args, **kwargs):
        """Override the save method to generate and save verification code."""
        if not self.verification_code:
            signer = Signer()
            self.verification_code = signer.sign(generate_verification_code())
        super(Ticket, self).save(*args, **kwargs)
