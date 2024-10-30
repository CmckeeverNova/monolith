.PHONY: run-server
run-server:
	poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload


.PHONY: check-formatting
check-formatting: ## Run formatting and linting checks
	poetry run isort --check-only . && poetry run black --check . && poetry run flake8 .

.PHONY fix-formatting: ## Run formatting and linting fixes
fix-formatting:
	poetry run isort . && poetry run black .

.PHONY: run-migrations ## Runs alembic migrations
run-migrations:
	poetry run alembic upgrade head

