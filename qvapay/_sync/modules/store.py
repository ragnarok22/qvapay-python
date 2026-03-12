from typing import Any, List

from httpx import Client

from ...models.product import Product
from ...models.purchased_product import PurchasedProduct
from ...utils import validate_response


class PhonePackageSubModule:
    def __init__(self, http: Client):
        self._http = http

    def list(self) -> List[Any]:
        """List available phone packages."""
        response = self._http.get("store/phone_package")
        validate_response(response)
        payload = response.json()
        if isinstance(payload, dict) and isinstance(
            payload.get("phone_packages"), list
        ):
            return payload["phone_packages"]
        return payload

    def purchase(self, **kwargs: Any) -> Any:
        """Purchase a phone package."""
        response = self._http.post("store/phone_package", json=kwargs)
        validate_response(response)
        return response.json()


class DebitCardSubModule:
    def __init__(self, http: Client):
        self._http = http

    def list(self) -> Any:
        """List available debit card packages."""
        response = self._http.get("store/visa_card")
        validate_response(response)
        payload = response.json()
        if isinstance(payload, dict) and "visaCardService" in payload:
            return payload["visaCardService"]
        return payload

    def purchase(self, **kwargs: Any) -> Any:
        """Purchase a debit card package."""
        response = self._http.post("store/visa_card", json=kwargs)
        validate_response(response)
        return response.json()


class GiftCardSubModule:
    def __init__(self, http: Client):
        self._http = http

    def catalog(self) -> List[Any]:
        """Get gift cards catalog."""
        response = self._http.get("store/gift-card")
        validate_response(response)
        payload = response.json()
        if isinstance(payload, dict) and isinstance(payload.get("data"), list):
            return payload["data"]
        return payload

    def get(self, uuid: str) -> Any:
        """Get gift card item details."""
        response = self._http.get(f"store/gift-card/{uuid}")
        validate_response(response)
        return response.json()

    def purchase(self, uuid: str, **kwargs: Any) -> Any:
        """Purchase a gift card item."""
        response = self._http.post(f"store/gift-card/{uuid}", json=kwargs)
        validate_response(response)
        return response.json()


class StoreModule:
    def __init__(self, http: Client):
        self._http = http
        self.phone_package = PhonePackageSubModule(http)
        self.debit_card = DebitCardSubModule(http)
        self.gift_card = GiftCardSubModule(http)

    @staticmethod
    def _data_items(payload: Any) -> list[Any]:
        if isinstance(payload, dict) and isinstance(payload.get("data"), list):
            return payload["data"]
        return payload

    @staticmethod
    def _detail_payload(payload: Any) -> Any:
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        if isinstance(payload, list) and payload:
            return payload[0]
        return payload

    def products(self) -> List[Product]:
        """Get available store products."""
        response = self._http.get("store")
        validate_response(response)
        return [Product.from_json(p) for p in self._data_items(response.json())]

    def my_purchased(self) -> List[PurchasedProduct]:
        """Get my purchased products."""
        response = self._http.get("store/my")
        validate_response(response)
        return [
            PurchasedProduct.from_json(p)
            for p in self._data_items(response.json())
        ]

    def get_purchased(self, uuid: str) -> PurchasedProduct:
        """Get details of a purchased product."""
        response = self._http.get(f"store/my/{uuid}")
        validate_response(response)
        return PurchasedProduct.from_json(self._detail_payload(response.json()))
