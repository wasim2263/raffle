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
        fields = ('id', 'name', 'total_tickets', 'prizes', 'available_tickets', 'winners_drawn')
        read_only_fields = ['available_tickets', 'winners_drawn']

    def validate(self, data):
        validated_data = super().validate(data)
        """
        Check total prize doesn't exceed the total tickets.
        """
        if len(data['prizes']) == 0:
            raise serializers.ValidationError("No prizes")
        prize_count = 0
        for prize in data['prizes']:
            prize_count += prize['amount']
            if prize_count > data['total_tickets']:
                raise serializers.ValidationError("Too many prizes")

        return validated_data
