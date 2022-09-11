from typing import Union

from django.db import models, transaction

# Create your models here.
from django_extensions.db.models import TimeStampedModel

from . import ShipmentStatuses


class TrackingEvent(TimeStampedModel):
    status = models.CharField(
        max_length=25, choices=ShipmentStatuses.CHOICES, default=ShipmentStatuses.PENDING
    )
    message = models.TextField(blank=True, null=True)


class Address(TimeStampedModel):
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=3)
    country = models.CharField(max_length=4)
    postal_code = models.CharField(max_length=5)


class BaseShipment(TimeStampedModel):
    """
    Represents a single shipment. .
    """

    tracking_number = models.CharField(max_length=255, blank=True)
    to_address = models.ForeignKey(Address,related_name='receiver_address', on_delete=models.PROTECT)
    from_address = models.ForeignKey(Address,related_name='sender_address', on_delete=models.PROTECT)
    weight = models.DecimalField(max_digits=9, decimal_places=2, default="0.0")
    no_of_items = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, default="")
    provider = models.CharField(max_length=256, blank=True)
    provider_response = models.TextField(null=True, blank=True)
    tracking_events = models.ManyToManyField(TrackingEvent)
    label_url = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    @transaction.atomic()
    def change_status(self, status: Union[ShipmentStatuses, str], message=None, provider_response=None):
        """
        Updates the shipment status.
        """
        self.provider_response = provider_response
        self.tracking_events.create(status=status, message=message, shipment=self)
        self.save(update_fields=["provider_response"])

    def add_tracking_number(self, tracking_number: str, provider, label_url=None):
        self.tracking_number = tracking_number
        self.provider = provider
        self.label_url = label_url if label_url else self.label_url
        self.save(update_fields=["tracking_number", 'provider', 'label_url'])

