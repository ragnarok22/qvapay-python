install:
	uv sync

tests: install
	uv run flake8 . --count --show-source --statistics --max-line-length=88 --extend-ignore=E203
	uv run black . --check
	uv run isort . --profile=black
	uv run pre-commit run --all-files
	uv run pytest --cov=./ --cov-report=xml --junitxml=junit.xml -o junit_family=legacy
