# app/api/v1/users.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from app.api.dependencies import get_current_user
from app.domain.entities import User

router = APIRouter()


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


@router.get("/me", response_model=UserResponse, summary="Получить текущего пользователя")
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(id=current_user.id, username=current_user.username, email=current_user.email)
