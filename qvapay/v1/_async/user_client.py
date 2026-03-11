from dataclasses import dataclass, field
from typing import Any, List, Optional, Union
from uuid import UUID

from ..auth import QvaPayUserAuth
from ..http_clients import DEFAULT_TIMEOUT, AsyncClient, TimeoutTypes
from ..models.coin import Coin
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
class AsyncQvaPayUserClient:
    """
    Creates a QvaPay user client authenticated with a Bearer token.
    * access_token: Bearer token obtained from login.
    """

    access_token: str
    timeout: TimeoutTypes = field(default_factory=lambda: DEFAULT_TIMEOUT)

    def __post_init__(self):
        self.base_url = "https://api.qvapay.com"
        self.http_client = AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=self.timeout,
            follow_redirects=True,
        )

    async def __aenter__(self) -> "AsyncQvaPayUserClient":
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self.http_client.aclose()

    @staticmethod
    def from_auth(
        auth: QvaPayUserAuth,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT,
    ) -> "AsyncQvaPayUserClient":
        return AsyncQvaPayUserClient(auth.access_token, timeout)

    # User profile

    async def get_user(self) -> User:
        """Get the authenticated user's profile."""
        response = await self.http_client.get("user")
        validate_response(response)
        return User.from_json(response.json())

    async def update_user(
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
        payload = {
            k: v
            for k, v in {
                "name": name,
                "lastname": lastname,
                "bio": bio,
                "logo": logo,
                "username": username,
                "email": email,
                "password": password,
            }.items()
            if v is not None
        }
        response = await self.http_client.put("user", json=payload)
        validate_response(response)
        return User.from_json(response.json())

    # Financial operations

    async def topup(self, pay_method: str, amount: float) -> dict[str, Any]:
        """Request a deposit/top-up."""
        payload = {"pay_method": pay_method, "amount": amount}
        response = await self.http_client.post("topup", json=payload)
        validate_response(response)
        return response.json()

    async def withdraw(
        self, pay_method: str, amount: float, details: str
    ) -> Withdrawal:
        """Request a withdrawal."""
        payload = {
            "pay_method": pay_method,
            "amount": amount,
            "details": details,
        }
        response = await self.http_client.post("withdraw", json=payload)
        validate_response(response)
        return Withdrawal.from_json(response.json())

    # Transactions

    async def get_transactions(
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
        response = await self.http_client.get("transactions", params=params)
        validate_response(response)
        return PaginatedTransactions.from_json(response.json())

    async def get_transaction(self, id: Union[str, UUID]) -> TransactionDetail:
        """Get a specific transaction by id."""
        response = await self.http_client.get(f"transactions/{id}")
        validate_response(response)
        return TransactionDetail.from_json(response.json())

    async def transfer(
        self, to: Union[str, UUID], amount: float, description: str
    ) -> Transfer:
        """Transfer funds to another user."""
        payload = {
            "to": str(to),
            "amount": amount,
            "description": description,
        }
        response = await self.http_client.post("transactions/transfer", json=payload)
        validate_response(response)
        return Transfer.from_json(response.json())

    async def pay(self, uuid: Union[str, UUID], pin: str) -> dict[str, Any]:
        """Pay a pending transaction."""
        payload = {"uuid": str(uuid), "pin": pin}
        response = await self.http_client.post("transactions/pay", json=payload)
        validate_response(response)
        return response.json()

    # Withdrawals

    async def get_withdrawals(self) -> List[Withdrawal]:
        """Get the authenticated user's withdrawals."""
        response = await self.http_client.get("withdraws")
        validate_response(response)
        return [Withdrawal.from_json(item) for item in response.json()]

    async def get_withdrawal(self, id: Union[str, UUID]) -> Withdrawal:
        """Get a specific withdrawal by id."""
        response = await self.http_client.get(f"withdraws/{id}")
        validate_response(response)
        return Withdrawal.from_json(response.json())

    # P2P

    async def get_p2p_coins_list(self) -> List[Coin]:
        """Get P2P enabled currencies."""
        response = await self.http_client.get("p2p/get_coins_list")
        validate_response(response)
        return [Coin.from_json(item) for item in response.json()]

    async def get_p2p_offers(self) -> List[P2POffer]:
        """Get P2P offers."""
        response = await self.http_client.get("p2p/index")
        validate_response(response)
        return [P2POffer.from_json(item) for item in response.json()]

    async def get_p2p_offer(self, id: Union[str, UUID]) -> P2POffer:
        """Get a specific P2P offer by id."""
        response = await self.http_client.get(f"p2p/{id}")
        validate_response(response)
        return P2POffer.from_json(response.json())

    # Services

    async def get_services(self) -> List[Service]:
        """Get available services."""
        response = await self.http_client.get("services")
        validate_response(response)
        return [Service.from_json(item) for item in response.json()]

    async def get_service(self, id: Union[str, UUID]) -> Service:
        """Get a specific service by id."""
        response = await self.http_client.get(f"services/{id}")
        validate_response(response)
        return Service.from_json(response.json())

    # Payment Links

    async def get_payment_links(self) -> List[PaymentLink]:
        """Get the authenticated user's payment links."""
        response = await self.http_client.get("payment_links")
        validate_response(response)
        return [PaymentLink.from_json(item) for item in response.json()]

    async def create_payment_link(
        self,
        amount: float,
        description: str,
    ) -> PaymentLink:
        """Create a new payment link."""
        payload = {"amount": amount, "description": description}
        response = await self.http_client.post("payment_links/create", json=payload)
        validate_response(response)
        return PaymentLink.from_json(response.json())

    # Auth convenience

    async def logout(self) -> None:
        """Logout and invalidate the current token."""
        response = await self.http_client.get("auth/logout")
        validate_response(response)
