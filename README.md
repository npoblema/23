# Habit Tracker

Habit Tracker — это REST API для управления привычками с интеграцией уведомлений через Telegram. Проект предназначен для отслеживания привычек, предоставления публичного списка и отправки напоминаний пользователям.

## Описание проекта

Habit Tracker предоставляет следующий функционал:
- Создание, редактирование и удаление привычек.
- Просмотр публичных привычек других пользователей.
- Отправка напоминаний через Telegram с помощью асинхронных задач.

Проект реализован с использованием:
- **Django** и **Django REST Framework** для API.
- **PostgreSQL** для хранения данных.
- **Celery** и **Redis** для асинхронной обработки задач.
- **Telegram Bot API** для уведомлений.
- **Swagger (drf-yasg)** для документации API.

Код протестирован с покрытием **97%**.

---

## Требования

- **Python**: 3.12
- **PostgreSQL**: 13 или выше
- **Redis**: 5 или выше
- **Docker** (опционально, для запуска Redis)
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))

---

## Установка

### 1. Клонирование репозитория
```bash
git clone <repository_url>
cd Course_work_Habit_Tracker
```

### 2. Настройка виртуального окружения
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка окружения
Создайте файл `.env` в корне проекта и добавьте:
```bash
DATABASE_URL=postgres://postgres:your_password@localhost:5432/habit_tracker
SECRET_KEY=your_django_secret_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```
- Замените `your_password`, `your_django_secret_key` и `your_telegram_bot_token` на свои значения.

### 5. Применение миграций
```bash
python habit_tracker/manage.py migrate
```

### 6. Запуск Redis
```bash
docker run -d -p 6379:6379 redis
```

### 7. Запуск сервера
```bash
python habit_tracker/manage.py runserver
```

### 8. Запуск Celery


```bash
celery -A habit_tracker worker -l info
```

---

## Использование

### Для пользователей
1. Зарегистрируйтесь через API: `POST /api/users/register/`.
2. Войдите в систему: `POST /api/users/login/`.
3. Используйте токен в заголовке `Authorization: Token <token>` для доступа к защищённым эндпоинтам.
4. Создавайте привычки и получайте напоминания в Telegram.

### API
- **Базовый URL**: `http://127.0.0.1:8000/api/`
- **Эндпоинты**:
  - `POST /api/users/register/` — регистрация пользователя.
  - `POST /api/users/login/` — авторизация и получение токена.
  - `GET /api/habits/` — список привычек текущего пользователя (требуется токен).
  - `POST /api/habits/` — создание привычки (требуется токен).
  - `GET /api/habits/public/` — список публичных привычек.
  - `PATCH /api/habits/<id>/` — обновление привычки (требуется токен).
  - `DELETE /api/habits/<id>/` — удаление привычки (требуется токен).

### Документация API
- **Swagger**: `http://127.0.0.1:8000/swagger/`

---

## Тестирование

Запустите тесты из директории `habit_tracker`:


```bash
cd habit_tracker
pytest -v --cov=habits --cov-report=html
```
- **Покрытие кода**: 97% (см. `htmlcov/index.html`).

Для тестирования приложения `users`:
```bash
pytest -v --cov=users --cov-report=html
```


---

## Структура проекта

- **`habit_tracker/`**: Основной каталог проекта.
- **`habits/`**: Приложение для работы с привычками (модели, сериализаторы, вьюхи, тесты).
- **`users/`**: Приложение для управления пользователями (регистрация, авторизация).
- **`requirements.txt`**: Список зависимостей.
- **`pytest.ini`**: Конфигурация тестов.

---

## Разработчикам

- Проект использует **Token Authentication** (DRF). Токен передаётся в заголовке: `Authorization: Token <token>`.
- Для настройки Telegram-бота замените `TELEGRAM_BOT_TOKEN` в `.env` на свой токен.
- Добавление новых эндпоинтов возможно через `habits/urls.py` или `users/urls.py`.

---

## Автор

- **Владимиров Александр**