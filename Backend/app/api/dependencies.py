# app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.use_cases.get_current_user import GetCurrentUserUseCase

# Token URL теперь ожидает `username` в теле запроса
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user_id = int(payload.get("sub"))
    user_repository = UserRepository()
    use_case = GetCurrentUserUseCase(user_repository)
    try:
        user = use_case.execute(user_id)
        return user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден.",
            headers={"WWW-Authenticate": "Bearer"},
        )
