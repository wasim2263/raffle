# serializers.py
from django.core.signing import Signer
from rest_framework import serializers
from .models import Prize, Raffle, Ticket


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ('name', 'amount')


class RaffleSerializer(serializers.ModelSerializer):
    prizes = PrizeSerializer(many=True)

    class Meta:
        model = Raffle
        fields = ('id', 'name', 'total_tickets', 'prizes', 'available_tickets', 'winners_drawn')
        read_only_fields = ['available_tickets', 'winners_drawn']

    def validate(self, data):
        """
            Check total prize doesn't exceed the total tickets.
        """
        validated_data = super().validate(data)
        if len(data['prizes']) == 0:
            raise serializers.ValidationError("No prizes")
        prize_count = 0
        for prize in data['prizes']:
            prize_count += prize['amount']
            if prize_count > data['total_tickets']:
                raise serializers.ValidationError("Too many prizes")

        return validated_data


class VerificationCodeField(serializers.Field):
    def to_representation(self, value):
        signer = Signer()
        return signer.unsign(value)


class PrizeField(serializers.Field):
    def to_representation(self, prize):
        if prize:
            return prize.name
        return None


class TicketSerializer(serializers.ModelSerializer):
    prize = PrizeField(read_only=True)
    verification_code = VerificationCodeField(read_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'ticket_number', 'verification_code', 'ip_address', 'prize', 'raffle_id', 'has_won')
