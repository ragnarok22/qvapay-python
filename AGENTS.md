# Repository Guidelines

## Project Structure & Module Organization
Core package code lives in `qvapay/`. The async implementation in `qvapay/v1/_async/` is the source of truth; `qvapay/v1/_sync/` is generated from it and should be refreshed, not hand-maintained. Shared dataclass models live in `qvapay/v1/models/`; `auth.py`, `errors.py`, `http_clients.py`, and `utils.py` handle credentials, exceptions, transport helpers, and response parsing. Tests mirror the package layout under `tests/v1/_async/` and `tests/v1/_sync/`.

## Architecture Overview
Both `AsyncQvaPayClient` and `SyncQvaPayClient` expose five methods: `get_info()`, `get_balance()`, `get_transactions()`, `get_transaction()`, and `create_invoice()`. `http_clients.py` keeps sync and async transport aligned, and model `from_json()` methods handle API field aliasing. Update the async path first, then regenerate the sync copy.

## Build, Test, and Development Commands
- `make install` or `uv sync` installs the package and dev tooling into `.venv`.
- `make tests` runs `flake8`, `black --check`, `isort`, `pre-commit`, and `pytest --cov=./ --cov-report=xml`.
- `uv run pytest` runs the test suite without the linting steps.
- `uv run pytest tests/v1/_async/test_client.py` runs a focused test module.
- `uv run pytest tests/v1/_sync/test_client.py::test_get_info` runs a single test.
- `uv build` creates distributable packages in `dist/`.

## Coding Style & Naming Conventions
Target Python 3.10+ and use 4-space indentation. Keep lines within 88 characters to match `black` and `flake8`. Use `snake_case` for modules, functions, and tests; use `PascalCase` for dataclasses and client classes such as `AsyncQvaPayClient`. Prefer type annotations on public APIs. Formatting is enforced by `black`, `isort --profile=black`, `flake8`, `autoflake`, and the hooks in `.pre-commit-config.yaml`.

## Testing Guidelines
Tests use `pytest`, `pytest-cov`, and `anyio`. Name files `test_*.py` and keep test functions focused, for example `test_get_balance`. Tests exercise the live QvaPay API, so set `QVAPAY_APP_ID` and `QVAPAY_APP_SECRET` in your environment or `.env`; `python-dotenv` loads them locally. Add or update tests for both async and sync surfaces when the public API changes.

## Commit & Pull Request Guidelines
Recent history follows Conventional Commit style, for example `build: ...`, `ci(workflow): ...`, and `chore(metadata): ...`. Keep commit subjects imperative and scoped when useful. PRs should explain the change, link related issues, and note required credential or API setup. Update `README.md` or `CHANGELOG.md` when behavior or packaging changes are visible.

## Security & Configuration Tips
Do not commit `.env` files or real QvaPay credentials. Keep secrets in local environment variables and GitHub Actions secrets. Because tests hit external services, avoid running them against production credentials you do not control.
