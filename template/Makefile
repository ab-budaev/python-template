.DEFAULT_GOAL := help

.PHONY: help mypy ruff fmt lint test run

help: ## Показать доступные команды
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'

mypy: ## Проверить типы
	uv run mypy .

ruff: ## Запустить ruff-линтер
	uv run ruff check .

lint: ## Запустить линтер и проверку типов
	$(MAKE) ruff
	$(MAKE) mypy

fmt: ## Автоформатировать код
	uv run ruff format .

test: ## Запустить тесты
	uv run pytest tests/

run: ## Запустить сервер локально (с автоперезагрузкой)
	PYTHONPATH=src uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
