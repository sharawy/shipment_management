from django.urls import path, include
from rest_framework import routers

from . import viewsets

router = routers.SimpleRouter()
# router.register(r'shipments', viewsets.ShipmentViewSet)

urlpatterns = [
    path('shipments/', viewsets.ShipmentViewSet.as_view(), name='shipment_api')

]

