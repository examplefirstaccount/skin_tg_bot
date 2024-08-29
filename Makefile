# Linting and Formatting (CI step only)
lint:
	poetry run ruff check bot
	poetry run mypy bot
	poetry run black --check bot

format:
	poetry run black bot
	poetry run ruff check --fix bot

security-check:
	poetry run bandit -r bot

# Testing
test:
	poetry run pytest

# Migrations with Alembic
# Manually run when changes to models are made
generate:
	poetry run alembic revision --message="$(NAME)" --autogenerate

# Apply database migrations
migrate:
	poetry run alembic upgrade head

# Deployment Chain
deploy: test migrate
	poetry run python bot/main.py
	@echo "Deployment Successful"

# Launch Application Separately (if needed outside of deploy)
run:
	poetry run python bot/main.py
