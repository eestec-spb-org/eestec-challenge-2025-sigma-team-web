# app/use_cases/register_user.py
from app.core.security import hash_password
from app.domain.entities import User
from app.domain.repositories import UserRepositoryInterface


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, username: str, email: str, password: str) -> User:
        hashed = hash_password(password)
        user = self.user_repository.create_user(username, email, hashed)
        return user
