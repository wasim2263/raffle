# views.py
from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.response import Response

from .decorators import manager_ips_only
from .models import Prize, Raffle
from .serializers import PrizeSerializer, RaffleSerializer


class PrizeViewSet(viewsets.ModelViewSet):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer


class RaffleViewSet(viewsets.ModelViewSet):
    queryset = Raffle.objects.order_by('-created').all()
    serializer_class = RaffleSerializer

    @method_decorator(manager_ips_only)
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prizes_data = serializer.validated_data.pop('prizes')
        # Get data from request
        name = serializer.validated_data['name']
        total_tickets = serializer.validated_data['total_tickets']

        # Create Raffle object
        raffle = Raffle(name=name, total_tickets=total_tickets, available_tickets=total_tickets)
        raffle.save()
        # Create Prize objects and associate with Raffle
        for prize_data in prizes_data:
            prize = Prize(name=prize_data['name'], amount=prize_data['amount'], raffle=raffle)
            prize.save()
        serializer = self.get_serializer(raffle)
        return Response(serializer.data, status=201)
