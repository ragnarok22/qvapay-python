from typing import Any, List, Optional

from httpx import AsyncClient

from ...models.contact import Contact
from ...models.domain import Domain
from ...models.payment_link import PaymentLink
from ...models.payment_method import PaymentMethod
from ...models.user import User
from ...utils import validate_response


class PaymentMethodsSubModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def list(self) -> List[PaymentMethod]:
        """List saved payment methods."""
        response = await self._http.get("user/payment-methods")
        validate_response(response)
        return [PaymentMethod.from_json(m) for m in response.json()]

    async def create(self, **kwargs: Any) -> PaymentMethod:
        """Create a payment method."""
        response = await self._http.post("user/payment-methods", json=kwargs)
        validate_response(response)
        return PaymentMethod.from_json(response.json())


class UserPaymentLinksSubModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def list(self) -> List[PaymentLink]:
        """List saved payment links."""
        response = await self._http.get("user/payment-links")
        validate_response(response)
        return [PaymentLink.from_json(item) for item in response.json()]

    async def delete(self, link_id: Any) -> None:
        """Delete a payment link by ID."""
        response = await self._http.delete(
            "user/payment-links",
            json={"id": link_id},
        )
        validate_response(response)

    async def create(self, **kwargs: Any) -> PaymentLink:
        """Create a payment link."""
        response = await self._http.post("user/payment-links", json=kwargs)
        validate_response(response)
        return PaymentLink.from_json(response.json())


class ContactsSubModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def list(self) -> List[Contact]:
        """List saved contacts."""
        response = await self._http.get("user/contact")
        validate_response(response)
        return [Contact.from_json(c) for c in response.json()]

    async def save(self, **kwargs: Any) -> Contact:
        """Save a contact."""
        response = await self._http.post("user/contact", json=kwargs)
        validate_response(response)
        return Contact.from_json(response.json())


class DomainsSubModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def check(self, domain: str) -> Domain:
        """Check domain availability."""
        response = await self._http.get("domain", params={"name": domain})
        validate_response(response)
        return Domain.from_json(response.json())

    async def get_available(self, **kwargs: Any) -> Domain:
        """Get an available domain."""
        response = await self._http.post("domain", json=kwargs)
        validate_response(response)
        return Domain.from_json(response.json())


class SavingsSubModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def status(self) -> Any:
        """Get savings status."""
        response = await self._http.get("saving")
        validate_response(response)
        return response.json()


class UserModule:
    def __init__(self, http: AsyncClient):
        self._http = http
        self.payment_methods = PaymentMethodsSubModule(http)
        self.payment_links = UserPaymentLinksSubModule(http)
        self.contacts = ContactsSubModule(http)
        self.domains = DomainsSubModule(http)
        self.savings = SavingsSubModule(http)

    async def me(self) -> User:
        """Get current user profile."""
        response = await self._http.get("user")
        validate_response(response)
        return User.from_json(response.json())

    async def me_extended(self) -> User:
        """Get extended user profile."""
        response = await self._http.get("user/extended")
        validate_response(response)
        return User.from_json(response.json())

    async def update(self, **kwargs: Any) -> User:
        """Update user profile."""
        response = await self._http.put("user/update", json=kwargs)
        validate_response(response)
        return User.from_json(response.json())

    async def update_email(self, email: str, pin: Optional[str] = None) -> User:
        """Update user email.

        On first call, sends a verification PIN to the new address.
        On second call, pass the PIN to confirm the change.
        """
        payload: dict = {"email": email}
        if pin is not None:
            payload["pin"] = pin
        response = await self._http.put("user/update/email", json=payload)
        validate_response(response)
        return User.from_json(response.json())

    async def update_username(self, username: str) -> User:
        """Update username."""
        response = await self._http.put(
            "user/update/username", json={"username": username}
        )
        validate_response(response)
        return User.from_json(response.json())

    async def upload_avatar(self, file: Any) -> User:
        """Upload user avatar (128×128 px, JPG/JPEG/PNG, max 5 MB)."""
        response = await self._http.post(
            "user/avatar",
            data={"type": "avatar"},
            files={"avatar": file},
        )
        validate_response(response)
        return User.from_json(response.json())

    async def upload_cover(self, file: Any) -> User:
        """Upload user cover photo (1088×256 px, JPG/JPEG/PNG, max 10 MB)."""
        response = await self._http.post(
            "user/avatar",
            data={"type": "cover"},
            files={"cover": file},
        )
        validate_response(response)
        return User.from_json(response.json())

    async def kyc_status(self) -> Any:
        """Get KYC verification status."""
        response = await self._http.get("user/kyc")
        validate_response(response)
        return response.json()

    async def kyc_apply(self, **kwargs: Any) -> Any:
        """Apply for KYC verification."""
        response = await self._http.post("user/kyc", json=kwargs)
        validate_response(response)
        return response.json()

    async def topup(
        self,
        pay_method: str,
        amount: float,
        webhook_url: Optional[str] = None,
    ) -> Any:
        """Top up balance.

        Args:
            pay_method: Payment method e.g. ``"BTCLN"``, ``"USDT"``.
            amount: Amount to top up.
            webhook_url: Optional URL to receive a webhook notification.
        """
        payload: dict = {"pay_method": pay_method, "amount": amount}
        if webhook_url is not None:
            payload["webhook_url"] = webhook_url
        response = await self._http.post("topup", json=payload)
        validate_response(response)
        return response.json()

    async def search(self, query: str) -> List[User]:
        """Search for users."""
        response = await self._http.post("user/search", json={"query": query})
        validate_response(response)
        return [User.from_json(u) for u in response.json()]

    async def referrals(self) -> Any:
        """Get user referrals."""
        response = await self._http.get("user/referrals")
        validate_response(response)
        return response.json()

    async def gold_status(self) -> Any:
        """Get user gold membership status."""
        response = await self._http.get("user/gold")
        validate_response(response)
        return response.json()

    async def gold_purchase(self, **kwargs: Any) -> Any:
        """Purchase gold membership."""
        response = await self._http.post("user/gold", json=kwargs)
        validate_response(response)
        return response.json()

    # Keep backwards-compatible savings_status() alias
    async def savings_status(self) -> Any:
        """Get savings status. Alias for user.savings.status()."""
        return await self.savings.status()
