from django.db import IntegrityError, transaction
from django.db.models import F
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.raffle_draw.decorators import manager_ips_only
from apps.raffle_draw.models import Ticket, Raffle
from apps.raffle_draw.serializers import TicketSerializer


class WinnerView(APIView):
    """
    Viewset for handling raffle tickets.
    """
    @method_decorator(manager_ips_only)
    def post(self, request, raffle_id=None):
        """
        Create a raffle ticket.
        """
        if not raffle_id:
            return Response({'error': 'Raffle ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                update_raffle = Raffle.objects.filter(id=raffle_id, available_tickets=0, winners_drawn=False).update(
                    winners_drawn=True)
                if update_raffle > 0:
                    raffle = Raffle.objects.get(id=raffle_id)
                    raffle.draw()
                    tickets = raffle.winners()
                    serializer = TicketSerializer(tickets, many=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Your ip address has already participated in this raffle'},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({'error': "Winners can't be drawn when tickets are still available"}, status=status.HTTP_403_FORBIDDEN)
