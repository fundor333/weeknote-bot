SHELL := /bin/bash

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
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: install
install: ## Make venv and install requirements
	@mkdir -p .venv
	@uv sync
	@uv run pre-commit install
	@pre-commit autoupdate

.PHONY: update
update: ## Update requirements
	@uv lock --upgrade
	@uv sync
	@uv run pre-commit autoupdate


.PHONY: run
run: ## Run the basic command
	@uv run weeknote -config config_example.json


.PHONY: run_error
run_error: ## Run the basic command with an error in the config
	@uv run weeknote -config dev_config/1201/config_example_error.json
	@rm -rf dev_config

.PHONY: clean
clean: ## Clean the project of the test stuff
	@rm -rf dev_config || true
	@rm -rf weeknotes || true
	@rm -rf dist || true
