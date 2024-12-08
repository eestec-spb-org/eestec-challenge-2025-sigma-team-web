# app/repositories/migrations.py
from app.domain.models import UserModel
from app.repositories.database import db


def migrate():
    with db:
        db.create_tables([UserModel], safe=True)
