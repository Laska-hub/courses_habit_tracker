# Habit Tracker API

REST API для трекера полезных привычек, разработанный на Django REST Framework.

Проект позволяет пользователям создавать привычки, получать напоминания через Telegram и управлять личными и публичными привычками.

## Возможности

* Регистрация пользователей
* JWT-аутентификация
* Просмотр и редактирование собственного профиля
* CRUD для привычек
* Просмотр списка публичных привычек
* Валидация привычек согласно требованиям проекта
* Telegram-уведомления
* Celery + Redis для фоновых задач
* Планировщик задач `django-celery-beat`
* Swagger-документация API
* Автоматическое тестирование и линтинг
* Контейнеризация проекта с помощью Docker
* Запуск всех сервисов через Docker Compose
* Автоматический деплой на удалённый сервер через GitHub Actions

---

## Технологии

* Python 3.12
* Django 6
* Django REST Framework
* PostgreSQL 16
* Celery
* Redis 7
* django-celery-beat
* Simple JWT
* drf-yasg (Swagger)
* pytest
* pytest-django
* pytest-cov
* Docker
* Docker Compose
* Nginx
* GitHub Actions
* Yandex Cloud

---

# Локальная установка

## 1. Клонировать репозиторий

```bash
git clone https://github.com/Laska-hub/courses_habit_tracker.git
cd courses_habit_tracker
```

## 2. Установить зависимости

Для запуска проекта без Docker используется Poetry:

```bash
poetry install
```

## 3. Создать файл окружения

Создать `.env` на основе `.env.template`:

```bash
cp .env.template .env
```

Заполнить необходимые переменные окружения.

> Файл `.env` содержит секретные данные и не должен добавляться в Git.

---

## Переменные окружения

Пример основных переменных:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=habit_tracker
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379

CELERY_BROKER_URL=redis://localhost:6379/0

TELEGRAM_BOT_TOKEN=your_bot_token

ALLOWED_HOSTS=localhost,127.0.0.1
```

---

# Запуск проекта без Docker

## 1. Применить миграции

```bash
poetry run python manage.py migrate
```

## 2. Создать суперпользователя

```bash
poetry run python manage.py createsuperuser
```

## 3. Запустить Django

```bash
poetry run python manage.py runserver
```

API будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

---

# Docker

Проект полностью контейнеризирован и может быть запущен одной командой.

## Сервисы Docker Compose

В проекте используются следующие сервисы:

| Сервис        | Назначение                      |
| ------------- | ------------------------------- |
| `web`         | Django-приложение и Gunicorn    |
| `db`          | PostgreSQL                      |
| `redis`       | Redis                           |
| `celery`      | Celery worker                   |
| `celery-beat` | Планировщик периодических задач |
| `nginx`       | Веб-сервер и reverse proxy      |

PostgreSQL и Redis запускаются как отдельные контейнеры. Django, Celery и Celery Beat используют общий Docker-образ приложения.

## Запуск всех сервисов

Убедитесь, что установлен Docker Desktop, затем выполните:

```bash
docker compose up -d --build
```

После запуска проверить состояние контейнеров:

```bash
docker compose ps
```

Просмотреть логи:

```bash
docker compose logs -f
```

Остановить проект:

```bash
docker compose down
```

После запуска приложение доступно через Nginx:

```text
http://localhost/
```

Swagger:

```text
http://localhost/swagger/
```

---

# Архитектура Docker Compose

Схема взаимодействия сервисов:

```text
                    ┌─────────────┐
                    │    Nginx    │
                    │     :80     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Django   │
                    │  Gunicorn   │
                    │    :8000    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │PostgreSQL│ │  Redis   │ │  Celery  │
        │   :5432  │ │   :6379  │ │  worker  │
        └──────────┘ └────┬─────┘ └─────┬────┘
                          │              │
                          │       ┌──────▼──────┐
                          │       │ Celery Beat │
                          │       │  scheduler  │
                          │       └─────────────┘
                          │
                          └── Celery broker
```

---

# Swagger

Документация API доступна по адресу:

```text
http://localhost/swagger/
```

---

# Получение JWT-токена

Получение токена:

```text
POST /api/token/
```

Обновление токена:

```text
POST /api/token/refresh/
```

---

# Celery

Для локального запуска без Docker необходимо предварительно запустить Redis.

Celery worker:

```bash
poetry run celery -A config worker -l info
```

Celery Beat:

```bash
poetry run celery -A config beat -l info
```

При использовании Docker Compose Redis, Celery worker и Celery Beat запускаются автоматически.

---

# Основные эндпоинты

## Пользователи

* `POST /api/users/register/` — регистрация
* `GET /api/users/profile/` — профиль пользователя
* `PATCH /api/users/profile/` — обновление профиля

## Авторизация

* `POST /api/token/` — получение JWT-токена
* `POST /api/token/refresh/` — обновление JWT-токена

## Привычки

* `GET /api/habits/`
* `POST /api/habits/`
* `GET /api/habits/{id}/`
* `PATCH /api/habits/{id}/`
* `DELETE /api/habits/{id}/`

## Публичные привычки

* `GET /api/public/`

---

# Тестирование

Запуск тестов:

```bash
poetry run pytest
```

Запуск тестов с покрытием:

```bash
poetry run pytest --cov
```

Перед деплоем тесты автоматически запускаются в GitHub Actions.

---

# CI/CD

Для проекта настроен GitHub Actions workflow:

```text
.github/workflows/deploy.yml
```

Pipeline выполняет следующие этапы:

```text
Lint
  ↓
Tests
  ↓
Docker Build
  ↓
Deploy
```

При создании или обновлении Pull Request в `develop` выполняются проверки:

* Lint
* Tests
* Docker Build

При успешном `push` в ветку `develop` после прохождения всех проверок дополнительно выполняется автоматический Deploy.

## Lint

Проверяются:

* `flake8`
* `isort`
* `black`

## Tests

Запускаются автоматические тесты проекта с использованием PostgreSQL и Redis.

## Docker Build

Проверяется возможность сборки Docker-образов проекта:

```bash
docker compose build
```

## Automatic Deploy

После успешного прохождения всех предыдущих этапов и `push` в ветку `develop` GitHub Actions автоматически подключается к удалённому серверу по SSH и выполняет деплой.

На сервере выполняются:

```bash
git fetch origin
git checkout develop
git pull origin develop
docker compose down
docker compose up -d --build
```

Файл `.env` с секретными переменными хранится непосредственно на сервере и не передаётся в репозиторий.

---

# Настройка удалённого сервера

Для деплоя используется виртуальная машина Yandex Cloud.

На сервере установлены:

* Docker
* Docker Compose
* Git

Также настроен SSH-доступ для автоматического деплоя.

В GitHub Repository → **Settings → Secrets and variables → Actions** используются следующие секреты:

```text
SSH_HOST
SSH_USER
SSH_PRIVATE_KEY
```

Где:

* `SSH_HOST` — публичный IP-адрес сервера;
* `SSH_USER` — пользователь сервера;
* `SSH_PRIVATE_KEY` — приватный SSH-ключ для подключения.

На сервере создаётся файл:

```text
~/.env
```

с переменными окружения проекта.

Файл `.env` не хранится в Git и не добавляется в репозиторий.

---

# Запуск проекта на сервере

После успешного деплоя GitHub Actions автоматически запускает Docker Compose.

Проверить состояние контейнеров на сервере:

```bash
docker compose ps
```

Проверить запущенные контейнеры:

```bash
docker ps
```

Посмотреть логи:

```bash
docker compose logs -f
```

После успешного деплоя приложение доступно по адресу:

```text
http://51.250.18.142/
```

Swagger:

```text
http://51.250.18.142/swagger/
```

---

# Остановка проекта на сервере

Для остановки контейнеров:

```bash
docker compose down
```

Для повторного запуска:

```bash
docker compose up -d --build
```

---

# Структура проекта

```text
courses_habit_tracker/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── config/
├── habits/
├── users/
├── telegram_bot/
├── nginx/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.template
├── manage.py
├── pyproject.toml
├── poetry.lock
├── pytest.ini
└── README.md
```

---

## Автор

Олеся Ласковец
