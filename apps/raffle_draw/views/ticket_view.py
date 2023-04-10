from django.db import IntegrityError, transaction
from django.db.models import F
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.raffle_draw.models import Ticket, Raffle
from apps.raffle_draw.serializers import TicketSerializer


class TicketApiView(APIView):
    """
    Api View for handling raffle tickets ie participants.
    """

    def post(self, request, raffle_id=None):
        """
        Create a raffle ticket.
        """
        if not raffle_id:
            return Response({'error': 'Raffle ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        client_ip = request.META.get('REMOTE_ADDR')
        try:
            with transaction.atomic():
                update_raffle = Raffle.objects.filter(id=raffle_id, available_tickets__gt=0).update(
                    available_tickets=F('available_tickets') - 1)
                if update_raffle > 0:
                    raffle = Raffle.objects.get(id=raffle_id)
                    ticket_number = raffle.total_tickets - raffle.available_tickets
                    ticket = Ticket(raffle=raffle, ticket_number=ticket_number, ip_address=client_ip)
                    ticket.save()
                    serializer = TicketSerializer(ticket)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Tickets to this raffle are no longer available.'},
                                    status=status.HTTP_410_GONE)

        except IntegrityError:
            return Response({'error': 'Your ip address has already participated in this raffle.'},
                            status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
