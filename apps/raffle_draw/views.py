# views.py
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Prize, Raffle
from .permissions import ManagerIPsOnly
from .serializers import PrizeSerializer, RaffleSerializer


class PrizeViewSet(viewsets.ModelViewSet):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer


class RaffleViewSet(viewsets.ModelViewSet):
    queryset = Raffle.objects.all()
    serializer_class = RaffleSerializer
    permission_classes = [ManagerIPsOnly]

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