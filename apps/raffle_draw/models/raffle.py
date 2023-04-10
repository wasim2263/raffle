import random

from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel


class Raffle(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=255)
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    winners_drawn = models.BooleanField(default=False)

    def winners(self):
        return self.tickets.filter(prize__isnull=False, has_won=True)

    def draw(self):
        prizes = self.prizes.all()
        tickets = [ticket_number for ticket_number in range(1, self.total_tickets + 1)]
        all_winners_prize = {}
        for prize in prizes:
            prize_winners = random.sample(tickets, k=prize.amount)
            tickets = list(set(tickets) - set(prize_winners))
            for winner in prize_winners:
                # assign prize to the ticket number
                all_winners_prize[winner] = prize
        winners_tickets = self._get_winners_tickets(all_winners_prize.keys())
        self._update_winner_tickets(winners_tickets, all_winners_prize)

    def _get_winners_tickets(self, ticket_numbers):
        return self.tickets.filter(ticket_number__in=ticket_numbers)

    @staticmethod
    def _update_winner_tickets(winners_tickets, all_winners_prize):
        # To avoid circular import using it locally
        from apps.raffle_draw.models import Ticket
        for winners_ticket in winners_tickets:
            winners_ticket.prize = all_winners_prize[winners_ticket.ticket_number]
            winners_ticket.has_won = True
        Ticket.objects.bulk_update(winners_tickets, ['prize', 'has_won'], batch_size=200)
