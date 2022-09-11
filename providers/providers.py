from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from django.utils.module_loading import import_string

from providers import ShipmentStatuses, get_shipment_model
from providers.clients import FEDEXClient
from providers.exceptions import ProviderError
from .abstract import AbstractCourierProvider


class CourierProviderFacade:

    def __init__(self, courier_provider: str):
        if not hasattr(settings, "COURIER_PROVIDERS"):
            raise ImproperlyConfigured("COURIER_PROVIDERS are not provided in settings")
        self.courier_provider = import_string(settings.COURIER_PROVIDERS[courier_provider]['class'])()

    def _get_shipment(self, shipment_uuid: str):
        ShipmentModel = get_shipment_model()
        shipment = get_object_or_404(ShipmentModel, uuid=shipment_uuid)
        return shipment

    def create_tracking_number(self, shipment):
        """
        :param: shipment model.
        """
        result = {}
        try:
            result = self.courier_provider.create_shipment(shipment)
        except ProviderError as e:
            shipment.change_status(ShipmentStatuses.FAILED, e.message, e.api_response)
        if result.get('tracking_number'):

            shipment.add_tracking_number(tracking_number=result.get('tracking_number'),
                                         provider=self.courier_provider.name, label_url=result.get('label_url', None))
            shipment.change_status(ShipmentStatuses.PENDING, message="Waybill label created")

    def cancel_shipment(self, shipment):
        self.courier_provider.cancel_shipment(shipment.waybill_number)
        shipment.change_status(ShipmentStatuses.CANCELED, "Shipment canceled")

        return shipment

    def print_waybill(self, shipment):
        return self.courier_provider.print_waybill(shipment.tracking_number)


class DummyProvider(AbstractCourierProvider):

    @property
    def name(self) -> str:
        return "Dummy"

    def create_shipment(self, shipment: object) -> str:
        print("test")
        return {"tracking_number": "123445566",
                "label_url": "https://example.com"}

    def print_waybill(self, **kwargs: dict) -> str:
        return "https://example.com"


class FEDEXProvider(AbstractCourierProvider):
    """This is  a test provider """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = FEDEXClient()

    @property
    def name(self) -> str:
        return "FEDEX"

    def _generate_payload(self, shipment):
        """This is simple example of mapping shipment to provider client api request"""
        # TODO: replace by dataclasses for the whole payload

        return {"shipper": {
            "contact": {
                "personName": "SHIPPER NAME",
                "phoneNumber": 1234567890,
                "companyName": "Shipper Company Name"
            },
            "address": {
                "streetLines": [
                    shipment.from_address.street
                ],
                "city": shipment.from_address.city,
                "stateOrProvinceCode": shipment.from_address.state,
                "postalCode": int(shipment.from_address.postal_code),
                "countryCode": shipment.from_address.country
            }
        },
            "recipients": [
                {
                    "contact": {
                        "personName": "RECIPIENT NAME",
                        "phoneNumber": 1234567890,
                        "companyName": "Recipient Company Name"
                    },
                    "address": {
                        "streetLines": [
                            shipment.to_address.street
                        ],
                        "city": shipment.to_address.city,
                        "stateOrProvinceCode": shipment.to_address.state,
                        "postalCode": int(shipment.to_address.postal_code),
                        "countryCode": shipment.to_address.country
                    }
                }
            ]
        }

    def create_shipment(self, shipment: object) -> dict:
        """
        :param shipment: shipment model
        :return: waybill or tracking number and document url
        """
        result = self.client.create_shipment(self._generate_payload(shipment), shipment_date="2022-09-12")
        return {"tracking_number": result['output']['transactionShipments'][0]['masterTrackingNumber'],
                "label_url": result['output']['transactionShipments'][0]['pieceResponses']['packageDocuments'][
                    'url']}

    def print_waybill(self, **kwargs: dict) -> str:
        pass
