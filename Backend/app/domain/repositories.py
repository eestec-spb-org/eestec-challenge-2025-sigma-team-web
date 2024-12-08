# app/domain/repositories.py
from typing import List, Optional

from app.domain.entities import User


class UserRepositoryInterface:
    def create_user(self, username: str, email: str, hashed_password: str) -> User:
        raise NotImplementedError

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    def get_user_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    def get_all_users(self) -> List[User]:
        raise NotImplementedError

    def update_user(self, user_id: int, username: Optional[str] = None, email: Optional[str] = None,
                    hashed_password: Optional[str] = None) -> Optional[User]:
        raise NotImplementedError

    def delete_user(self, user_id: int) -> bool:
        raise NotImplementedError
