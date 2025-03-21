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
	@poetry run python manage.py collectstatic --noinput


.PHONY: run
run: ## Run the basic command
	@poetry run weeknote -config config_example.json
