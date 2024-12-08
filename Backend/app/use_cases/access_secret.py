# app/use_cases/access_secret.py
from app.domain.repositories import UserRepositoryInterface


class AccessSecretUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> str:
        return "This is top secret information!"
