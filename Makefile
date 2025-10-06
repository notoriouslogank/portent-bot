.PHONY: dev run fmt lint test sync-global

dev: ## run with guild sync
	@export SYNC_MODE=guild; python3 -m src.portent.bot

run: ## run without resync (faster)
	@export SYNC_MODE=none; python3 -m src.portent.bot

fmt:
	ruff check --fix .
	ruff format .

lint:
	ruff check .
	ruff format --check .

test:
	pytest -q

sync-global:
	@export SYNC_MODE=global; python3 -m src.portent.bot
