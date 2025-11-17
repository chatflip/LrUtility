.PHONY: help format lint test builddocs cleandocs

.DEFAULT_GOAL := help

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  install - Install dependencies"
	@echo "  format - Run formatting checks and fixes"
	@echo "  lint - Run linting checks"
	@echo "  test - Run tests"

install:
	uv sync --all-groups

format:
	uv run ruff check --fix
	uv run ruff format

lint:
	uv run ruff check
	uv run ty check

test:
	uv run pytest tests/ --cov=./ --cov-report=xml
