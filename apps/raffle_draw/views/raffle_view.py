# raffle_view.py
from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.raffle_draw.decorators import manager_ips_only
from apps.raffle_draw.models import Raffle
from apps.raffle_draw.serializers import RaffleSerializer


class RaffleApiViewSet(viewsets.ModelViewSet):
    queryset = Raffle.objects.order_by('-created')
    serializer_class = RaffleSerializer

    @method_decorator(manager_ips_only)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Get data from request
        name = serializer.validated_data['name']
        total_tickets = serializer.validated_data['total_tickets']
        prizes_data = serializer.validated_data['prizes']
        # Create Raffle object
        try:
            with transaction.atomic():
                # can be used get_or_create if considered uniqueness. lot of options to consider
                raffle = Raffle(name=name, total_tickets=total_tickets, available_tickets=total_tickets)
                raffle.save()
                # Create Prize objects and associate with Raffle
                raffle.store_prizes(prizes_data)
                serializer = self.get_serializer(raffle)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response(serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
