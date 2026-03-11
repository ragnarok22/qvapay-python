from typing import Any, List, Optional

from httpx import Client

from ...models.contact import Contact
from ...models.domain import Domain
from ...models.payment_link import PaymentLink
from ...models.payment_method import PaymentMethod
from ...models.user import User
from ...utils import validate_response


class PaymentMethodsSubModule:
    def __init__(self, http: Client):
        self._http = http

    def list(self) -> List[PaymentMethod]:
        """List saved payment methods."""
        response = self._http.get("user/payment_methods")
        validate_response(response)
        return [PaymentMethod.from_json(m) for m in response.json()]

    def create(self, **kwargs: Any) -> PaymentMethod:
        """Create a payment method."""
        response = self._http.post(
            "user/payment_methods", json=kwargs
        )
        validate_response(response)
        return PaymentMethod.from_json(response.json())


class UserPaymentLinksSubModule:
    def __init__(self, http: Client):
        self._http = http

    def list(self) -> List[PaymentLink]:
        """List saved payment links."""
        response = self._http.get("user/payment_links")
        validate_response(response)
        return [PaymentLink.from_json(l) for l in response.json()]

    def delete(self, uuid: str) -> None:
        """Delete a payment link."""
        response = self._http.delete(
            f"user/payment_links/{uuid}"
        )
        validate_response(response)

    def create(self, **kwargs: Any) -> PaymentLink:
        """Create a payment link."""
        response = self._http.post(
            "user/payment_links", json=kwargs
        )
        validate_response(response)
        return PaymentLink.from_json(response.json())


class ContactsSubModule:
    def __init__(self, http: Client):
        self._http = http

    def list(self) -> List[Contact]:
        """List saved contacts."""
        response = self._http.get("user/contacts")
        validate_response(response)
        return [Contact.from_json(c) for c in response.json()]

    def save(self, **kwargs: Any) -> Contact:
        """Save a contact."""
        response = self._http.post(
            "user/contacts", json=kwargs
        )
        validate_response(response)
        return Contact.from_json(response.json())


class DomainsSubModule:
    def __init__(self, http: Client):
        self._http = http

    def check(self, domain: str) -> Domain:
        """Check domain availability."""
        response = self._http.get(
            "user/domains/check", params={"domain": domain}
        )
        validate_response(response)
        return Domain.from_json(response.json())

    def get_available(self, **kwargs: Any) -> Domain:
        """Get an available domain."""
        response = self._http.post(
            "user/domains/available", json=kwargs
        )
        validate_response(response)
        return Domain.from_json(response.json())


class UserModule:
    def __init__(self, http: Client):
        self._http = http
        self.payment_methods = PaymentMethodsSubModule(http)
        self.payment_links = UserPaymentLinksSubModule(http)
        self.contacts = ContactsSubModule(http)
        self.domains = DomainsSubModule(http)

    def me(self) -> User:
        """Get current user profile."""
        response = self._http.get("user/me")
        validate_response(response)
        return User.from_json(response.json())

    def me_extended(self) -> User:
        """Get extended user profile."""
        response = self._http.get("user/me/extended")
        validate_response(response)
        return User.from_json(response.json())

    def update(self, **kwargs: Any) -> User:
        """Update user profile."""
        response = self._http.put("user/me", json=kwargs)
        validate_response(response)
        return User.from_json(response.json())

    def update_email(self, email: str) -> User:
        """Update user email."""
        response = self._http.put(
            "user/me/email", json={"email": email}
        )
        validate_response(response)
        return User.from_json(response.json())

    def update_username(self, username: str) -> User:
        """Update username."""
        response = self._http.put(
            "user/me/username", json={"username": username}
        )
        validate_response(response)
        return User.from_json(response.json())

    def upload_avatar(self, file: Any) -> User:
        """Upload user avatar."""
        response = self._http.post(
            "user/me/avatar", files={"avatar": file}
        )
        validate_response(response)
        return User.from_json(response.json())

    def upload_cover(self, file: Any) -> User:
        """Upload user cover image."""
        response = self._http.post(
            "user/me/cover", files={"cover": file}
        )
        validate_response(response)
        return User.from_json(response.json())

    def kyc_status(self) -> Any:
        """Get KYC verification status."""
        response = self._http.get("user/kyc")
        validate_response(response)
        return response.json()

    def kyc_apply(self, **kwargs: Any) -> Any:
        """Apply for KYC verification."""
        response = self._http.post("user/kyc", json=kwargs)
        validate_response(response)
        return response.json()

    def topup(self, pay_method: str, amount: float) -> Any:
        """Top up balance."""
        payload = {"pay_method": pay_method, "amount": amount}
        response = self._http.post("user/topup", json=payload)
        validate_response(response)
        return response.json()

    def search(self, query: str) -> List[User]:
        """Search for users."""
        response = self._http.post(
            "user/search", json={"query": query}
        )
        validate_response(response)
        return [User.from_json(u) for u in response.json()]

    def referrals(self) -> Any:
        """Get user referrals."""
        response = self._http.get("user/referrals")
        validate_response(response)
        return response.json()

    def gold_status(self) -> Any:
        """Get user gold status."""
        response = self._http.get("user/gold")
        validate_response(response)
        return response.json()

    def gold_purchase(self, **kwargs: Any) -> Any:
        """Purchase gold membership."""
        response = self._http.post("user/gold", json=kwargs)
        validate_response(response)
        return response.json()

    def savings_status(self) -> Any:
        """Get savings status."""
        response = self._http.get("user/savings")
        validate_response(response)
        return response.json()
