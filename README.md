# Python SDK for the QvaPay API

![Banner](https://raw.githubusercontent.com/ragnarok22/qvapay-python/main/banner.jpg)

Non official, but friendly QvaPay library for the Python language.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Test](https://github.com/ragnarok22/qvapay-python/workflows/CI/badge.svg)](https://github.com/ragnarok22/qvapay-python/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/ragnarok22/qvapay-python/branch/main/graph/badge.svg)](https://codecov.io/gh/ragnarok22/qvapay-python)
[![Version](https://img.shields.io/pypi/v/qvapay?color=%2334D058&label=Version)](https://pypi.org/project/qvapay)
[![Last commit](https://img.shields.io/github/last-commit/ragnarok22/qvapay-python.svg?style=flat)](https://github.com/ragnarok22/qvapay-python/commits)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/ragnarok22/qvapay-python)](https://github.com/ragnarok22/qvapay-python/commits)
[![Github Stars](https://img.shields.io/github/stars/ragnarok22/qvapay-python?style=flat&logo=github)](https://github.com/ragnarok22/qvapay-python/stargazers)
[![Github Forks](https://img.shields.io/github/forks/ragnarok22/qvapay-python?style=flat&logo=github)](https://github.com/ragnarok22/qvapay-python/network/members)
[![Github Watchers](https://img.shields.io/github/watchers/ragnarok22/qvapay-python?style=flat&logo=github)](https://github.com/ragnarok22/qvapay-python)
[![GitHub contributors](https://img.shields.io/github/contributors/ragnarok22/qvapay-python?label=code%20contributors)](https://github.com/ragnarok22/qvapay-python/graphs/contributors)<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Installation

```bash
pip install qvapay
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add qvapay
```

## Sign up on QvaPay

Create your account to process payments through **QvaPay** at [qvapay.com/register](https://qvapay.com/register).

## Quick start

The SDK provides two types of clients:

- **User clients** (`AsyncQvaPayClient` / `SyncQvaPayClient`) — Bearer-token authenticated, for user-level operations.
- **Merchant clients** (`AsyncQvaPayMerchant` / `SyncQvaPayMerchant`) — UUID + secret key authenticated, for app-level operations like invoicing.

### Authentication

Use the standalone `auth` module to obtain an access token:

```python
from qvapay import auth

# Async
token = await auth.login("email@example.com", "password")
print(token.access_token)
```

For the sync equivalent:

```python
from qvapay._sync import auth

token = auth.login("email@example.com", "password")
```

The `auth` module also provides `register`, `request_pin`, `check`, and `logout` functions.

### User client

Create a client with the access token obtained from login:

```python
from qvapay import AsyncQvaPayClient

async with AsyncQvaPayClient(access_token="your-token") as client:
    profile = await client.user.me()
    print(profile.username)
```

Or synchronously:

```python
from qvapay import SyncQvaPayClient

with SyncQvaPayClient(access_token="your-token") as client:
    profile = client.user.me()
    print(profile.username)
```

### Merchant client

For app-level operations, use the merchant client with your app UUID and secret key (get these at [qvapay.com/apps/create](https://qvapay.com/apps/create)):

```python
from qvapay import AsyncQvaPayMerchant

async with AsyncQvaPayMerchant(uuid="app-uuid", secret_key="app-secret") as merchant:
    invoice = await merchant.create_invoice(
        amount=10.00,
        description="Ebook",
        remote_id="EE-BOOK-123",
    )
    print(invoice.url)
```

## User client modules

The user client organizes functionality into modules accessed as attributes:

### Transactions (`client.transactions`)

```python
# List recent transactions (with optional filters)
transactions = await client.transactions.list(
    start="2024-01-01",
    end="2024-12-31",
    status="completed",
)

# Get a specific transaction
detail = await client.transactions.get("transaction-uuid")

# Transfer balance to another user (by UUID, email, or phone)
tx = await client.transactions.transfer(
    to="user@email.com",
    amount=5.00,
    description="Payment for services",
)

# Pay a pending transaction
tx = await client.transactions.pay("transaction-uuid", pin="1234")

# Download transaction PDF
pdf_bytes = await client.transactions.get_pdf("transaction-uuid")
```

### User profile (`client.user`)

```python
profile = await client.user.me()
extended = await client.user.me_extended()

# Update profile
await client.user.update(bio="Hello world")
await client.user.update_username("new_username")

# Search users
users = await client.user.search("john")

# KYC verification
status = await client.user.kyc_status()

# Sub-modules
contacts = await client.user.contacts.list()
methods = await client.user.payment_methods.list()
domains = await client.user.domains.check("example.com")
```

### Apps (`client.app`)

```python
apps = await client.app.list()
app = await client.app.get("app-uuid")
new_app = await client.app.create(
    name="My App",
    url="https://example.com",
    desc="My QvaPay app",
    callback="https://example.com/callback",
)
```

### P2P trading (`client.p2p`)

```python
offers = await client.p2p.get_offers(coin="USDT", type="buy")
offer = await client.p2p.create_offer(coin="USDT", amount=100, price=1.05, type="sell")

# Chat
messages = await client.p2p.chat.get("offer-uuid")
await client.p2p.chat.send("offer-uuid", "Hello!")

# Trade flow
await client.p2p.apply("offer-uuid")
await client.p2p.mark_paid("offer-uuid")
await client.p2p.confirm_received("offer-uuid")
```

### Withdrawals (`client.withdraw`)

```python
withdrawal = await client.withdraw.create(
    pay_method="USDT",
    amount=50.00,
    details={"address": "0x..."},
)
withdrawals = await client.withdraw.list()
```

### Payment links (`client.payment_links`)

```python
links = await client.payment_links.list()
link = await client.payment_links.create(
    name="Donation",
    product_id="product-uuid",
    amount=5.00,
)
```

### Store (`client.store`)

```python
products = await client.store.products()
purchased = await client.store.my_purchased()

# Sub-modules
packages = await client.store.phone_package.list()
cards = await client.store.gift_card.catalog()
```

### Top-up (`client.topup`)

```python
packages = await client.topup.list_products()
```

## Merchant client methods

```python
async with AsyncQvaPayMerchant(uuid="app-uuid", secret_key="secret") as merchant:
    # App info and balance
    info = await merchant.info()
    balance = await merchant.balance()

    # Invoicing
    invoice = await merchant.create_invoice(
        amount=25.00,
        description="Premium Plan",
        remote_id="INV-001",
        signed=True,
    )
    await merchant.modify_invoice("invoice-uuid", amount=30.00)

    # Transactions
    txs = await merchant.get_transactions()
    status = await merchant.get_transaction_status("tx-uuid")

    # Payment authorization
    auth_url = await merchant.get_payments_authorization(redirect_url="https://...")
    await merchant.charge_user(token="auth-token", amount=10.00)
```

## Standalone modules

### Coins

```python
from qvapay import coins

categories = await coins.list()
operational = await coins.list_v2(enabled_in=True)
coin = await coins.get(coin_id=1)
history = await coins.price_history("BTC", timeframe="7D")
```

### Stocks

```python
from qvapay import stocks

data = await stocks.list()
```

## Error handling

All API errors raise `QvaPayError`:

```python
from qvapay import QvaPayError

try:
    await client.transactions.transfer(to="user@email.com", amount=1000)
except QvaPayError as e:
    print(e.status_code, e.status_message)
```

## For developers

### Setup

```bash
git clone https://github.com/ragnarok22/qvapay-python.git
cd qvapay-python
make install  # or: uv sync
```

### Commands

- `make tests` — run linting and tests with coverage
- `make coverage` — tests with terminal coverage report
- `make format` — auto-format with ruff
- `make lint` — check formatting without modifying files

## Migration guide

### 0.3.0 -> 0.9.0

- Imports moved from `qvapay.v1` to `qvapay` (e.g., `from qvapay import AsyncQvaPayClient`)
- Client methods are now organized into modules: `client.transactions.list()` instead of `client.get_transactions()`
- New `AsyncQvaPayMerchant` / `SyncQvaPayMerchant` for app-level operations (invoicing, balance)
- Standalone `auth`, `coins`, and `stocks` modules replace the old `QvaPayAuth` helper
- Client constructor takes `access_token` instead of `app_id` / `app_secret`

### 0.2.0 -> 0.3.0

- `QvaPayClient` was divided into two classes: `AsyncQvaPayClient` and `SyncQvaPayClient`. Both classes have the same methods and properties, with the difference that the methods in `AsyncQvaPayClient` are asynchronous and in `SyncQvaPayClient` are synchronous.

### 0.1.0 -> 0.2.0

- `user_id` of `Transaction` model was removed
- `paid_by_user_id` of `Transaction` model was removed

### 0.0.3 -> 0.1.0

- `from qvapay.v1 import *` instead of `from qvapay import *`
- `QvaPayClient` instead of `Client`
- `client.get_info` instead of `client.info`
- `client.get_balance` instead of `client.balance`
- `client.get_transactions` instead of `client.transactions`

## Contributors

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://bio.link/ragnarok22"><img src="https://avatars.githubusercontent.com/u/18733370?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Carlos Lugones</b></sub></a><br /><a href="https://github.com/ragnarok22/qvapay-python/commits?author=ragnarok22" title="Code">💻</a></td>
    <td align="center"><a href="http://codeshard.github.io/"><img src="https://avatars.githubusercontent.com/u/5880754?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ozkar L. Garcell</b></sub></a><br /><a href="https://github.com/ragnarok22/qvapay-python/commits?author=codeshard" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/leynier"><img src="https://avatars.githubusercontent.com/u/36774373?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Leynier Gutiérrez González</b></sub></a><br /><a href="https://github.com/ragnarok22/qvapay-python/commits?author=leynier" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/jorgeajimenezl"><img src="https://avatars.githubusercontent.com/u/18174581?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jorge Alejandro Jimenez Luna</b></sub></a><br /><a href="https://github.com/ragnarok22/qvapay-python/commits?author=jorgeajimenezl" title="Code">💻</a></td>
    <td align="center"><a href="https://blog.ragnarok22.dev"><img src="https://avatars.githubusercontent.com/u/8838803?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Reinier Hernández</b></sub></a><br /><a href="https://github.com/ragnarok22/qvapay-python/issues?q=author%3Aragnarok22" title="Bug reports">🐛</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

<p align="center">
    <img src="http://ForTheBadge.com/images/badges/made-with-python.svg">
</p>
