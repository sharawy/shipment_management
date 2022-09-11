from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class ShipmentStatuses:
    PENDING = "Pending"
    READY_FOR_PICKUP = "Ready for pickup"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    FAILED = "Failed"
    CANCELED = "Canceled"

    CHOICES = [
        (PENDING, _("Waiting for confirmation")),
        (READY_FOR_PICKUP, _("Ready for pickup")),
        (SHIPPED, _("Shipped to destination")),
        (DELIVERED, _("Delivered")),
        (FAILED, _("Failed")),
        (CANCELED, _("Canceled")),
    ]


def get_shipment_model():
    """
    Return the shipment model that is active in this project
    """
    try:
        app_label, model_name = settings.SHIPMENT_MODEL.split(".")
    except (ValueError, AttributeError):
        raise ImproperlyConfigured(
            "shipment_model must be of the form " '"app_label.model_name"'
        )
    from django.apps import apps
    shipment_model = apps.get_model(app_label, model_name)
    if shipment_model is None:
        msg = (
            'shipment_model refers to model "%s" that has not been installed'
            % settings.shipment_model
        )
        raise ImproperlyConfigured(msg)
    return shipment_model
