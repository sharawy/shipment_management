from rest_framework import serializers
from providers.models import Address
from providers.serializers import AddressSerializer, TrackingEventSerializer
from providers.utils import get_available_providers
from shipment.tasks import create_shipment_task
from .models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    provider = serializers.ChoiceField(choices=get_available_providers())
    to_address = AddressSerializer()
    from_address = AddressSerializer()
    tracking_events = TrackingEventSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = ['id', 'tracking_number', 'to_address', 'from_address', 'weight',
                  'no_of_items', 'description', 'provider', 'provider_response', 'label_url', 'tracking_events']
        read_only_fields = ('tracking_number', 'provider_response', 'label_url', )

    def create(self, validated_data):
        from_address = validated_data.pop('from_address')
        to_address = validated_data.pop('to_address')
        validated_data['from_address_id'] = Address.objects.create(**from_address).id
        validated_data['to_address_id'] = Address.objects.create(**to_address).id
        shipment = super().create(validated_data)
        create_shipment_task.delay(shipment.id)
        return shipment
