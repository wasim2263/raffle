# raffle_view.py
from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.response import Response

from apps.raffle_draw.decorators import manager_ips_only
from apps.raffle_draw.models import Prize, Raffle
from apps.raffle_draw.serializers import RaffleSerializer


class RaffleApiViewSet(viewsets.ModelViewSet):
    queryset = Raffle.objects.order_by('-created').all()
    serializer_class = RaffleSerializer
    @transaction.atomic
    @method_decorator(manager_ips_only)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Get data from request
        name = serializer.validated_data['name']
        total_tickets = serializer.validated_data['total_tickets']
        prizes_data = serializer.validated_data['prizes']
        # Create Raffle object
        raffle = Raffle(name=name, total_tickets=total_tickets, available_tickets=total_tickets)
        raffle.save()
        try:
            with transaction.atomic():
                # Create Prize objects and associate with Raffle
                for prize_data in prizes_data:
                    prize = Prize(name=prize_data['name'], amount=prize_data['amount'], raffle=raffle)
                    prize.save()
                serializer = self.get_serializer(raffle)
        except Exception as exception:
            raffle.delete()
        return Response(serializer.data, status=201)
