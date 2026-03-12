# QvaPay API — Endpoint Reference

Base URL: `https://api.qvapay.com`

Authentication (unless stated otherwise): `Authorization: Bearer <token>`

---

## Models

### `AuthToken`
| Field | Type | Notes |
|-------|------|-------|
| `access_token` | `str` | JWT bearer token (valid 60 min by default) |
| `token_type` | `str` | Always `"Bearer"` |
| `me` | `User \| None` | Authenticated user object |

---

### `User`
| Field | Type |
|-------|------|
| `uuid` | `str` |
| `username` | `str` |
| `name` | `str` |
| `lastname` | `str` |
| `email` | `str` |
| `bio` | `str \| None` |
| `logo` | `str \| None` |
| `image` | `str \| None` |
| `cover` | `str \| None` |
| `balance` | `str \| None` |
| `pending_balance` | `str \| None` |
| `satoshis` | `int \| None` |
| `phone` | `str \| None` |
| `phone_verified` | `bool \| None` |
| `telegram` | `str \| None` |
| `twitter` | `str \| None` |
| `kyc` | `bool \| None` |
| `vip` | `bool \| None` |
| `golden_check` | `bool \| None` |
| `pin` | `int \| None` |
| `last_seen` | `str \| None` |
| `role` | `str \| None` |
| `p2p_enabled` | `bool \| None` |
| `created_at` | `str \| None` |
| `updated_at` | `str \| None` |

---

### `Transaction`
| Field | Type |
|-------|------|
| `uuid` | `str` |
| `amount` | `float` |
| `description` | `str` |
| `remote_id` | `str` |
| `status` | `str` — `"paid"`, `"pending"`, `"cancelled"` |
| `created_at` | `str` |
| `updated_at` | `str` |
| `app_id` | `int \| None` |
| `logo` | `str \| None` |
| `signed` | `str \| None` |
| `app` | `TransactionApp \| None` |
| `paid_by` | `TransactionUser \| None` |
| `app_owner` | `TransactionApp \| None` |
| `owner` | `TransactionUser \| None` |
| `wallet` | `Wallet \| None` |
| `servicebuy` | `ServiceBuy \| None` |

`TransactionDetail` extends `Transaction` with `paid_by_user_id: str | None`.

`PaginatedTransactions` wraps `List[Transaction]` with `current_page: int` and `total: int`.

---

### `Coin`
| Field | Type |
|-------|------|
| `id` | `str` |
| `name` | `str` |
| `logo` | `str` |
| `tick` | `str` |
| `price` | `str` |
| `enabled_in` | `bool` |
| `enabled_out` | `bool` |
| `enabled_p2p` | `bool` |
| `fee_in` | `str` |
| `fee_out` | `str` |
| `min_in` | `str` |
| `min_out` | `str` |
| `max_in` | `float \| None` |
| `max_out` | `float \| None` |
| `network` | `str \| None` |
| `coin_category` | `CoinCategory \| None` |

`CoinCategory` has `id: int`, `name: str`, `logo: str`, `coins: List[Coin]`.

---

### `Withdrawal`
| Field | Type |
|-------|------|
| `amount` | `float` |
| `transaction_id` | `str` |
| `id` | `int \| None` |
| `withdraw_id` | `str \| None` |
| `user_id` | `int \| None` |
| `receive` | `float \| None` |
| `receive_amount` | `float \| None` |
| `fee_to_apply` | `float \| None` |
| `payment_method` | `str \| None` |
| `coin` | `str \| None` |
| `details` | `str \| None` |
| `status` | `str \| None` |
| `tx_id` | `str \| None` |
| `created_at` | `str \| None` |
| `transaction` | `WithdrawTransaction \| None` |
| `coin_detail` | `WithdrawCoin \| None` |

---

### `P2POffer`
| Field | Type |
|-------|------|
| `uuid` | `str` |
| `coin` | `str` |
| `amount` | `float` |
| `price` | `float` |
| `type` | `str` — `"buy"` or `"sell"` |
| `status` | `str` |
| `owner` | `str \| None` |
| `created_at` | `str \| None` |

### `P2PMessage`
| Field | Type |
|-------|------|
| `uuid` | `str` |
| `message` | `str` |
| `sender` | `str` |
| `created_at` | `str` |

---

### `App`
| Field | Type |
|-------|------|
| `uuid` | `str` |
| `name` | `str` |
| `logo` | `str` |
| `url` | `str` |
| `description` | `str` |
| `callback` | `str` |
| `success_url` | `str` |
| `cancel_url` | `str` |
| `enabled` | `bool` |
| `active` | `bool` |
| `allowed_payment_auth` | `bool` |
| `card` | `bool` |
| `secret` | `str \| None` |
| `created_at` | `str \| None` |
| `updated_at` | `str \| None` |

---

### `Invoice`
| Field | Type |
|-------|------|
| `app_id` | `str` |
| `amount` | `str` |
| `description` | `str` |
| `remote_id` | `str` |
| `signed` | `str` |
| `transation_uuid` | `str` |
| `url` | `str` (payment URL) |
| `signedUrl` | `str \| None` |

---

### Other small models

| Model | Fields |
|-------|--------|
| `PaymentLink` | `name`, `product_id`, `amount`, `payment_link_url?`, `created_at?`, `updated_at?` |
| `PaymentMethod` | `uuid`, `name`, `details?`, `created_at?` |
| `Contact` | `uuid`, `name`, `username?`, `logo?` |
| `Domain` | `domain: str`, `available: bool` |
| `Product` | `uuid`, `name`, `description`, `price: float`, `logo?`, `category?`, `created_at?` |

---

## Auth

> No token needed for `login`, `register`, `request_pin`. Token is required for `check` and `logout`.

### `POST /auth/login`
Login with email and password.

**Body**
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `email` | `str` | ✅ | |
| `password` | `str` | ✅ | |
| `two_factor_code` | `str` | ❌ | 4-digit PIN from email or TOTP |
| `remember` | `bool` | ❌ | If `true`, returns a permanent token |

**Returns** → `AuthToken`

---

### `POST /auth/register`
Register a new user account.

**Body**
| Param | Type | Required |
|-------|------|----------|
| `name` | `str` | ✅ |
| `email` | `str` | ✅ |
| `password` | `str` | ✅ — min 8 chars with special characters |
| `lastname` | `str` | ❌ |
| `invite` | `str` | ❌ — referral code |
| `terms` | `bool` | ❌ — defaults to `true` |

**Returns** → `AuthToken` (unconfirmed; requires email verification)

---

### `POST /auth/request_pin`
Request a PIN code via email (used as 2FA for login).

**Body**
| Param | Type | Required |
|-------|------|----------|
| `email` | `str` | ✅ |

**Returns** → `None`

---

### `POST /auth/check`
Validate an access token.

**Returns** → `None` (raises `QvaPayError` if token is invalid)

---

### `GET /auth/logout`
Invalidate the current session token.

**Returns** → `None`

---

## Coins

> No authentication required.

### `GET /coins`
List all coins grouped by category.

**Returns** → `List[CoinCategory]`

---

### `GET /coins/v2`
List operational coins with optional filtering.

**Query params**
| Param | Type | Notes |
|-------|------|-------|
| `enabled_in` | `bool` | Filter coins that accept deposits |
| `enabled_out` | `bool` | Filter coins that allow withdrawals |
| `enabled_p2p` | `bool` | Filter coins available in P2P |

**Returns** → `List[Coin]`

---

### `GET /coins/{id}`
Get a specific coin by its numeric ID.

**Path params**
| Param | Type |
|-------|------|
| `id` | `int` |

**Returns** → `Coin`

---

### `GET /coins/price-history/{tick}`
Get price history for a coin.

**Path params**
| Param | Type | Notes |
|-------|------|-------|
| `tick` | `str` | Coin ticker, e.g. `"BTC"` |

**Query params**
| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `timeframe` | `str` | `"24H"` | e.g. `"24H"`, `"7D"`, `"30D"` |

**Returns** → `list` (raw JSON — list of price data points)

---

## Transactions

### `GET /transactions`
Get the last 30 transactions for the authenticated user.

**Query params**
| Param | Type | Notes |
|-------|------|-------|
| `start` | `str` | ISO datetime, e.g. `"2021-10-17 13:05:30"` |
| `end` | `str` | ISO datetime |
| `status` | `str` | `"paid"`, `"pending"`, or `"cancelled"` |
| `remote_id` | `str` | Filter by external reference ID |
| `description` | `str` | Filter by description text |

**Returns** → `List[Transaction]`

---

### `GET /transactions/sent`
Get the last 30 transactions sent by the authenticated user.

**Query params** — same as `GET /transactions`

**Returns** → `List[Transaction]`

---

### `GET /transactions/latest_sent`
Get the latest sent transactions for the authenticated user.

**Query params** — same as `GET /transactions`

**Returns** → `List[Transaction]`

---

### `GET /transaction/{uuid}`
Get full detail for a single transaction.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `TransactionDetail`

---

### `GET /transactions/{uuid}/pdf`
Download a transaction receipt as a PDF.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `bytes` (PDF content)

---

### `POST /transactions/transfer`
Transfer balance to another user.

**Body**
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `to` | `str` | ✅ | UUID, email, or phone number of recipient |
| `amount` | `float` | ✅ | |
| `description` | `str` | ❌ | |

**Returns** → `Transaction`

---

### `POST /transactions/transfer_app`
Transfer balance via app context.

**Body** — same as `/transactions/transfer`

**Returns** → `Transaction`

---

### `POST /transactions/pay`
Pay a pending transaction.

**Body**
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `uuid` | `str` | ✅ | UUID of the pending transaction |
| `pin` | `str` | ✅ | User's security PIN (default `"0000"`) |

**Returns** → `Transaction`

---

## User

### `GET /user/me`
Get the authenticated user's profile.

**Returns** → `User`

---

### `GET /user/me/extended`
Get extended user profile including ranking, completed P2P operations, and badges.

**Returns** → `User`

---

### `PUT /user/me`
Update the authenticated user's profile fields.

**Body** — any subset of writable `User` fields (e.g. `bio`, `phone`, `telegram`, `twitter`, `address`).

**Returns** → `User`

---

### `PUT /user/me/email`
Update user email. Sends a verification PIN to the new address on first call.

**Body**
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `email` | `str` | ✅ | New email address |
| `pin` | `str` | ❌ | Verification PIN (required on second call to confirm) |

**Returns** → `User`

---

### `PUT /user/me/username`
Update username. Must be unique.

**Body**
| Param | Type | Required |
|-------|------|----------|
| `username` | `str` | ✅ |

**Returns** → `User`

---

### `POST /user/me/avatar`
Upload a user avatar image (128×128 px, JPG/JPEG/PNG, max 5 MB).

**Body** — `multipart/form-data`
| Param | Type | Required |
|-------|------|----------|
| `avatar` | `file` | ✅ |

**Returns** → `User`

---

### `POST /user/me/cover`
Upload a user cover photo (1088×256 px, JPG/JPEG/PNG, max 10 MB).

**Body** — `multipart/form-data`
| Param | Type | Required |
|-------|------|----------|
| `cover` | `file` | ✅ |

**Returns** → `User`

---

### `GET /user/kyc`
Get current KYC (Know Your Customer) verification status.

**Returns** → `dict` (raw JSON)

---

### `POST /user/kyc`
Submit KYC verification documents.

**Body** — KYC fields (varies by verification level)

**Returns** → `dict` (raw JSON)

---

### `POST /user/topup`
Initiate a balance top-up.

**Body**
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `pay_method` | `str` | ✅ | e.g. `"BTCLN"`, `"USDT"` |
| `amount` | `float` | ✅ | |
| `webhook_url` | `str` | ❌ | URL to receive webhook notification |

**Returns** → `dict` with `response`, `coin`, `value`, `wallet`, `price`, `transaction_id`

---

### `POST /user/search`
Search for users by username, email, or phone.

**Body**
| Param | Type | Required |
|-------|------|----------|
| `query` | `str` | ✅ |

**Returns** → `List[User]`

---

### `GET /user/referrals`
Get the list of users referred by the authenticated user.

**Returns** → `dict` (raw JSON)

---

### `GET /user/gold`
Get the authenticated user's gold membership status.

**Returns** → `dict` (raw JSON)

---

### `POST /user/gold`
Purchase a gold membership.

**Body** — gold plan parameters

**Returns** → `dict` (raw JSON)

---

### `GET /user/savings`
Get savings account status and balance.

**Returns** → `dict` (raw JSON)

---

### `GET /user/payment_methods`
List saved payment methods (wallets, banks, etc.).

**Returns** → `List[PaymentMethod]`

---

### `POST /user/payment_methods`
Save a new payment method.

**Body** — payment method fields (e.g. `name`, `details`)

**Returns** → `PaymentMethod`

---

### `GET /user/payment_links`
List saved payment links for the user.

**Returns** → `List[PaymentLink]`

---

### `POST /user/payment_links`
Create a new payment link for the user.

**Body** — payment link fields (e.g. `name`, `product_id`, `amount`)

**Returns** → `PaymentLink`

---

### `DELETE /user/payment_links/{uuid}`
Delete a payment link by UUID.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `None`

---

### `GET /user/contacts`
List saved contacts.

**Returns** → `List[Contact]`

---

### `POST /user/contacts`
Save a new contact.

**Body** — contact fields (e.g. `uuid`, `name`)

**Returns** → `Contact`

---

### `GET /user/domains/check`
Check whether a QvaPay username/domain is available.

**Query params**
| Param | Type | Required |
|-------|------|----------|
| `domain` | `str` | ✅ |

**Returns** → `Domain`

---

### `POST /user/domains/available`
Request an available domain.

**Body** — domain fields

**Returns** → `Domain`

---

## Withdraw

### `POST /withdraw`
Create a withdrawal to an external destination.

**Body**
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `pay_method` | `str` | ✅ | e.g. `"USDT"`, `"BTCLN"`, `"BANK_MLC"` |
| `amount` | `float` | ✅ | |
| `details` | `dict` | ✅ | Destination info, e.g. `{"Wallet": "..."}` for crypto |
| `pin` | `int` | ❌ | Can be omitted if wallet is pre-saved |
| `note` | `str` | ❌ | Personal note for the record |

**Returns** → `Withdrawal`

---

### `GET /withdraws`
Get the last 10 withdrawals for the authenticated user.

**Returns** → `List[Withdrawal]`

---

### `GET /withdraw/{id}`
Get withdrawal details by numeric ID.

**Path params**
| Param | Type |
|-------|------|
| `id` | `int` |

**Returns** → `Withdrawal`

---

### `POST /withdraw/balance`
Get withdrawal balance/fee preview.

**Returns** → `dict` (raw JSON)

---

## Payment Links

> Note: these are global payment links, distinct from per-user payment links under `/user/payment_links`.

### `GET /payment_links`
List all payment links for the authenticated user.

**Returns** → `List[PaymentLink]`

---

### `POST /payment_links/create`
Create a new payment link.

**Body**
| Param | Type | Required |
|-------|------|----------|
| `name` | `str` | ✅ |
| `product_id` | `str` | ✅ |
| `amount` | `float` | ✅ |

**Returns** → `PaymentLink`

---

## Apps (Development)

### `GET /app`
List all development apps owned by the authenticated user.

**Returns** → `List[App]`

---

### `GET /app/{uuid}`
Get a specific dev app by UUID.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `App`

---

### `POST /app/create`
Create a new development app.

**Body** — `multipart/form-data`
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | `str` | ✅ | |
| `url` | `str` | ✅ | App URL |
| `desc` | `str` | ✅ | Description |
| `callback` | `str` | ✅ | Webhook callback URL |
| `logo` | `file` | ❌ | App logo image |
| `success_url` | `str` | ❌ | Redirect on success |
| `cancel_url` | `str` | ❌ | Redirect on cancel |

**Returns** → `App`

---

### `DELETE /app/{uuid}`
Delete a development app.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `App` (the deleted app)

---

## P2P

### `GET /p2p`
List open P2P offers (public; delay depends on user tier).

**Query params**
| Param | Type | Notes |
|-------|------|-------|
| `type` | `str` | `"buy"` or `"sell"` |
| `min` | `float` | Minimum amount |
| `max` | `float` | Maximum amount |
| `coin` | `str` | Coin ticker |
| `my` | `bool` | If `true`, show only your own offers |
| `vip` | `bool` | If `true`, show only VIP offers |

**Returns** → `List[P2POffer]`

---

### `GET /p2p/my`
List the authenticated user's own P2P offers.

**Returns** → `List[P2POffer]`

---

### `GET /p2p/average`
Get the weighted average P2P exchange rate for a coin.

**Query params**
| Param | Type | Required |
|-------|------|----------|
| `coin` | `str` | ✅ |

**Returns** → `dict` (raw JSON — average rate data)

---

### `GET /p2p/averages`
Get average P2P exchange rates for all coins.

**Returns** → `dict` (raw JSON)

---

### `GET /p2p/completed_pairs_average`
Get the average exchange rate from completed P2P pairs in the last week.

**Query params**
| Param | Type | Required |
|-------|------|----------|
| `coin` | `str` | ✅ — uppercased automatically |

**Returns** → `float`

---

### `GET /p2p/total_public_open_ops`
Get the total count of publicly visible open P2P operations.

**Returns** → `dict` (raw JSON)

---

### `GET /p2p/{uuid}`
Get a specific P2P offer (authenticated; must be open or user must be a peer).

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `P2POffer`

---

### `GET /p2p/{uuid}/public`
Get public data of a P2P offer.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `P2POffer`

---

### `POST /p2p`
Create a new P2P offer.

**Body**
| Param | Type | Notes |
|-------|------|-------|
| `type` | `str` | `"buy"` or `"sell"` |
| `coin` | `str` | Coin ticker |
| `amount` | `float` | Amount to trade |
| `receive` | `float` | Amount to receive |
| `only_vip` | `bool` | Restrict to VIP users |
| `only_kyc` | `bool` | Restrict to KYC-verified users |
| `private` | `bool` | Make offer private |

**Returns** → `P2POffer`

---

### `POST /p2p/{uuid}/edit`
Edit an existing P2P offer.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Body** — same fields as create offer (partial update)

**Returns** → `P2POffer`

---

### `POST /p2p/{uuid}/apply`
Apply to participate in a P2P offer.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `dict` (raw JSON)

---

### `POST /p2p/{uuid}/mark_paid`
Mark a P2P trade as paid (buyer action).

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `dict` (raw JSON)

---

### `POST /p2p/{uuid}/confirm_received`
Confirm receipt of payment (seller action — releases crypto).

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `dict` (raw JSON)

---

### `POST /p2p/{uuid}/cancel`
Cancel a P2P offer.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `dict` (raw JSON)

---

### `POST /p2p/{uuid}/rate`
Rate a completed P2P trade.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Body**
| Param | Type | Required |
|-------|------|----------|
| `rating` | `int` | ✅ |

**Returns** → `dict` (raw JSON)

---

### `GET /p2p/{uuid}/chat`
Retrieve chat messages for a P2P trade.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `List[P2PMessage]`

---

### `POST /p2p/{uuid}/chat`
Send a chat message in a P2P trade.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Body**
| Param | Type | Required |
|-------|------|----------|
| `message` | `str` | ✅ |

**Returns** → `P2PMessage`

---

## Merchant (App-authenticated)

> These endpoints authenticate via `app_id` + `app_secret` in the POST body (no Bearer token needed).
> Obtain credentials at [qvapay.com/apps/create](https://qvapay.com/apps/create).

### `POST /info`
Get information about the merchant app.

**Body**
| Param | Type |
|-------|------|
| `app_id` | `str` |
| `app_secret` | `str` |

**Returns** → `App`

---

### `POST /balance`
Get the balance of the app owner's account.

**Body** — `app_id` + `app_secret`

**Returns** → `float`

---

### `POST /create_invoice`
Create a payment invoice.

**Body**
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `app_id` | `str` | ✅ | |
| `app_secret` | `str` | ✅ | |
| `amount` | `float` | ✅ | |
| `description` | `str` | ✅ | |
| `remote_id` | `str` | ✅ | Your internal order/reference ID |
| `signed` | `int` | ❌ | `1` to get a signed URL |

**Returns** → `Invoice`

---

### `POST /modify_invoice`
Modify an existing invoice.

**Body**
| Param | Type | Required |
|-------|------|----------|
| `app_id` | `str` | ✅ |
| `app_secret` | `str` | ✅ |
| `uuid` | `str` | ✅ |
| *(other invoice fields)* | | ❌ |

**Returns** → `Invoice`

---

### `POST /transactions`
Get paginated transaction list for the merchant app.

**Body** — `app_id` + `app_secret`

**Returns** → `PaginatedTransactions`

---

### `POST /transaction_status`
Check the status of a specific transaction.

**Body**
| Param | Type | Required |
|-------|------|----------|
| `app_id` | `str` | ✅ |
| `app_secret` | `str` | ✅ |
| `uuid` | `str` | ✅ |

**Returns** → `dict` (raw JSON)

---

### `POST /payments_authorization`
Get a temporary authorization URL to connect a QvaPay user to an external system.

**Body**
| Param | Type | Required |
|-------|------|----------|
| `app_id` | `str` | ✅ |
| `app_secret` | `str` | ✅ |
| *(authorization params)* | | ❌ |

**Returns** → `dict` (raw JSON — includes temporary URL)

---

### `POST /charge_user`
Charge a user account using a previously obtained authorization token.

**Body**
| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `app_id` | `str` | ✅ | |
| `app_secret` | `str` | ✅ | |
| `user_uuid` | `str` | ✅ | UUID of the user to charge |
| *(charge params)* | | ❌ | |

**Returns** → `dict` (raw JSON)

---

## Store

### `GET /store/products`
List all available store products.

**Returns** → `List[Product]`

---

### `GET /store/my_products`
List products purchased by the authenticated user.

**Returns** → `List[Product]`

---

### `GET /store/my_products/{uuid}`
Get details of a specific purchased product.

**Path params**
| Param | Type |
|-------|------|
| `uuid` | `str` |

**Returns** → `Product`
