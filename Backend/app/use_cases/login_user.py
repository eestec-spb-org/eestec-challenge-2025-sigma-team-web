# app/use_cases/login_user.py
from fastapi import HTTPException, status

from app.core.security import verify_password, create_access_token
from app.domain.repositories import UserRepositoryInterface


class LoginUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> str:
        user = self.user_repository.get_user_by_email(email)  # Проверяем как email
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": str(user.id)})
        return access_token
