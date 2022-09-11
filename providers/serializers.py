from rest_framework import serializers

from .models import Address, TrackingEvent


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'street', 'city', 'country', 'state', 'postal_code')


class TrackingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingEvent
        fields = ('id', 'status', 'message')
