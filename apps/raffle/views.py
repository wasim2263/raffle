# views.py
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response

from project.settings import  MANAGER_IPS
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

    def create(self, request, *args, **kwargs):
        client_ip=request.META.get('REMOTE_ADDR')
        manager_ips =MANAGER_IPS
        if client_ip not in manager_ips:
            # Raise an error or return a response indicating that the client IP is not allowed
            raise serializers.ValidationError(
                "Access denied. Client IP is not allowed to access raffle manager endpoints.")

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
