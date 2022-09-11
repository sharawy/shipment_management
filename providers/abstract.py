import abc


class AbstractCourierProvider(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_shipment(
            self,
            shipment: object,

    ) -> dict:
        """
        Place limit order for a token pair.

        :param shipment: shipment model to create waybill for specific provider


        :return: {"tracking_number": "",
                "label_url": ""}
        """

        raise NotImplementedError()

    @abc.abstractmethod
    def print_waybill(
            self,
            **kwargs: dict,

    ) -> str:
        """
        Place limit order for a token pair.

        :param kwargs: key arguments needed to print waybill label for specific provider


        :return: dict
        """

        raise NotImplementedError()

    def cancel_shipment(
            self,
            waybill: str,
    ):
        """
        Place market or limit order for a token pair.

        :param waybill: (str)

        :return: (boolean) Example
        """
        pass
