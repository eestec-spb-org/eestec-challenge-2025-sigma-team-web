# app/use_cases/get_current_user.py
from app.domain.entities import User
from app.domain.repositories import UserRepositoryInterface


class GetCurrentUserUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> User:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден.")
        return user
