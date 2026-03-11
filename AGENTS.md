# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python SDK for the QvaPay API — provides both async (`AsyncQvaPayClient`) and sync (`SyncQvaPayClient`) clients, plus `AsyncQvaPayMerchant` / `SyncQvaPayMerchant` for app-level operations.

## Build, Test, and Development Commands

- `make install` or `uv sync` — install package and dev dependencies
- `make tests` — run ruff linting, pre-commit hooks, and pytest with coverage
- `make coverage` — run tests with terminal coverage report
- `make format` — auto-format with ruff
- `make lint` — check formatting without modifying files
- `uv run pytest` — run tests only (no linting)
- `uv run pytest tests/test_transactions.py` — run a single test module
- `uv run pytest tests/test_transactions.py::TestAsyncTransactionsList::test_list_no_filters` — run a single test
- `uv build` — create distributable packages

## Architecture

### Async-first with sync mirror
`qvapay/_async/` is the source of truth; `qvapay/_sync/` mirrors it with synchronous equivalents. When adding features, implement in async first, then create the sync counterpart. Both clients share the same dataclass models and `http.py` transport layer.

### Client structure
`AsyncQvaPayClient` / `SyncQvaPayClient` are Bearer-token-authenticated user clients. They compose functionality via modules:
- `client.transactions` — list, get, transfer, pay, get PDF
- `client.app` — app info
- `client.user` — user profile
- `client.payment_links` — CRUD for payment links
- `client.withdraw` — withdrawal operations
- `client.p2p` — peer-to-peer offers/messages
- `client.store` — store products

`AsyncQvaPayMerchant` / `SyncQvaPayMerchant` are UUID+secret-authenticated app clients for merchant operations (invoices, transaction status, balance).

### Standalone modules
`qvapay._async.auth` / `qvapay._sync.auth` — login, register, request_pin, check, logout (no client instance needed).
`qvapay._async.coins` / `qvapay._sync.coins` and `stocks` — standalone functions.

### Models
Dataclass models in `qvapay/models/` each have a `from_json()` classmethod that uses `utils.parse_json()` for flexible deserialization (handles extra API fields via `setattr`). Nested objects (e.g., `Transaction.wallet`, `Transaction.servicebuy`) are manually parsed in `from_json()`.

### HTTP layer
`qvapay/http.py` re-exports `httpx.AsyncClient`, wraps `httpx.Client` as `SyncClient` (adding an `aclose()` alias), and defines `BASE_URL`, `DEFAULT_TIMEOUT`, and `TimeoutTypes`.

### Error handling
`qvapay/utils.py:validate_response()` raises `QvaPayError(status_code, message)` on non-success or HTML responses. All module methods call this after every HTTP request.

## Coding Style

- Python 3.10+, 88-char line length
- Formatting enforced by `ruff` (replaces black/flake8/isort/autoflake)
- Pre-commit hooks: trailing-whitespace, check-added-large-files, mixed-line-ending, ruff check+format

## Testing

- Tests use `pytest` with `pytest-cov` and `anyio` (for async tests marked with `@pytest.mark.anyio`)
- Tests live in `tests/` (flat structure, not mirroring `_async`/`_sync`)
- Tests mock `httpx` clients with `unittest.mock.AsyncMock` / `MagicMock` — no live API calls
- Coverage config in `pyproject.toml`: `--cov=qvapay --cov-report=xml`

## Commit Style

Conventional Commits: `feat(scope): ...`, `fix(scope): ...`, `test(scope): ...`, `build: ...`, etc.
