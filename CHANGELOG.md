## v0.9.0 (2026-05-22)

### Breaking

- require Python 3.12 or newer
- flatten public imports under `qvapay` and remove the old `qvapay.v1` layout
- replace the previous monolithic client API with async and sync clients organized by modules
- use bearer-token authentication for user clients and UUID/secret authentication for merchant clients

### Feat

- add async and sync auth helpers for login, two-factor login, register, request PIN, token checks, and logout
- add merchant clients for invoices, transaction status, app balance, and app operations
- add modular support for transactions, payment links, withdrawals, P2P offers and messages, store products, top-ups, users, apps, coins, and stocks
- add transaction filters, nested transaction parsing, transfer responses as models, and PDF/share helpers
- add app creation with logo uploads and app update operations
- add coin categories, coin filters, per-coin price history, and P2P average parsing

### Fix

- align base URLs, endpoints, redirects, auth payloads, and request methods with the current QvaPay API
- correct payment link creation payloads, withdrawal retrieval IDs, transaction detail endpoints, and app response parsing
- prevent shared mutable defaults in clients and auth configuration
- improve API error reporting and response validation

### Refactor

- migrate package metadata and tooling from Poetry to uv and Hatchling
- replace Black, isort, and flake8 with Ruff-based formatting and linting
- simplify model parsing, standardize timeouts, and replace python-dateutil with standard datetime parsing
- align dataclass models with the updated API schemas and preserve extra response fields

### Docs

- overhaul README usage examples, migration notes, and developer commands
- add comprehensive API endpoint documentation
- update repository links, ownership metadata, contributor data, and agent guidance

### Test

- add comprehensive async and sync test coverage for clients, modules, models, auth flows, and API response parsing

### Build

- refresh dependency constraints and lockfile versions
- expand the CI Python matrix through Python 3.14 and update workflow actions
- configure coverage, JUnit reports, and authenticated Codecov uploads

## v0.3.0 (2021-10-30)

### Fix

- improve parsing method for evicting errors by fields aggregations

### Feat

- integrate pre-commit for avoid format errors
- split implementation in two classes

## v0.2.0 (2021-09-17)

### Fix

- add aclose method for async with and use run_until_complete
- remove user_id and paid_by_user_id properties from Transaction
- add type hint in __enter__ method of QvaPayClient class

### Feat

- add cache to GitHub Actions
- add context manager; updated README

## v0.1.0 (2021-09-05)

### Feat

- add post init validation to QvaPayAuth
- add not required status message to QvaPayError
- improve implementation

### Fix

- change UUID by str in remote_id of transaction model
- use python-dotenv for obtain authentication info from environment

### Perf

- remove pydantic dependency

## v0.0.3 (2021-08-30)

### Perf

- contributors
- contributors & deps
- added all contributors to README.md
- improved client
- preparing for publishing to pypi

### Fix

- switched from stage to production
- removed unused field
- improved imports
- improved imports
- removed unused code
- changed signed attr type
- fixed invoice model attrs
- fixed info model using alias values and str repr from datetimes
- path and pep8 fixes
- added vscode settings file
- error class for qvapay requests
- removed unused import

### Feat

- added github dependabot
- transaction endpoints
- fixed transaction model
- added alias to uuid field
- using json dataclass
- added link model
- renamed folder to better understanding of the project layout
- fixed info class and post init function
- using dataclass decorator, PEP 557 PEP 526
- qvapay client
