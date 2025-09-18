# Guardian Agents Development Makefile
# All Python operations use uv

.PHONY: help install dev-install test lint format check clean reports validate

PYTHON := $(shell if [ -f .venv/bin/python ]; then echo .venv/bin/python; else echo python; fi)

# Default target
help:
	@echo "Guardian Agents Development Commands (using uv)"
	@echo ""
	@echo "Setup:"
	@echo "  install     Install project dependencies"
	@echo "  dev-install Install with development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  test        Run test suite"
	@echo "  lint        Run linting checks"
	@echo "  format      Format code"
	@echo "  check       Run all quality checks"
	@echo ""
	@echo "Project Management:"
	@echo "  reports     Generate all project reports"
	@echo "  validate    Run project validation"
	@echo "  track       Update progress tracking"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean       Clean build artifacts"
	@echo "  update-deps Update dependencies"

# Installation targets
install:
	uv pip install -e .

dev-install:
	uv pip install -e ".[dev,docs,validation]"

# Development targets
test:
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	$(PYTHON) -m ruff check src/ scripts/
	$(PYTHON) -m mypy src/ scripts/

format:
	$(PYTHON) -m black src/ scripts/ tests/
	$(PYTHON) -m ruff check --fix src/ scripts/ tests/

check: lint test
	@echo "All quality checks passed!"

# Project management targets
reports:
	$(PYTHON) scripts/generate-reports.py all

validate:
	$(PYTHON) scripts/track-progress.py calculate-completion

track:
	$(PYTHON) scripts/track-progress.py calculate-completion
	$(PYTHON) scripts/generate-reports.py weekly

# Maintenance targets
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

update-deps:
	uv pip install --upgrade -e ".[dev,docs,validation]"

# Environment management
env-create:
	uv venv .venv --python 3.13

env-activate:
	@echo "Run: source .venv/bin/activate"

env-reset: clean
	rm -rf .venv
	$(MAKE) env-create
	uv pip install -e ".[dev,docs,validation]"
