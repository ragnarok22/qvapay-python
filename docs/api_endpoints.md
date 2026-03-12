# QvaPay API Reference

This repository now treats the published Postman document as the only API source
of truth:

- https://documenter.getpostman.com/view/8765260/TzzHnDGw

The published collection metadata fetched from that document on March 12, 2026
shows a publish date of March 13, 2025 and uses these base URLs:

- Public API: `https://api.qvapay.com`
- Merchant API: `https://api.qvapay.com/v2`

## Route Summary

### Authentication

- `POST /auth/login`
- `POST /auth/request-pin`
- `POST /auth/register`
- `POST /auth/check`
- `GET /auth/logout`

### Apps

- `GET /app`
- `GET /app/{uuid}`
- `DELETE /app/{uuid}`
- `POST /app/create`

### Coins and Stocks

- `GET /coins`
- `GET /coins/v2`
- `GET /coins/{id}`
- `GET /coins/price-history/{tick}`
- `GET /stocks/index`

### Transactions

- `GET /transaction`
- `GET /transaction/latestusers`
- `GET /transaction/{uuid}`
- `GET /transaction/{uuid}/pdf`
- `POST /transaction/transfer`
- `POST /transaction/{uuid}/pay`

Notes:
- Sent-to-user lookups are the same `GET /transaction` endpoint with query
  parameters such as `user_uuid` and `take`.
- The published collection uses the same transfer endpoint for both regular and
  app transfer examples.

### Withdraw

- `POST /withdraw`
- `GET /withdraw`
- `GET /withdraw/{id}`

### User

- `GET /user`
- `GET /user/extended`
- `PUT /user/update`
- `PUT /user/update/email`
- `PUT /user/update/username`
- `POST /user/avatar`
- `GET /user/kyc`
- `POST /user/kyc`
- `POST /topup`
- `POST /user/search`
- `GET /user/referrals`
- `GET /user/gold`
- `POST /user/gold`
- `GET /saving`

### User Payment Methods, Links, Contacts, Domains

- `GET /user/payment-methods`
- `POST /user/payment-methods`
- `GET /user/payment-links`
- `DELETE /user/payment-links`
- `POST /user/payment-links`
- `GET /user/contact`
- `POST /user/contact`
- `GET /domain`
- `POST /domain`

Notes:
- The published collection documents payment-link deletion as `DELETE
  /user/payment-links` with a JSON body containing `id`.

### P2P

- `GET /p2p`
- `GET /p2p/average`
- `GET /p2p/averages`
- `GET /p2p/completed_pairs_average`
- `GET /p2p/get_total_operations`
- `GET /p2p/{uuid}`
- `GET /p2p/{uuid}/pub`
- `POST /p2p/create`
- `POST /p2p/{uuid}/edit`
- `POST /p2p/{uuid}/apply`
- `POST /p2p/{uuid}/paid`
- `POST /p2p/{uuid}/received`
- `POST /p2p/{uuid}/cancel`
- `POST /p2p/{uuid}/rate`
- `GET /p2p/{uuid}/chat`
- `POST /p2p/{uuid}/chat`

Notes:
- "My offers" are documented as `GET /p2p?my=true`, not a separate `/p2p/my`
  route.

### Merchant

- `POST /v2/info`
- `POST /v2/balance`
- `POST /v2/create_invoice`
- `POST /v2/modify_invoice`
- `POST /v2/transactions`
- `POST /v2/transactions/{uuid}`
- `POST /v2/authorize_payments`
- `POST /v2/charge`

### Global Payment Links

- `GET /payment_links`
- `POST /payment_links/create`

### Store

- `GET /store`
- `GET /store/my`
- `GET /store/my/{id}`
- `GET /store/phone_package`
- `POST /store/phone_package`
- `GET /store/visa_card`
- `POST /store/visa_card`
- `GET /store/gift-card`
- `GET /store/gift-card/{id}`
- `POST /store/gift-card`

Notes:
- The collection shows the gift-card detail and purchased-product detail routes
  with a blank trailing path segment in examples; this SDK treats those as
  path-parameter routes.
