#doc#
#doc# python-project-foundry - Makefile
#doc#
#doc# Purpose: Automate common development tasks, including managing the project's virtual environment, running tests,
#doc# and doing autoformatting.
#doc#
#doc# Usage: run `make <target>` (common targets: template, setup, check, test, format, clean, help).
#doc#
#doc# Notes:
#doc#   - This Makefile installs `uv` when needed (configurable via UV). See https://docs.astral.sh/uv/.
#doc#   - A project virtualenv is created in .venv by default (UV_PROJECT_ENVIRONMENT).
#doc#   - The `help` target prints any Makefile lines prefixed with `#doc# `; avoid leading underscores for visible
#doc#     targets.
#doc#

### Make configurations
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

### Tooling
UV_VERSION ?= 0.12.1
UV_INSTALL_DIR ?= $(HOME)/.local/bin
UV_INSTALL_URL ?= https://astral.sh/uv/$(UV_VERSION)/install.sh
UV ?= uv
DEST ?=
PPF_ENVIRONMENT ?= $(HOME)/.cache/python-project-foundry/venv
PPF_ARGS ?=
PYTEST_ARGS ?=
RUFF_ARGS ?= .
MKDOCS_ARGS ?=
LINKCHECK_REPORT ?= reports/linkchecker.xml

### Make a standalone uv installation available to this Make process
export PATH := $(UV_INSTALL_DIR):$(HOME)/.cargo/bin:$(PATH)

### Force an in-project virtualenv for determinism
export UV_PROJECT_ENVIRONMENT ?= .venv

.DEFAULT_GOAL := help

.PHONY: help
.PHONY: bootstrap setup template
.PHONY: format fmt lint typecheck test test-cov check all
.PHONY: docs docs-linkcheck serve-docs
.PHONY: precommit build
.PHONY: lock update clean

### Helper targets

help:  #doc# Show this help
	@sed -ne '/@sed/!s/#doc#//p' $(MAKEFILE_LIST) | grep -v '^_'

bootstrap:  #doc# Install a compatible uv version when it is not already available
	@uv_version=""; \
	if command -v "$(UV)" >/dev/null 2>&1; then \
	  uv_version=$$("$(UV)" --version | awk '{ print $$2 }'); \
	fi; \
	if [ -n "$$uv_version" ] && echo "$$uv_version" | awk -F. \
	  '{ exit !($$1 == 0 && (($$2 == 11 && $$3 + 0 >= 8) || $$2 == 12)) }'; then \
	  "$(UV)" --version; \
	else \
	  echo "Compatible uv not found; installing uv $(UV_VERSION) to $(UV_INSTALL_DIR)."; \
	  if command -v curl >/dev/null 2>&1; then \
	    curl -LsSf "$(UV_INSTALL_URL)" | env UV_INSTALL_DIR="$(UV_INSTALL_DIR)" UV_NO_MODIFY_PATH=1 sh; \
	  elif command -v wget >/dev/null 2>&1; then \
	    wget -qO- "$(UV_INSTALL_URL)" | env UV_INSTALL_DIR="$(UV_INSTALL_DIR)" UV_NO_MODIFY_PATH=1 sh; \
	  else \
	    echo "Cannot install uv: curl or wget is required." >&2; \
	    exit 1; \
	  fi; \
	  "$(UV_INSTALL_DIR)/uv" --version; \
	fi

### Primary targets

setup:  #doc# Create/refresh .venv and install deps from pyproject
setup: bootstrap
	$(UV) sync --group dev

template:  #doc# Scaffold a project; usage: make template DEST=/path/to/project
template: bootstrap
	@if [ -z "$(DEST)" ]; then \
	  echo "DEST is required. Usage: make template DEST=/path/to/project" >&2; \
	  exit 2; \
	fi
	UV_PROJECT_ENVIRONMENT="$(PPF_ENVIRONMENT)" $(UV) run --project . --no-dev ppf $(PPF_ARGS) "$(DEST)"

format:  #doc# Apply Ruff lint fixes and format Python files
format: bootstrap
	$(UV) run ruff check --fix $(RUFF_ARGS)
	$(UV) run ruff format $(RUFF_ARGS)

fmt:  #doc# Alias for format
fmt: format

lint:  #doc# Run Ruff lint and formatting checks
lint: bootstrap
	$(UV) run ruff check $(RUFF_ARGS)
	$(UV) run ruff format --check $(RUFF_ARGS)

typecheck:  #doc# Run basedpyright static type checks
typecheck: bootstrap
	$(UV) run basedpyright

test:  #doc# Run the pytest test suite
test: bootstrap
	$(UV) run pytest $(PYTEST_ARGS)

test-cov:  #doc# Run tests with a terminal coverage report
test-cov: bootstrap
	$(UV) run pytest --cov=python_project_foundry --cov-report=term-missing $(PYTEST_ARGS)

check:  #doc# Run lint, type, and test checks
check: lint typecheck test docs

all:  #doc# Alias for check
all: check

### Documentation targets

docs:  #doc# Build the documentation site in strict mode
docs: bootstrap
	DISABLE_MKDOCS_2_WARNING=true NO_MKDOCS_2_WARNING=1 \
	  $(UV) run --group docs mkdocs build --strict $(MKDOCS_ARGS)

docs-linkcheck:  #doc# Build documentation and check its links
docs-linkcheck: docs
	@mkdir -p "$$(dirname "$(LINKCHECK_REPORT)")"
	$(UV) run --group docs linkchecker --no-status --no-warnings \
	  --ignore-url 'sitemap\.xml\.gz$$' -F xml/utf-8/"$(LINKCHECK_REPORT)" site/index.html

serve-docs:  #doc# Preview documentation with live reload
serve-docs: bootstrap
	DISABLE_MKDOCS_2_WARNING=true NO_MKDOCS_2_WARNING=1 \
	  $(UV) run --group docs mkdocs serve --strict $(MKDOCS_ARGS)

### Convenience targets

lock:  #doc# (Re)generate uv.lock without installing
lock: bootstrap
	$(UV) lock

update:  #doc# Update to latest compatible versions and resync
update: bootstrap
	$(UV) lock --upgrade
	$(UV) sync --group dev

precommit:  #doc# Run all pre-commit hooks against all files
precommit: bootstrap
	$(UV) run pre-commit run --all-files

build:  #doc# Build source and wheel distributions
build: bootstrap
	$(UV) run python -m build

clean:  #doc# Remove Python caches and build artifacts (keeps .venv)
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} + || true
	@find . -type d -name "*.egg-info" -prune -exec rm -rf {} + || true
	@rm -rf .basedpyright_cache .pytest_cache .ruff_cache build dist htmlcov .coverage || true
