SHELL := /bin/bash


.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: install
install: ## Make venv and install requirements
	@mkdir -p .venv
	@poetry install
	@poetry run pre-commit install
	@pre-commit autoupdate

.PHONY: update
update: ## Update requirements
	@poetry update
	@poetry run pre-commit autoupdate


.PHONY: run
run: ## Run the basic command
	@poetry run weeknote -config config_example.json


.PHONY: run_error
run_error: ## Run the basic command with an error in the config
	@poetry run weeknote -config dev_config/1201/config_example_error.json
	@rm -rf dev_config

.PHONY: clean
clean: ## Clean the project of the test stuff
	@rm -rf dev_config || true
	@rm -rf weeknotes || true
	@rm -rf dist || true
