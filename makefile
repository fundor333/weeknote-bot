SHELL := /bin/bash

RUNNER := uv run --env-file=.env

publish: build ## Publish to pypi
	@echo "🚀 Publishing project"
	@$(eval user := $(shell sed -ne 's/username *= *//p' $(HOME)/.pypirc))
	@$(eval pass := $(shell sed -ne 's/password *= *//p' $(HOME)/.pypirc))
	uv publish -u $(user) -p $(pass)

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uv build

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@$(RUNNER) python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: install
install: ## Make venv and install requirements
	@mkdir -p .venv
	@uv sync
	@$(RUNNER) pre-commit install
	@pre-commit autoupdate

.PHONY: update
update: ## Update requirements
	@uv lock --upgrade
	@uv sync --upgrade
	@$(RUNNER) pre-commit autoupdate


.PHONY: run
run: ## Run the basic command
	@$(RUNNER) weeknote -config config_example.json


.PHONY: run_error
run_error: ## Run the basic command with an error in the config
	@$(RUNNER) weeknote -config dev_config/1201/config_example_error.json
	@rm -rf dev_config

.PHONY: clean
clean: ## Clean the project of the test stuff
	@rm -rf dev_config || true
	@rm -rf weeknotes || true
	@rm -rf dist || true

patch: ## Increment patch
	@uv version --bump patch


minor: ## Increment minor
	@uv version --bump minor

major: ## Increment major
	@uv version --bump major

alpha: ## Increment alpha
	@uv version --bump alpha

beta: ## Increment beta
	@uv version --bump beta

stable: ## Increment stable
	@uv version --bump stable

dev: ## Increment dev
	@uv version --bump dev

.PHONY: deploy
deploy: update  ## Deploy for production
	@uv build
	@uv publish


precommit: ## Run pre-commit hooks
	@git add . & uv run pre-commit run --all-files
