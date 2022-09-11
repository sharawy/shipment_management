import logging

from celery import shared_task

from providers.providers import CourierProviderFacade
from shipment.models import Shipment

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def create_shipment_task(self, shipment_id):
    try:
        shipment = Shipment.objects.get(pk=shipment_id)
        CourierProviderFacade(shipment.provider).create_tracking_number(shipment)
    except Exception as e:
        logger.error('exception raised, it would be retry after 5 seconds')
        raise self.retry(exc=e, countdown=5)
