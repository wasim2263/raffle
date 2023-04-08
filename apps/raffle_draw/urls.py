from django.urls import path, include
from apps.raffle_draw.views import TicketView, RaffleViewSet, WinnerView
from project.urls import router

router.register(r'', RaffleViewSet)

urlpatterns = [
    path('<uuid:raffle_id>/participate/', TicketView.as_view(), name='raffle-tickets'),
    path('<uuid:raffle_id>/winners/', WinnerView.as_view(), name='raffle-tickets'),
    path('', include(router.urls)),

]
