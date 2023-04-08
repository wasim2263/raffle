from django.db import IntegrityError, transaction
from django.db.models import F
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_410_GONE, HTTP_201_CREATED, HTTP_403_FORBIDDEN

from apps.raffle_draw.models import Ticket, Prize, Raffle
from apps.raffle_draw.serializers import TicketSerializer


class TicketViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    """
    Viewset for handling raffle tickets.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, raffle_id=None):
        """
        Create a raffle ticket.
        """
        if not raffle_id:
            return Response({'error': 'Raffle ID is required.'}, status=HTTP_400_BAD_REQUEST)

        client_ip = request.META.get('REMOTE_ADDR')
        try:
            with transaction.atomic():
                update_raffle = Raffle.objects.filter(id=raffle_id, available_tickets__gt=0).update(
                    available_tickets=F('available_tickets') - 1)
                if update_raffle > 0:
                    raffle = Raffle.objects.get(id=raffle_id)
                    ticket_number = raffle.total_tickets - raffle.available_tickets
                    # Create Prize objects and ass
                    ticket = Ticket(raffle=raffle, ticket_number=ticket_number, ip_address=client_ip)
                    ticket.save()
                    serializer = self.get_serializer(ticket)
                    return Response(serializer.data, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Your ip address has already participated in this raffle'},
                            status=HTTP_403_FORBIDDEN)
        return Response({'error': 'Tickets to this raffle are no longer available'}, status=HTTP_410_GONE)
