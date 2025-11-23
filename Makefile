.PHONY: help build up down restart logs shell-app shell-db shell-redis clean lint format

help: ## Показать помощь
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Собрать Docker образы
	docker-compose build

up: ## Запустить все сервисы
	docker-compose up -d

down: ## Остановить все сервисы
	docker-compose down

restart: ## Перезапустить все сервисы
	docker-compose restart

logs-all: ## Показать логи всех сервисов
	docker-compose logs -f

shell-app: ## Открыть shell в контейнере приложения
	docker-compose exec app /bin/bash

shell-db: ## Открыть psql в PostgreSQL
	docker-compose exec postgres psql -U ledger_user -d mini_ledger

shell-redis: ## Открыть redis-cli
	docker-compose exec redis redis-cli

clean: ## Остановить и удалить все контейнеры и volumes
	docker-compose down -v
	docker system prune -f

rebuild: ## Пересобрать и запустить
	docker-compose up -d --build

status: ## Показать статус контейнеров
	docker-compose ps

lint: ## Проверить код с помощью ruff
	ruff check .

lint-fix: ## Проверить и автоисправить код
	ruff check . --fix

format: ## Форматировать код с помощью ruff
	@ruff check --select F401 --fix $(git diff --name-only --diff-filter=d $(git merge-base HEAD "origin/master") | grep -E "\.py$") 2>/dev/null || true
	@ruff format $(git diff --name-only --diff-filter=d $(git merge-base HEAD "origin/master") | grep -E "\.py$")
	@ruff check --select I --fix $(git diff --name-only --diff-filter=d $(git merge-base HEAD "origin/master") | grep -E "\.py$") 2>/dev/null || true
	@ruff check --select E301,E302,E303,E305 --fix $(git diff --name-only --diff-filter=d $(git merge-base HEAD "origin/master") | grep -E "\.py$") 2>/dev/null || true



check: lint ## Полная проверка кода
	@echo "Проверка завершена"

