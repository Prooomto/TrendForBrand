# TrendForBrand Backend

Backend для платформы TrendForBrand, построенный на FastAPI.

## Установка и запуск

```bash
# Установка зависимостей
poetry install

# Запуск в режиме разработки
poetry run uvicorn main:app --reload
```

## Структура проекта

- `app/` - основной код приложения
- `tests/` - тесты
- `main.py` - точка входа FastAPI
- `pyproject.toml` - конфигурация Poetry
- `.env` - переменные окружения
