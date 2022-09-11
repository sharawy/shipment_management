import json
import logging
from datetime import date
from json import JSONDecodeError

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .exceptions import ProviderError, ServerError, ServiceUnavailable

logger = logging.getLogger(__name__)


class BasicClient(object):

    def __init__(self, base_url, **kwargs):
        self.headers = kwargs.get('headers', {})
        self.oauth_needed = kwargs.get('oauth_needed', False)
        if not base_url:
            raise ImproperlyConfigured("Base url is not provided for the client.")
        self.base_url = base_url

    def _dispatch_request(self, http_method: str):
        return {
            "get": requests.get,
            "delete": requests.delete,
            "put": requests.put,
            "post": requests.post,
        }.get(http_method.lower(), "GET")

    def _handle_exception(self, response):
        status_code = response.status_code
        print(response.content, response.status_code)
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)
            except JSONDecodeError as e:
                raise ProviderError(message=e, code=status_code)
            raise ProviderError("Bad Request Error", code=status_code, api_response=err)
        raise ServerError(status_code, response.text)

    def send_request(self, http_method, url_path, payload=None):
        if payload is None:
            payload = {}
        url = self.base_url + url_path
        logger.debug("url: " + url)
        params = {
            "url": url,
            "data": payload,
        }
        self.handle_authentication()
        print(self.headers)
        response = self._dispatch_request(http_method)(**params, headers=self.headers)
        logger.debug("raw response from server:" + response.text)
        self._handle_exception(response)

        try:
            data = response.json()
        except ValueError:
            data = response.text
        return data

    def handle_authentication(self):
        # TODO: need enhancement
        if self.oauth_needed:
            self.headers["Authorization"] = "Bearer " + self.get_token()
        else:
            self.headers["Authorization"] = "Basic " + self.get_token()

    def get_token(self):
        raise NotImplementedError()


class FEDEXClient(BasicClient):
    """ This is not fully implemented client it just to test the framework"""

    def __init__(self):
        headers = {"Content-Type": "application/json"}
        if not hasattr(settings, "FEDEX_ACCOUNT_NUMBER"):
            raise ImproperlyConfigured("FEDEX_ACCOUNT_NUMBER should be provided in settings")
        self.fedex_account_number = settings.FEDEX_ACCOUNT_NUMBER
        super().__init__(base_url=settings.FEDEX_API, headers=headers, oauth_needed=True)

    def get_token(self):

        try:
            response = self._dispatch_request("post")(url=self.base_url + "oauth/token",
                                                      data={"grant_type": "client_credentials",
                                                            "client_id": settings.FEDEX_API_KEY,
                                                            "client_secret": settings.FEDEX_API_SECRET},
                                                      headers={"Content-Type": "application/x-www-form-urlencoded"})
        except Exception as e:
            logger.error(e)
            raise ServiceUnavailable("Failed to obtain token, service is not available")
        if response.ok:
            print(response.json()['access_token'])
            return response.json()['access_token']
        else:
            logger.error(response.text)
            raise ProviderError(message="Failed to obtain token", code=response.status_code, api_response=response.text)

    def create_shipment(self, shipment_info: dict, shipment_date: date, items: list = [{}]):
        """
            this an example request to test the integration
        """
        payload = {
            "labelResponseOptions": "URL_ONLY",
            "requestedShipment": {
                "shipper": shipment_info['shipper'],
                "recipients": shipment_info['recipients'],
                "shipDatestamp": shipment_date,
                "serviceType": "STANDARD_OVERNIGHT",
                "packagingType": "FEDEX_SMALL_BOX",
                "pickupType": "USE_SCHEDULED_PICKUP",
                "blockInsightVisibility": False,
                "shippingChargesPayment": {
                    "paymentType": "SENDER"
                },
                "shipmentSpecialServices": {
                    "specialServiceTypes": [
                        "FEDEX_ONE_RATE"
                    ]
                },
                "labelSpecification": {
                    "imageType": "PDF",
                    "labelStockType": "PAPER_85X11_TOP_HALF_LABEL"
                },
                "requestedPackageLineItems": items
            },
            "accountNumber": {
                "value": self.fedex_account_number
            }
        }
        self.send_request('post', url_path='ship/v1/shipments', payload=payload)
