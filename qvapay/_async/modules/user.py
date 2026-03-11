from typing import Any, List

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
        response = await self._http.get("user/payment_methods")
        validate_response(response)
        return [PaymentMethod.from_json(m) for m in response.json()]

    async def create(self, **kwargs: Any) -> PaymentMethod:
        """Create a payment method."""
        response = await self._http.post("user/payment_methods", json=kwargs)
        validate_response(response)
        return PaymentMethod.from_json(response.json())


class UserPaymentLinksSubModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def list(self) -> List[PaymentLink]:
        """List saved payment links."""
        response = await self._http.get("user/payment_links")
        validate_response(response)
        return [PaymentLink.from_json(item) for item in response.json()]

    async def delete(self, uuid: str) -> None:
        """Delete a payment link."""
        response = await self._http.delete(f"user/payment_links/{uuid}")
        validate_response(response)

    async def create(self, **kwargs: Any) -> PaymentLink:
        """Create a payment link."""
        response = await self._http.post("user/payment_links", json=kwargs)
        validate_response(response)
        return PaymentLink.from_json(response.json())


class ContactsSubModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def list(self) -> List[Contact]:
        """List saved contacts."""
        response = await self._http.get("user/contacts")
        validate_response(response)
        return [Contact.from_json(c) for c in response.json()]

    async def save(self, **kwargs: Any) -> Contact:
        """Save a contact."""
        response = await self._http.post("user/contacts", json=kwargs)
        validate_response(response)
        return Contact.from_json(response.json())


class DomainsSubModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def check(self, domain: str) -> Domain:
        """Check domain availability."""
        response = await self._http.get("user/domains/check", params={"domain": domain})
        validate_response(response)
        return Domain.from_json(response.json())

    async def get_available(self, **kwargs: Any) -> Domain:
        """Get an available domain."""
        response = await self._http.post("user/domains/available", json=kwargs)
        validate_response(response)
        return Domain.from_json(response.json())


class UserModule:
    def __init__(self, http: AsyncClient):
        self._http = http
        self.payment_methods = PaymentMethodsSubModule(http)
        self.payment_links = UserPaymentLinksSubModule(http)
        self.contacts = ContactsSubModule(http)
        self.domains = DomainsSubModule(http)

    async def me(self) -> User:
        """Get current user profile."""
        response = await self._http.get("user/me")
        validate_response(response)
        return User.from_json(response.json())

    async def me_extended(self) -> User:
        """Get extended user profile."""
        response = await self._http.get("user/me/extended")
        validate_response(response)
        return User.from_json(response.json())

    async def update(self, **kwargs: Any) -> User:
        """Update user profile."""
        response = await self._http.put("user/me", json=kwargs)
        validate_response(response)
        return User.from_json(response.json())

    async def update_email(self, email: str) -> User:
        """Update user email."""
        response = await self._http.put("user/me/email", json={"email": email})
        validate_response(response)
        return User.from_json(response.json())

    async def update_username(self, username: str) -> User:
        """Update username."""
        response = await self._http.put("user/me/username", json={"username": username})
        validate_response(response)
        return User.from_json(response.json())

    async def upload_avatar(self, file: Any) -> User:
        """Upload user avatar."""
        response = await self._http.post("user/me/avatar", files={"avatar": file})
        validate_response(response)
        return User.from_json(response.json())

    async def upload_cover(self, file: Any) -> User:
        """Upload user cover image."""
        response = await self._http.post("user/me/cover", files={"cover": file})
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

    async def topup(self, pay_method: str, amount: float) -> Any:
        """Top up balance."""
        payload = {"pay_method": pay_method, "amount": amount}
        response = await self._http.post("user/topup", json=payload)
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
        """Get user gold status."""
        response = await self._http.get("user/gold")
        validate_response(response)
        return response.json()

    async def gold_purchase(self, **kwargs: Any) -> Any:
        """Purchase gold membership."""
        response = await self._http.post("user/gold", json=kwargs)
        validate_response(response)
        return response.json()

    async def savings_status(self) -> Any:
        """Get savings status."""
        response = await self._http.get("user/savings")
        validate_response(response)
        return response.json()
