from django.core.signing import Signer
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from apps.raffle_draw.decorators import manager_ips_only
from apps.raffle_draw.models import Ticket, Raffle
from apps.raffle_draw.serializers import TicketSerializer


class VerifyTicketAPIView(APIView):
    def post(self, request, raffle_id=None):
        ticket_number = request.data.get('ticket_number')
        verification_code = request.data.get('verification_code')
        signer = Signer()
        verification_code = signer.sign(verification_code)

        if not ticket_number or not verification_code:
            return Response({'error': 'Ticket number and verification code are required.'}, status=HTTP_400_BAD_REQUEST)
        try:
            Raffle.objects.get(id=raffle_id, winners_drawn=True)
        except Raffle.DoesNotExist:
            return Response({'error': 'Winners for the raffle have not been drawn yet.'}, status=HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(raffle_id=raffle_id, ticket_number=ticket_number,
                                        verification_code=verification_code)
        except Ticket.DoesNotExist:
            return Response({'error': 'Invalid verification code.'}, status=HTTP_400_BAD_REQUEST)

        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=HTTP_200_OK)
