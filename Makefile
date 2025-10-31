PROJNAME=glinkfix

ifeq (${MAKECMDGOALS},coverage)
	WEBPATH=htmlcov/index.html
endif

# --------------------------------------------

define BROWSER_PYSCRIPT
import webbrowser
from pathlib import Path
p = Path('.').resolve()/'${WEBPATH}'
webbrowser.open(f'file://{p}', new=2)
endef

export BROWSER_PYSCRIPT
BROWSER?=python3 -c "$$BROWSER_PYSCRIPT"

# --------------------------------------------

all: help

# --------------------------------------------

.PHONY: setup
setup: ## initialize the project and python venv
ifeq (,$(wildcard .init/setup))
	@(which uv > /dev/null 2>&1) || \
	(echo "glinkfix requires uv. See README for instructions."; exit 1)
	mkdir -p scratch .init run
	touch .init/setup
	cp ./scripts/* ./run
	find ./run -name '*.sh' -exec chmod 744 {} \;
	uv sync --frozen --no-dev
else
	@echo "Initial setup is already complete. If you are having issues, run:"
	@echo
	@echo "make reset"
	@echo "make setup"
	@echo
endif

# --------------------------------------------

.PHONY: dev
dev: ## add development dependencies (run make setup first)
ifeq (,$(wildcard .init/setup))
	@echo "Please run \"make setup\" first" ; exit 1
endif
	uv sync --all-groups --frozen
	@touch .init/dev

# --------------------------------------------

.PHONY: upgrade
upgrade: ## synchronize helper scripts and upgrade project dependencies
ifeq (,$(wildcard .init/setup))
	@echo "Please run \"make setup\" first" ; exit 1
endif
	cp -f ./scripts/* ./run
	find ./run -name '*.sh' -exec chmod 744 {} \;
ifeq (,$(wildcard .init/dev))
	uv sync --upgrade --no-dev
else
	uv sync --upgrade --all-groups
endif

# --------------------------------------------

.PHONY: sync
sync: ## sync dependencies with the lock file (use --frozen)
ifeq (,$(wildcard .init/setup))
	@echo "Please run \"make setup\" first" ; exit 1
endif

ifneq (,$(wildcard .init/dev))
	uv sync --all-groups
else
	uv sync --no-dev
endif

# --------------------------------------------

.PHONY: clean
clean: ## Purge project build artifacts
	@echo Cleaning project build artifacts
	@rm -rf build/
	@rm -rf dist/
	@find . -type d -name __pycache__ -exec rm -rf {} \; -prune
	@find . -type d -name .ipynb_checkpoints -exec rm -rf {} \; -prune
	@find . -type d -name .pytest_cache -exec rm -rf {} \; -prune
	@find . -type d -name .eggs -exec rm -rf {} \; -prune
	@find . -type d -name htmlcov -exec rm -rf {} \; -prune
	@find . -type d -name *.egg-info -exec rm -rf {} \; -prune
	@find . -type f -name *.egg -delete
	@find . -type f -name *.pyc -delete
	@find . -type f -name *.pyo -delete
	@find . -type f -name *.coverage -delete

# --------------------------------------------

.PHONY: reset
reset: clean ## reinitialize the project
	@echo Resetting project state
	rm -rf .init .mypy_cache .ruff_cache .venv run

# --------------------------------------------

.PHONY: tags
tags: ## Update project tags
	./run/release_tags.sh

# --------------------------------------------

.PHONY: rebase
rebase: ## re-baseline with the main branch
	./run/rebaseline.sh

# --------------------------------------------

.PHONY: coverage
coverage: ## Generate an html code coverage report
	coverage run -m pytest 
	coverage report -m
	coverage html
	${BROWSER}

# --------------------------------------------

.PHONY: test
test: ## Run pytest with --tb=short option
	pytest --tb=short

# --------------------------------------------

.PHONY: build
build: ## build package for publishing
	rm -rf dist
	uv build

# --------------------------------------------

.PHONY: publish-production
publish-production: build ## publish package to pypi.org for production
	@set -a; eval "$$(grep '^PYPI_' $$HOME/.secrets)"; \
	uv publish --publish-url https://upload.pypi.org/legacy/ \
		--token "$$PYPI_PROD"

# --------------------------------------------

.PHONY: publish-test
publish-test: build ## publish package to test.pypi.org for testing
	@set -a; eval "$$(grep '^PYPI_' $$HOME/.secrets)"; \
	uv publish  --publish-url https://test.pypi.org/legacy/ \
		--token "$$PYPI_TEST"

# --------------------------------------------

.PHONY: help
help: ## show help
	@echo ""
	@echo "Available Commands"
	@echo "========================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk \
	'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
