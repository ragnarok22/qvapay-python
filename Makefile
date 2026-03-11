help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

format: ## Format code with black and isort
	uv run black .
	uv run isort . --profile=black

lint: ## Run linters (flake8, black --check, isort --check)
	uv run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203 --exclude=.venv
	uv run black . --check
	uv run isort . --check --profile=black

tests: install ## Run linters and tests with coverage
	uv run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203 --exclude=.venv
	uv run black . --check
	uv run isort . --profile=black
	uv run pre-commit run --all-files
	uv run pytest --cov=./ --cov-report=xml --junitxml=junit.xml -o junit_family=legacy
