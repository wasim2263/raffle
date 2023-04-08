import random

from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel


# Create your models here.
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
                all_winners_prize[winner] = prize
        winners_tickets = self.__get_winners_tickets(all_winners_prize.keys())
        self.__update_winner_tickets(winners_tickets, all_winners_prize)
        # print(winners_tickets)

    def __get_winners_tickets(self, ticket_numbers):
        return self.tickets.filter(ticket_number__in=ticket_numbers)

    def __update_winner_tickets(self, winners_tickets, all_winners_prize):
        from apps.raffle_draw.models import Ticket
        for winners_ticket in winners_tickets:
            winners_ticket.prize = all_winners_prize[winners_ticket.ticket_number]
            winners_ticket.has_won=True
        Ticket.objects.bulk_update(winners_tickets, ['prize', 'has_won'])
