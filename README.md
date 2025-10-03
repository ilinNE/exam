### Описание

Небольшое Django-приложение `birthdays` показывает ближайший день рождения сотрудника и транслирует обновления по WebSocket (Django Channels). В составе проектной конфигурации присутствуют PostgreSQL, Redis, Nginx и Docker Compose.

### Стек
- Django 4.2
- Channels 4 + Daphne
- PostgreSQL, Redis
- Nginx
- Docker / Docker Compose

### Локальный запуск (без Docker)
1. Создать и активировать виртуальное окружение.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Поднять Redis локально (например, через Docker):
```bash
docker run --rm -p 6379:6379 redis:7-alpine
```
3. Настроить переменные окружения (необязательно). Можно создать файл `.env` в корне:
```bash
SECRET_KEY=django-insecure-default-key
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```
4. Выполнить миграции и собрать статику:
```bash
cd proj
python manage.py migrate
python manage.py collectstatic --noinput
```
5. Запустить дев-сервер:
```bash
python manage.py runserver
```
6. Открыть приложение: `http://127.0.0.1:8000/`

### Запуск через Docker Compose
1. Создать файл `.env` в корне (минимально):
```bash
SECRET_KEY=django-insecure-default-key
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=django_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
```
2. Собрать и запустить:
```bash
docker compose up --build
```
3. Открыть: `http://localhost/`

### Полезные команды
- Создать суперпользователя:
```bash
cd proj
python manage.py createsuperuser
```
- Применить миграции:
```bash
python manage.py migrate
```
- Собрать статику:
```bash
python manage.py collectstatic --noinput
```

### Структура проекта (основное)
- `proj/birthdays/` — приложение (модели, вьюхи, утилиты, WebSocket-консумер)
- `proj/proj/settings.py` — конфигурация Django/Channels
- `docker-compose.yaml`, `Dockerfile`, `nginx.conf` — инфраструктура
- `requirements.txt` — зависимости
- `staticfiles/`, `media/` — статика и медиа (игнорируются в гите)

### Примечания
- По умолчанию проект настроен на PostgreSQL; для локального теста можно переключиться на SQLite, изменив `DATABASES` в `proj/proj/settings.py`.
- Для корректной работы WebSocket используется Redis (настройки `CHANNEL_LAYERS`).
