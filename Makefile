# Makefile — единая точка входа для окружения и качества кода (stateless)

PYTHON := .venv/bin/python
PIP := .venv/bin/pip

BLACK := .venv/bin/black
ISORT := .venv/bin/isort
FLAKE8 := .venv/bin/flake8
MYPY := .venv/bin/mypy

PYTEST := .venv/bin/pytest

PIP_MISSING := .venv/bin/pip-missing-reqs
PIP_EXTRA := .venv/bin/pip-extra-reqs

SRC_DIR := src
TEST_DIR := tests

REQ_FILE := requirements.txt
REQ_DEV_FILE := requirements-dev.txt

.PHONY: help venv install install-dev run format lint typecheck test check-requirements check clean

help:
	@echo "Targets:"
	@echo "  make venv                 - create .venv"
	@echo "  make install              - install prod deps"
	@echo "  make install-dev          - install dev deps"
	@echo "  make run                  - run app using venv python"
	@echo "  make format               - format code (black + isort)"
	@echo "  make lint                 - style checks (flake8 + black/isort check)"
	@echo "  make typecheck            - mypy typecheck"
	@echo "  make test                 - pytest + coverage"
	@echo "  make check-requirements   - imports vs requirements.txt"
	@echo "  make check                - lint + typecheck + req-check + tests"
	@echo "  make clean                - remove venv and caches"

venv:
	python3 -m venv .venv
	$(PIP) install --upgrade pip setuptools wheel

install: venv
	$(PIP) install -r $(REQ_FILE)

install-dev: install
	$(PIP) install -r $(REQ_DEV_FILE)

run: install
	$(PYTHON) -m src.weather

format: install-dev
	$(BLACK) $(SRC_DIR) $(TEST_DIR)
	$(ISORT) $(SRC_DIR) $(TEST_DIR)

lint: install-dev
	$(FLAKE8) $(SRC_DIR) $(TEST_DIR)
	$(BLACK) --check --diff $(SRC_DIR) $(TEST_DIR)
	$(ISORT) --check-only --diff $(SRC_DIR) $(TEST_DIR)

typecheck: install-dev
	$(MYPY) $(SRC_DIR) $(TEST_DIR) --strict --ignore-missing-imports

test: install-dev
	$(PYTEST) $(TEST_DIR) -v --cov=$(SRC_DIR) --cov-report=term-missing --cov-fail-under=80

check-requirements: install-dev
	$(PIP_MISSING) $(SRC_DIR) --requirements-file=$(REQ_FILE)
	$(PIP_EXTRA) $(SRC_DIR) --requirements-file=$(REQ_FILE)

check: lint typecheck check-requirements test
	@echo "OK: all checks passed"

clean:
	rm -rf .venv
	rm -rf .mypy_cache .pytest_cache htmlcov
	rm -f .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true