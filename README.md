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
* Планировщик задач django-celery-beat
* Swagger-документация API
* Покрытие тестами 99%

---

## Технологии

* Python 3.12
* Django 6
* Django REST Framework
* PostgreSQL
* Celery
* Redis
* django-celery-beat
* Simple JWT
* drf-yasg (Swagger)
* pytest
* pytest-django
* pytest-cov

---

## Установка проекта

### 1. Клонировать репозиторий

```bash
git clone <repository_url>
cd courses_habit_tracker
```

### 2. Установить зависимости

```bash
poetry install
```

### 3. Создать файл окружения

Создать файл `.env` по примеру:

```bash
cp .env.template .env
```

Заполнить необходимые переменные окружения.

---

## Переменные окружения

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=habit_tracker
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

TELEGRAM_BOT_TOKEN=your_bot_token
```

---

## Применение миграций

```bash
poetry run python manage.py migrate
```

---

## Создание суперпользователя

```bash
poetry run python manage.py createsuperuser
```

---

## Запуск проекта

```bash
poetry run python manage.py runserver
```

API будет доступно по адресу:

```
http://127.0.0.1:8000/
```

---

## Swagger

Документация доступна по адресу:

```
http://127.0.0.1:8000/swagger/
```

---

## Получение JWT-токена

Получение токена:

```
POST /api/token/
```

Обновление токена:

```
POST /api/token/refresh/
```

---

## Celery

Запуск worker:

```bash
poetry run celery -A config worker -l info
```

Запуск beat:

```bash
poetry run celery -A config beat -l info
```

Для работы Celery должен быть запущен Redis.

---

## Основные эндпоинты

### Пользователи

* `POST /api/users/register/` — регистрация
* `GET /api/users/profile/` — профиль пользователя
* `PATCH /api/users/profile/` — обновление профиля

### Авторизация

* `POST /api/token/`
* `POST /api/token/refresh/`

### Привычки

* `GET /api/habits/`
* `POST /api/habits/`
* `GET /api/habits/{id}/`
* `PATCH /api/habits/{id}/`
* `DELETE /api/habits/{id}/`

### Публичные привычки

* `GET /api/public/`

---

## Тестирование

Запуск тестов:

```bash
poetry run pytest
```

Запуск тестов с покрытием:

```bash
poetry run pytest --cov
```

Покрытие проекта — **99%**.

---

## Автор

Олеся Ласковец
