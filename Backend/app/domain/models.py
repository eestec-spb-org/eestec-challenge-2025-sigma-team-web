# app/domain/models.py
from peewee import Model, CharField

from app.repositories.database import db


class BaseModel(Model):
    class Meta:
        database = db


class UserModel(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    hashed_password = CharField()
