help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

format: ## Format code with ruff
	uv run ruff check --fix .
	uv run ruff format .

lint: ## Run linters (ruff check and format --check)
	uv run ruff check .
	uv run ruff format --check .

tests: install ## Run linters and tests with coverage
	uv run ruff check .
	uv run ruff format --check .
	uv run pre-commit run --all-files
	uv run pytest

coverage: install ## Run tests and show coverage report
	uv run pytest --cov-report=term-missing
