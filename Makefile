# Makefile for development tasks
# Usage:
#   make dev               # start fastapi dev server and celery worker concurrently
#   make run-server        # start only the fastapi dev server
#   make run-celery       # start only the celery worker (foreground)
#   make run-celery-bg     # start celery in background and write pid/logs
# Notes: commands run with PYTHONPATH set to project root so "src" imports resolve.

.PHONY: dev run-server run-celery run-celery-bg stop clean-logs

PYTHONPATH := .

# Use the fastapi CLI as requested via bash -c. This requires `fastapi` to be
# installed in your environment (pip install fastapi[all] provides the CLI).
FASTAPI_CMD := bash -c 'fastapi dev backend/src/'

CELERY_CMD := bash -c 'celery -A backend.src.celery_tasks.celery_app worker --loglevel=info'

NODE_FRONTEND_COMMAND := bash -c 'npm --prefix frontend/coding-interview run dev'

dev:
	@echo "Starting fastapi dev server and celery worker (press Ctrl-C to stop)..."
	PYTHONPATH=$(PYTHONPATH) $(FASTAPI_CMD) & \
	PYTHONPATH=$(PYTHONPATH) $(CELERY_CMD) & \
	PYTHONPATH=$(PYTHONPATH) $(NODE_FRONTEND_COMMAND) & \
	wait

run-server:
	@echo "Starting fastapi dev server..."
	PYTHONPATH=$(PYTHONPATH) $(FASTAPI_CMD)

run-celery:
	@echo "Starting celery worker (foreground)..."
	PYTHONPATH=$(PYTHONPATH) $(CELERY_CMD)

run-frontend:
	@echo "starting frontend server"
	PYTHONPATH=$(PYTHONPATH) $(NODE_FRONTEND_COMMAND)

# Start celery in background, store pid and log output to logs/celery.log
run-celery-bg:
	@mkdir -p logs
	@echo "Starting celery worker in background (logs/celery.log)..."
	PYTHONPATH=$(PYTHONPATH) nohup sh -c "$(CELERY_CMD)" > logs/celery.log 2>&1 & echo $$! > celery.pid
	@echo "celery pid: `cat celery.pid`"

stop:
	@echo "To stop processes started by 'make dev' just Ctrl-C that terminal.\n"
	@echo "If you started celery with run-celery-bg you can stop it with:"
	@echo "  kill `cat celery.pid` && rm -f celery.pid"

clean-logs:
	@rm -rf logs && rm -f celery.pid

# TO DO:
# - lint: run flake8/ruff
# - format: run black/isort
# - typecheck: run mypy or ruff with --select
# - test: run pytest
# - db-migrate: run alembic migrations
# - seed: run a script to seed the DB
# - docker-build / docker-run: build and run containers

