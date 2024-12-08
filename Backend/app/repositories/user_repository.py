# app/repositories/user_repository.py
from typing import List, Optional

from peewee import IntegrityError

from app.domain.entities import User
from app.domain.models import UserModel
from app.domain.repositories import UserRepositoryInterface
from app.repositories.database import db


class UserRepository(UserRepositoryInterface):
    def __init__(self):
        if db.is_closed():
            db.connect()
        db.create_tables([UserModel], safe=True)

    def create_user(self, username: str, email: str, hashed_password: str) -> Optional[User]:
        try:
            user = UserModel.create(username=username, email=email, hashed_password=hashed_password)
            return User(id=user.id, username=user.username, email=user.email, hashed_password=user.hashed_password)
        except IntegrityError as e:
            print(f"Ошибка при создании пользователя: {e}")
            raise ValueError("Пользователь с таким email или username уже существует.")

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            user = UserModel.get(UserModel.id == user_id)
            return User(id=user.id, username=user.username, email=user.email, hashed_password=user.hashed_password)
        except UserModel.DoesNotExist:
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            user = UserModel.get(UserModel.email == email)
            return User(id=user.id, username=user.username, email=user.email, hashed_password=user.hashed_password)
        except UserModel.DoesNotExist:
            return None

    def get_all_users(self) -> List[User]:
        users = UserModel.select()
        return [User(id=user.id, username=user.username, email=user.email, hashed_password=user.hashed_password) for
                user in users]

    def update_user(self, user_id: int, username: Optional[str] = None, email: Optional[str] = None,
                    hashed_password: Optional[str] = None) -> Optional[User]:
        fields = {}
        if username is not None:
            fields['username'] = username
        if email is not None:
            fields['email'] = email
        if hashed_password is not None:
            fields['hashed_password'] = hashed_password

        if not fields:
            return self.get_user_by_id(user_id)

        try:
            query = UserModel.update(**fields).where(UserModel.id == user_id)
            rows_updated = query.execute()
            if rows_updated:
                return self.get_user_by_id(user_id)
            return None
        except IntegrityError as e:
            print(f"Ошибка при обновлении пользователя с ID '{user_id}': {e}")
            raise ValueError("Невозможно обновить пользователя. Возможно, email или username уже используются.")

    def delete_user(self, user_id: int) -> bool:
        rows_deleted = UserModel.delete().where(UserModel.id == user_id).execute()
        return rows_deleted > 0

    def __del__(self):
        if not db.is_closed():
            db.close()
