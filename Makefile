.DEFAULT_GOAL := help

.PHONY: help codegen clean

APP_NAME := my-app
BUILD_DIR := .build/template

help: ## Показать доступные команды
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'

codegen: ## Сгенерировать тестовый проект в scratch/
	mkdir -p $(BUILD_DIR)
	rsync -a --delete --exclude='.git' --exclude='.build' --exclude='scratch' --exclude='openspec' --exclude='__pycache__' --exclude='*.pyc' ./ $(BUILD_DIR)/
	copier copy --trust $(BUILD_DIR) scratch/$(APP_NAME) --defaults --data app_name=$(APP_NAME)

clean: ## Удалить сгенерированный проект и сборочный каталог
	rm -rf scratch $(BUILD_DIR)
