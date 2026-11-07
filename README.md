# Python Project Template

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)

Шаблон для быстрого старта новых Python-сервисов: FastAPI-приложение с health-проверкой, конфигурация из окружения, структурное логирование, опциональная телеметрия, тесты, ruff/mypy, Dockerfile и devcontainer. Генерация — через [Copier](https://copier.readthedocs.io/).

## Требования

- [uv](https://docs.astral.sh/uv/)
- [copier](https://copier.readthedocs.io/) — `uv tool install copier`
- Docker — для сборки образа и compose (опционально)
- VS Code + Dev Containers — для разработки в контейнере (опционально)

## Генерация проекта

```sh
copier copy <путь-или-url-этого-репозитория> my-app
```

Команда спросит имя приложения (`my-app`, kebab-case) и версию Python, после чего создаст проект в каталоге `my-app`. Имя используется единообразно: каталог проекта, Docker-образ, сервис по умолчанию. Ответы сохраняются в `.copier-answers.yml` внутри проекта — при выходе новых версий шаблона проект обновляется через `copier update`.

## Разработка шаблона

```sh
make codegen   # сгенерировать тестовый проект в scratch/my-app
make clean     # удалить scratch/
```

После генерации `uv.lock` создаётся автоматически (задача `uv lock` в `copier.yml`).

См. [CONTRIBUTING](CONTRIBUTING.md).
