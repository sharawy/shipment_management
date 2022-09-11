from rest_framework import generics

from .models import Shipment
from .serializers import ShipmentSerializer


class ShipmentViewSet(generics.CreateAPIView, generics.ListAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
