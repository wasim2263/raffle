import time

from django.db import IntegrityError, transaction
from django.db.models import F
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.raffle_draw.decorators import manager_ips_only
from apps.raffle_draw.models import Raffle
from apps.raffle_draw.serializers import TicketSerializer


class WinnerApiView(APIView, PageNumberPagination):

    @method_decorator(manager_ips_only)
    def post(self, request, raffle_id=None):
        """
        Draw winners
        """
        page_size = 100

        if not raffle_id:
            return Response({'error': 'Raffle ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                update_raffle = Raffle.objects.filter(id=raffle_id, available_tickets=0, winners_drawn=False).update(
                    winners_drawn=True)
                try:
                    raffle = Raffle.objects.get(id=raffle_id)
                except Raffle.DoesNotExist:
                    return Response({'error': 'Raffle does not exist.'},
                                    status=status.HTTP_404_NOT_FOUND)
                if update_raffle > 0:
                    raffle.draw()
                    tickets = raffle.winners()
                    serializer = TicketSerializer(tickets, many=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                elif raffle.winners_drawn:
                    return Response({'error': "Winners for the raffle have already been drawn."},
                                    status=status.HTTP_403_FORBIDDEN)
                elif raffle.available_tickets > 0:
                    return Response({'error': "Winners can't be drawn when tickets are still available."},
                                    status=status.HTTP_403_FORBIDDEN)
        except IntegrityError:
            return Response({'error': 'Failed to update raffle status, please try again.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, raffle_id=None):
        """
        Get winner list
        """
        try:
            raffle = Raffle.objects.get(id=raffle_id)
        except Raffle.DoesNotExist:
            return Response({'error': 'Raffle does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if not raffle.winners_drawn:
            return Response({'error': "Winners for the raffle have not drawn yet."}, status=status.HTTP_403_FORBIDDEN)
        tickets = raffle.winners()
        results = self.paginate_queryset(tickets, request, view=self)
        serializer = TicketSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
