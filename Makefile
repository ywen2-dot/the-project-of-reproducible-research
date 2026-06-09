.PHONY: help install lint format run report docs docker-build docker-push clean

DATA   ?= data/netflix_titles.csv
OUTPUT ?= output/figures
DOCKER_USER ?= yuhan023
IMAGE  = $(DOCKER_USER)/netflix-analysis

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Install the package and dev dependencies
	pip install -e ".[dev]"
	pre-commit install

lint: ## Run ruff linter
	ruff check netflix_analysis/ main.py

format: ## Auto-format code with ruff
	ruff format netflix_analysis/ main.py

run: ## Run the full analysis pipeline
	python main.py --data $(DATA) --output $(OUTPUT)

report: ## Run the analysis and render the Quarto HTML report
	python main.py --data $(DATA) --output $(OUTPUT)
	PYTHONPATH="$(CURDIR)" quarto render report/report.qmd --to html --execute-dir "$(CURDIR)"

docs: ## Build Sphinx HTML documentation
	sphinx-apidoc -o docs/source netflix_analysis
	sphinx-build -b html docs/source docs/_build/html

docker-build: ## Build the Docker image
	docker build -t $(IMAGE):latest .

docker-push: ## Push the Docker image to DockerHub
	docker push $(IMAGE):latest

clean: ## Remove generated outputs and cache files
	rm -rf output/ docs/_build/ __pycache__ .pytest_cache report/report.html
	find . -type d -name "__pycache__" -exec rm -rf {} +
