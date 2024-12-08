# app/main.py
from fastapi import FastAPI

from app.api.v1 import auth, users, secret
from app.repositories.migrations import migrate

app = FastAPI(
    title="Account Management Service",
    description="Сервис для управления аккаунтами пользователей.",
    version="1.0.0",
)

# Выполняем миграции при запуске
migrate()

# Включаем маршруты
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(secret.router, prefix="/api", tags=["Secret"])
