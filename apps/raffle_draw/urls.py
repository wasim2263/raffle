from django.urls import path, include
from apps.raffle_draw.views import TicketApiView, RaffleApiViewSet, WinnerApiView, VerifyTicketAPIView
from project.urls import router

router.register(r'', RaffleApiViewSet)

urlpatterns = [
    path('<uuid:raffle_id>/participate/', TicketApiView.as_view(), name='raffle-tickets'),
    path('<uuid:raffle_id>/winners/', WinnerApiView.as_view(), name='raffle-winners'),
    path('<uuid:raffle_id>/verify-ticket/', VerifyTicketAPIView.as_view(), name='raffle-ticket-verify'),
    path('', include(router.urls)),

]
