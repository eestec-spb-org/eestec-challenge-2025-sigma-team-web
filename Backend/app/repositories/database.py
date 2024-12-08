# app/repositories/database.py
from peewee import SqliteDatabase

from app.core.config import settings

# Убедимся, что директория для базы данных существует
database_dir = settings.DATABASE_PATH.parent
database_dir.mkdir(parents=True, exist_ok=True)

# Инициализируем базу данных с корректным путем
db = SqliteDatabase(str(settings.DATABASE_PATH))
