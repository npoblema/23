# Habit Tracker

Habit Tracker — это REST API для управления привычками с интеграцией уведомлений через Telegram. Проект разработан для отслеживания привычек пользователей, предоставления публичного списка привычек и отправки напоминаний.

## Описание

Habit Tracker позволяет пользователям:
- Создавать, редактировать и удалять свои привычки.
- Просматривать список публичных привычек.
- Получать напоминания о привычках через Telegram.

Проект построен на основе Django и Django REST Framework, использует PostgreSQL для хранения данных, Celery и Redis для асинхронной обработки задач, а также Telegram Bot API для уведомлений. API документировано с помощью Swagger (`drf-yasg`), а код протестирован с покрытием 97%.

## Требования

- Python 3.12
- PostgreSQL 13+
- Redis 5+



1. Настройка виртуального окружения
```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    # source .venv/bin/activate  # Linux/Mac
   ```
2. Установка зависимостей 
```bash
pip install -r requirements.txt
```
3. Настройка окружения

Создайте файл .env в корне проекта:
```bash
DATABASE_URL=postgres://postgres:your_password@localhost:5432/habit_tracker
SECRET_KEY=your_django_secret_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
````
4. Применение миграций
```bash
python habit_tracker/manage.py migrate
```
5. Запуск Redis
```bash
docker run -d -p 6379:6379 redis
```
6. Запуск сервера
```bash
python habit_tracker/manage.py runserver
```
7. Запуск Celery
```bash
celery -A habit_tracker worker -l info
```

# Использование
### API
* Базовый URL: http://127.0.0.1:8000/api/
* Эндпоинты:
    * GET /api/habits/ — список привычек текущего пользователя (требуется аутентификация).
    * POST /api/habits/ — создание привычки.
    * GET /api/habits/public/ — список публичных привычек.
    * PATCH /api/habits/<id>/ — обновление привычки.
    * DELETE /api/habits/<id>/ — удаление привычки.
### Документация API
* Swagger: http://127.0.0.1:8000/swagger/

# Тестирование
```bash
cd habit_tracker
pytest -v --cov=habits --cov-report=html
```
* Покрытие кода: 97% (см. htmlcov/index.html).

# Структура проекта
* habit_tracker/: Основной каталог проекта.
* habits/: Приложение с моделями, сериализаторами, вьюхами и тестами.
* requirements.txt: Зависимости.
* pytest.ini: Настройки тестов.

## Автор
* Владимиров Александр