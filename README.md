# Система отслеживания привычек
Система отслеживания привычек — это REST API для управления повседневными привычками с функцией уведомлений через Telegram. Проект разработан для создания, изменения и удаления привычек, просмотра публичных привычек других пользователей и отправки напоминаний с использованием асинхронных задач.

## Общая информация о проекте

Проект предоставляет следующие возможности:

- Формирование, редактирование и удаление записей о привычках.
- Доступ к списку публичных привычек.
- Автоматическая отправка уведомлений через Telegram с использованием асинхронной обработки.

Для реализации используются:

- Django и Django REST Framework для построения API.
- PostgreSQL как база данных.
- Celery и Redis для выполнения асинхронных задач.
- Telegram Bot API для отправки уведомлений.
- drf-yasg для создания документации API (Swagger).
- Код протестирован с покрытием **97%**.

---

## Требования

- Python: версия 3.12.
- PostgreSQL: версия 13 или выше.
- Redis: версия 5 или выше.
- Docker (рекомендуется для запуска Redis).
- Токен Telegram-бота, полученный через ([@BotFather](https://t.me/BotFather))

---

## Инструкция по установке

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

## Использование системы

### Для пользователей
1. Создайте учётную запись через API: POST /api/users/register/.
2. Авторизуйтесь для получения токена: POST /api/users/login/.
3. Используйте заголовок Authorization: Token <token> для доступа к защищённым эндпоинтам.
4. Управляйте привычками и получайте напоминания через Telegram.

### Эндпоинты API
- **Базовый URL**: `http://127.0.0.1:8000/api/`
- **Основные маршруты**:
- POST /api/users/register/ — регистрация нового пользователя.
- POST /api/users/login/ — авторизация и получение токена.
- GET /api/habits/ — просмотр привычек авторизованного пользователя.
- POST /api/habits/ — добавление новой привычки.
- GET /api/habits/public/ — список общедоступных привычек.
- PATCH /api/habits/<id>/ — частичное обновление привычки.
- DELETE /api/habits/<id>/ — удаление привычки.

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

## Организация проекта

- **`habit_tracker/`**: Основная директория проекта.
- **`habits/`**: Модуль для управления привычками (модели, сериализаторы, представления, тесты).
- **`users/`**: Модуль для работы с пользователями (регистрация, авторизация).
- **`requirements.txt`**: Перечень зависимостей.
- **`pytest.ini`**: Настройки для тестирования.

---

## Для разработчиков

- Аутентификация реализована через Token Authentication (DRF). Токен передаётся в заголовке: `Authorization: Token <token>`.
- Для настройки Telegram-бота замените `TELEGRAM_BOT_TOKEN` в `.env` на свой токен.
- Добавление новых эндпоинтов возможно через `habits/urls.py` или `users/urls.py`.

---

## Автор проекта

- **Григорьев Кирилл**
