PROJNAME=glinkfix
VENV=venv/${PROJNAME}
VER=patch
DRY=y

ifeq (${DRY},n)
	BUMPCMD?=bump2version ${VER}
else
	BUMPCMD?=bump2version ${VER} --dry-run --verbose
endif

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
setup: ## initialize the project and create python venv
ifeq (,$(wildcard .init/setup))
	@(which pip3 > /dev/null 2>&1) || \
	(echo "pip3 missing, run: sudo apt install pip3"; exit 1)
	@(python3 -m venv -h > /dev/null 2>&1) || \
	(echo "python3-venv missing, run: sudo apt install python3-venv"; exit 1)
	mkdir venv
	mkdir .init
	touch .init/setup
	python3 -m venv ${VENV}
	. ${VENV}/bin/activate; \
	pip3 install pip -U; \
	pip3 install -r requirements.txt -U
else
	@echo "Initial setup is already complete. If you are having issues, run:"
	@echo
	@echo "make reset"
	@echo "make setup"
	@echo
endif

# --------------------------------------------

# Manually activate the python virtual enviornment just to ensure that no pip
# packages are unintentionally installed if the user hasn't already activated
# the venv.
.PHONY: update
update: .init/setup ## update pip packages in venv
	. ${VENV}/bin/activate; \
	pip3 install pip -U; \
	pip3 install -r requirements.txt -U

# --------------------------------------------

.PHONY: reset
reset: clean ## reinitialize the project
	rm -rf venv .init

# --------------------------------------------

.PHONY: clean
clean: ## Purge project build artifacts
	@echo Cleaning project build artifacts
# @find . -type d -name .mypy_cache -exec rm -rf {} \; -prune
	@rm -rf build/
	@rm -rf dist/
	@find . -type d -name __pycache__ -exec rm -rf {} \; -prune
	@find . -type d -name .pytest_cache -exec rm -rf {} \; -prune
	@find . -type d -name .eggs -exec rm -rf {} \; -prune
	@find . -type d -name htmlcov -exec rm -rf {} \; -prune
	@find . -type d -name *.egg-info -exec rm -rf {} \; -prune
	@find . -type f -name *.egg -delete
	@find . -type f -name *.pyc -delete
	@find . -type f -name *.pyo -delete
	@find . -type f -name *.coverage -delete

# --------------------------------------------

.PHONY: coverage
coverage: ## Generate an html code coverage report
	coverage run -m pytest
	coverage report -m
	coverage html
	${BROWSER}

# --------------------------------------------

.PHONY: dist
dist: clean ## Build (but don't upload) distribution products
	python3 -m build
	twine check dist/*

# --------------------------------------------

.PHONY: test
test: ## Run pytest with --tb=short option
	pytest --tb=short

# --------------------------------------------

.PHONY: uptest
uptest: dist ## Upload a build to test.pypi.org
	twine upload dist/* --repository ${PROJNAME}-test

# --------------------------------------------

.PHONY: bump
bump: ## Bump version. VER=major|minor|patch, DRY=y|n
	${BUMPCMD}

# --------------------------------------------

.PHONY: release
release: dist ## Upload release version to pypi
	twine upload dist/* --repository ${PROJNAME}-release


# --------------------------------------------
.PHONY: help
help: ## Show help
	@echo Please specify a target. Choices are:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk \
	'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
