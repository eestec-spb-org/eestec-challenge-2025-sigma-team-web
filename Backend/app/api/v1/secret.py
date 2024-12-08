# app/api/v1/secret.py
from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.repositories.user_repository import UserRepository
from app.use_cases.access_secret import AccessSecretUseCase

router = APIRouter()


@router.get("/secret", summary="Доступ к секретным данным")
def get_secret(current_user=Depends(get_current_user)):
    user_repository = UserRepository()
    use_case = AccessSecretUseCase(user_repository)
    secret_data = use_case.execute(current_user.id)
    return {"secret_data": secret_data}
