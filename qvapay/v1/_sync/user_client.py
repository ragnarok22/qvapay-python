from dataclasses import dataclass, field
from typing import List, Optional, Union
from uuid import UUID

from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import TimeoutTypes

from ..auth import QvaPayUserAuth
from ..http_clients import SyncClient
from ..models.p2p_offer import P2POffer
from ..models.paginated_transactions import PaginatedTransactions
from ..models.payment_link import PaymentLink
from ..models.service import Service
from ..models.transaction_detail import TransactionDetail
from ..models.transfer import Transfer
from ..models.user import User
from ..models.withdrawal import Withdrawal
from ..utils import validate_response


@dataclass
class SyncQvaPayUserClient:
    """
    Creates a QvaPay user client authenticated with a Bearer token.
    * access_token: Bearer token obtained from login.
    """

    access_token: str
    timeout: TimeoutTypes = field(default_factory=lambda: DEFAULT_TIMEOUT_CONFIG)

    def __post_init__(self):
        self.base_url = "https://qvapay.com/api"
        self.http_client = SyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=self.timeout,
            follow_redirects=True,
        )

    def __enter__(self) -> "SyncQvaPayUserClient":
        return self

    def __exit__(self, exc_t, exc_v, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self.http_client.aclose()

    @staticmethod
    def from_auth(
        auth: QvaPayUserAuth,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    ) -> "SyncQvaPayUserClient":
        return SyncQvaPayUserClient(auth.access_token, timeout)

    # User profile

    def get_user(self) -> User:
        """Get the authenticated user's profile."""
        response = self.http_client.get("user")
        validate_response(response)
        return User.from_json(response.json())

    def update_user(
        self,
        name: Optional[str] = None,
        lastname: Optional[str] = None,
        bio: Optional[str] = None,
        logo: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> User:
        """Update the authenticated user's profile."""
        payload = {}
        if name is not None:
            payload["name"] = name
        if lastname is not None:
            payload["lastname"] = lastname
        if bio is not None:
            payload["bio"] = bio
        if logo is not None:
            payload["logo"] = logo
        if username is not None:
            payload["username"] = username
        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password
        response = self.http_client.put("user", json=payload)
        validate_response(response)
        return User.from_json(response.json())

    # Financial operations

    def topup(self, pay_method: str, amount: float) -> dict:
        """Request a deposit/top-up."""
        payload = {"pay_method": pay_method, "amount": amount}
        response = self.http_client.post("topup", json=payload)
        validate_response(response)
        return response.json()

    def withdraw(self, pay_method: str, amount: float, details: str) -> Withdrawal:
        """Request a withdrawal."""
        payload = {
            "pay_method": pay_method,
            "amount": amount,
            "details": details,
        }
        response = self.http_client.post("withdraw", json=payload)
        validate_response(response)
        return Withdrawal.from_json(response.json())

    # Transactions

    def get_transactions(
        self,
        start: Optional[str] = None,
        end: Optional[str] = None,
        status: Optional[str] = None,
        remote_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> PaginatedTransactions:
        """Get the authenticated user's transactions with optional filters."""
        params = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if status is not None:
            params["status"] = status
        if remote_id is not None:
            params["remote_id"] = remote_id
        if description is not None:
            params["description"] = description
        response = self.http_client.get("transactions", params=params)
        validate_response(response)
        return PaginatedTransactions.from_json(response.json())

    def get_transaction(self, id: Union[str, UUID]) -> TransactionDetail:
        """Get a specific transaction by id."""
        response = self.http_client.get(f"transactions/{id}")
        validate_response(response)
        return TransactionDetail.from_json(response.json())

    def transfer(
        self, to: Union[str, UUID], amount: float, description: str
    ) -> Transfer:
        """Transfer funds to another user."""
        payload = {
            "to": str(to),
            "amount": amount,
            "description": description,
        }
        response = self.http_client.post("transactions/transfer", json=payload)
        validate_response(response)
        return Transfer.from_json(response.json())

    def pay(self, uuid: Union[str, UUID], pin: str) -> dict:
        """Pay a pending transaction."""
        payload = {"uuid": str(uuid), "pin": pin}
        response = self.http_client.post("transactions/pay", json=payload)
        validate_response(response)
        return response.json()

    # Withdrawals

    def get_withdrawals(self) -> List[Withdrawal]:
        """Get the authenticated user's withdrawals."""
        response = self.http_client.get("withdraws")
        validate_response(response)
        return [Withdrawal.from_json(item) for item in response.json()]

    def get_withdrawal(self, id: Union[str, UUID]) -> Withdrawal:
        """Get a specific withdrawal by id."""
        response = self.http_client.get(f"withdraws/{id}")
        validate_response(response)
        return Withdrawal.from_json(response.json())

    # P2P

    def get_p2p_offers(self) -> List[P2POffer]:
        """Get P2P offers."""
        response = self.http_client.get("p2p/index")
        validate_response(response)
        return [P2POffer.from_json(item) for item in response.json()]

    def get_p2p_offer(self, id: Union[str, UUID]) -> P2POffer:
        """Get a specific P2P offer by id."""
        response = self.http_client.get(f"p2p/{id}")
        validate_response(response)
        return P2POffer.from_json(response.json())

    # Services

    def get_services(self) -> List[Service]:
        """Get available services."""
        response = self.http_client.get("services")
        validate_response(response)
        return [Service.from_json(item) for item in response.json()]

    def get_service(self, id: Union[str, UUID]) -> Service:
        """Get a specific service by id."""
        response = self.http_client.get(f"services/{id}")
        validate_response(response)
        return Service.from_json(response.json())

    # Payment Links

    def get_payment_links(self) -> List[PaymentLink]:
        """Get the authenticated user's payment links."""
        response = self.http_client.get("payment_links")
        validate_response(response)
        return [PaymentLink.from_json(item) for item in response.json()]

    def create_payment_link(
        self,
        amount: float,
        description: str,
    ) -> PaymentLink:
        """Create a new payment link."""
        payload = {"amount": amount, "description": description}
        response = self.http_client.post("payment_links/create", json=payload)
        validate_response(response)
        return PaymentLink.from_json(response.json())

    # Auth convenience

    def logout(self) -> None:
        """Logout and invalidate the current token."""
        response = self.http_client.get("auth/logout")
        validate_response(response)
