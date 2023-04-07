# serializers.py
from rest_framework import serializers
from .models import Prize, Raffle

class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ('name', 'amount')

class RaffleSerializer(serializers.ModelSerializer):
    prizes = PrizeSerializer(many=True)

    class Meta:
        model = Raffle
        fields = ('id','name', 'total_tickets', 'prizes', 'available_tickets', 'winners_drawn')
        read_only_fields = ['available_tickets', 'winners_drawn']