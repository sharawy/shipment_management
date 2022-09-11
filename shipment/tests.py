from unittest import mock

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class ShipmentTestCase(APITestCase):
    """ Basic test case """

    @mock.patch("shipment.serializers.create_shipment_task.delay")
    def test_create_shipment(self, mock_task_call):
        url = reverse('shipment_api')
        data = {

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(mock_task_call.call_count, 0)
        data = {
            "to_address": {
                "id": 16,
                "street": "RECIPIENT STREET LINE 1",
                "city": "Collierville",
                "country": "US",
                "state": "TN",
                "postal_code": "38017"
            },
            "from_address": {
                "id": 15,
                "street": "SHIPPER STREET LINE 1",
                "city": "HARRISON",
                "country": "US",
                "state": "AR",
                "postal_code": "72601"
            },
            "weight": "4.00",
            "no_of_items": 3,
            "description": "dsfdsf",
            "provider": "DUMMY",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(mock_task_call.call_count, 1)
