SHELL=/usr/bin/env bash

# Environment configuration
ENV_NAME = dra
PYTHON_VERSION ?= 3.13  # Default to 3.13 (system Python), but allow override

# Default goal
.DEFAULT_GOAL := help

# 🛠️ Create virtual environment using uv
.PHONY: venv
venv:
	@echo "Creating virtual environment with uv (Python $(PYTHON_VERSION))"
	uv python pin $(PYTHON_VERSION)
	uv venv .venv --python $(PYTHON_VERSION)
	@echo "Virtual environment created at .venv"
	@echo "To activate: source .venv/bin/activate"

# 🛠️ Create virtual environment with system Python
.PHONY: venv-system
venv-system:
	@echo "Creating virtual environment with system Python"
	uv venv .venv --python-preference system
	@echo "Virtual environment created at .venv"
	@echo "To activate: source .venv/bin/activate"

# 🛠️ Install dependencies using uv
.PHONY: install
install:
	@echo "Installing dependencies with uv"
	uv sync --all-extras
	@echo "Installing playwright browsers"
	uv run playwright install chromium --with-deps --no-shell
	@echo "Installation complete"

# 🛠️ Install development dependencies
.PHONY: install-dev
install-dev:
	@echo "Installing with development dependencies"
	uv sync --all-extras --dev
	uv run playwright install chromium --with-deps --no-shell

# 🛠️ Install dependencies from lock file only
.PHONY: install-locked
install-locked:
	@echo "Installing locked dependencies"
	uv sync --frozen
	uv run playwright install chromium --with-deps --no-shell

# 🛠️ Add a new dependency
.PHONY: add
add:
ifdef PKG
	@echo "Adding package: $(PKG)"
	uv add $(PKG)
else
	@echo "Usage: make add PKG=package-name"
endif

# 🛠️ Remove a dependency
.PHONY: remove
remove:
ifdef PKG
	@echo "Removing package: $(PKG)"
	uv remove $(PKG)
else
	@echo "Usage: make remove PKG=package-name"
endif

# 🛠️ Update dependencies
.PHONY: update
update:
	@echo "Updating dependencies"
	uv lock --upgrade

# 🛠️ Run the main application
.PHONY: run
run:
	uv run python main.py

# 🛠️ Run example scripts
.PHONY: run-general
run-general:
	uv run python examples/run_general.py

.PHONY: run-gaia
run-gaia:
	uv run python examples/run_gaia.py

.PHONY: run-hle
run-hle:
	uv run python examples/run_hle.py

# 🛠️ Run tests
.PHONY: test
test:
	uv run pytest

# 🛠️ Code formatting and linting
.PHONY: format
format:
	uv run black .
	uv run isort .

.PHONY: lint
lint:
	uv run ruff check .
	uv run mypy src/

.PHONY: lint-fix
lint-fix:
	uv run ruff check --fix .
	uv run ruff format .

# 🛠️ Clean up
.PHONY: clean
clean:
	@echo "Cleaning up virtual environment and cache"
	rm -rf .venv
	rm -rf .uv-cache
	rm -rf __pycache__
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +

# 🛠️ Show project info
.PHONY: info
info:
	@echo "Project information:"
	uv tree
	@echo ""
	@echo "Python version:"
	uv run python --version

# 🛠️ Show available Makefile commands
.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "  make venv        - Create virtual environment with uv"
	@echo "  make venv-system - Create virtual environment with system Python"
	@echo "  make install     - Install all dependencies"
	@echo "  make install-dev - Install with development dependencies"
	@echo "  make install-locked - Install from lock file only"
	@echo "  make add PKG=... - Add a new dependency"
	@echo "  make remove PKG=... - Remove a dependency"
	@echo "  make update      - Update all dependencies"
	@echo "  make run         - Run the main application"
	@echo "  make run-general - Run general example"
	@echo "  make run-gaia    - Run GAIA example"
	@echo "  make run-hle     - Run HLE example"
	@echo "  make test        - Run tests"
	@echo "  make format      - Format code with black and isort"
	@echo "  make lint        - Run linting with ruff and mypy"
	@echo "  make lint-fix    - Auto-fix linting issues with ruff"
	@echo "  make clean       - Clean up virtual environment and cache"
	@echo "  make info        - Show project information"
