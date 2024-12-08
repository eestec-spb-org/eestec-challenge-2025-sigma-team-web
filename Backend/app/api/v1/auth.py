# app/api/v1/auth.py
from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel, EmailStr

from app.repositories.user_repository import UserRepository
from app.use_cases.login_user import LoginUserUseCase
from app.use_cases.register_user import RegisterUserUseCase

router = APIRouter()


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    username: str  # Используем `username`, но это будет email
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", status_code=201, summary="Регистрация нового пользователя")
def register_user(request: RegisterRequest):
    user_repository = UserRepository()
    use_case = RegisterUserUseCase(user_repository)
    try:
        user = use_case.execute(request.username, request.email, request.password)
        return {"message": "Пользователь зарегистрирован успешно"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", summary="Авторизация пользователя")
def login_user(
        username: str = Form(...),  # Используем Form вместо Pydantic модели
        password: str = Form(...)
):
    user_repository = UserRepository()
    use_case = LoginUserUseCase(user_repository)
    try:
        # Интерпретируем `username` как email
        access_token = use_case.execute(email=username, password=password)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
