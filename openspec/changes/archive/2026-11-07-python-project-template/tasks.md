# Tasks

[[_TOC_]]

## 1. Скелет шаблона

- [x] 1.1 [Infra] Создать `copier.yml` с параметрами `project_name` (валидация kebab-case) и `python_version` (с дефолтом), `_subdirectory: template`. Критерий приёмки: `copier copy . scratch/ --defaults` запускается без ошибок валидации
- [x] 1.2 [Infra] Создать корневой `Makefile` шаблона с целями `help`, `codegen` (генерация в `scratch/` с `--defaults`), `lock` (пересборка `uv.lock`), `clean`. Критерий приёмки: `make help` и `make codegen` выполняются
- [x] 1.3 [Infra] Создать корневой `.gitignore` (scratch/, .venv/, __pycache__, кэши). Критерий приёмки: `git status` не показывает `scratch/` и `.venv/`
- [x] 1.4 [Docs] Написать README шаблона с командой генерации и требованиями (copier, uv, docker). Критерий приёмки: команда из README выполняется как написано

## 2. Каркас приложения

- [x] 2.1 [Backend] Создать `template/pyproject.toml.jinja`: имя проекта `{{app_name}}`, `requires-python >= {{python_version}}`, fastapi/uvicorn/pydantic/pydantic-settings/structlog/opentelemetry-зависимости, dev-группа (pytest, pytest-asyncio, pytest-cov, pytest-mock, httpx, ruff, mypy), конфиги ruff (line-length 119) и mypy (strict). Критерий приёмки: `uv lock` без ошибок
- [x] 2.2 [Backend] Реализовать `template/src/settings.py.jinja`: `AppSettings` (pydantic-settings, `.env`, `app_name` с дефолтом `{{app_name}}`, `app_env=local`, `app_debug=false`, `log_level` регистронезависимый enum, вложенный `OtelSettings`), `get_settings()` с lru_cache. Критерий приёмки: тесты из группы 3 проходят
- [x] 2.3 [Backend] Реализовать `template/src/log.py`: `initialize_logging(settings)` — structlog поверх stdlib, ConsoleRenderer при `app_debug=true`, JSONRenderer иначе. Критерий приёмки: `make run` с `APP_DEBUG=true` даёт цветной вывод, без — JSON
- [x] 2.4 [Backend] Реализовать `template/src/telemetry.py`: `initialize_telemetry(settings)` — выход при `OTEL_SDK_DISABLED=true`, иначе `setdefault` для `OTEL_RESOURCE_ATTRIBUTES` и OTLP-gRPC экспорт трейсов. Критерий приёмки: сервер стартует без коллектора и без OTEL-переменных
- [x] 2.5 [Backend] Реализовать `template/src/api/app.py` (фабрика `create_app`: telemetry → FastAPI с title из настроек → `app.state.settings` → health-роутер → `FastAPIInstrumentor`), `api/routers/health.py` (`GET /health` → `{"status": "ok"}`), `main.py` как точку входа uvicorn. Критерий приёмки: `uvicorn main:app` отвечает 200 на `/health`
- [x] 2.6 [Backend] Добавить служебные файлы проекта: `.python-version`, `.gitignore`, `.dockerignore`, `.env.example` (с `OTEL_SDK_DISABLED=true` и закомментированным `OTEL_EXPORTER_OTLP_ENDPOINT`), `entrypoint.sh` (uvicorn :8000, +x). Критерий приёмки: все файлы присутствуют в проекте после `make codegen`

## 3. Тесты и качество кода

- [x] 3.1 [Backend] Создать `template/tests/conftest.py` (`OTEL_SDK_DISABLED=true` до импорта приложения, фикстуры `app`/`test_client`/`test_client_raise_exceptions`) и тесты: health возвращает 200/`{"status": "ok"}`, настройки читаются из env, наследование `AppSettings` добавляет поле. Критерий приёмки: `make test` — все тесты зелёные
- [x] 3.2 [Backend] Создать `template/Makefile` проекта с целями `help`, `lint` (ruff + mypy), `fmt`, `test`, `run`. Критерий приёмки: `make lint` в сгенерированном проекте — без ошибок
- [x] 3.3 [Backend] Добавить тест формата логирования: при `app_debug=false` событие уходит в JSON (захват stdout), при `true` — человекочитаемый вывод. Критерий приёмки: тест проходит

## 4. Контейнер и dev-окружение

- [x] 4.1 [Infra] Создать `template/Dockerfile.jinja`: multi-stage (`dev` — все группы + make/git, `builder` — `uv sync --no-dev --frozen`, `release` — non-root `app`, `.venv` + `src` + entrypoint, EXPOSE 8000). Критерий приёмки: `docker build --target release` успешен, контейнер отвечает на `/health`
- [x] 4.2 [Infra] Создать `template/compose.yml.jinja`: build target `dev`, `env_file: .env`, проброс :8000, команда uvicorn. Критерий приёмки: `docker compose up` + `curl localhost:8000/health` → 200
- [x] 4.3 [Infra] Создать `template/.devcontainer/devcontainer.json.jinja` (build dev, volume для `.venv`, bind исходников, порт 8000, расширения python/debugpy/pylance/ruff) и `.vscode/` (`launch.json` — uvicorn+debug и pytest-debug, `settings.json` — pytest). Критерий приёмки: «Reopen in Container» в VS Code, запуск сервера и тестов из панели Debug
- [x] 4.4 [Docs] Создать `template/README.md.jinja` с Quick Start (зависимости: Docker+uv, devcontainer, make-команды, переменные окружения). Критерий приёмки: команды из README выполняются в сгенерированном проекте как написано

## 5. CI и сквозная проверка

- [x] 5.1 [Infra] Создать `.github/workflows/ci.yml` шаблона: на push/PR `uv sync` + `make lint` + `make test`. Критерий приёмки: workflow синтаксически валиден (actionlint или прогон)
- [x] 5.2 [Infra] Сквозная проверка: `make codegen` → в `scratch/my-app/` выполняются `make lint`, `make test`, `docker build --target release`. Критерий приёмки: все три команды успешны
- [x] 5.3 [Infra] Проверить идемпотентность генерации: два прогона `copier copy` с одинаковыми ответами дают `diff -r` без различий, `.copier-answers.yml` присутствует. Критерий приёмки: diff пуст

## Workflow follow-up

- После ревью артефактов и реализации — архивация change через `/skill:openspec-archive-change`.
