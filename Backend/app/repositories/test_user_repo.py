import pytest

from app.repositories.database import db
from app.repositories.migrations import UserModel
from app.repositories.user_repository import UserRepository
from app.repositories.utils import hash_password, verify_password


@pytest.mark.parametrize("real_password, entered_password", [
    ('securepassword', 'securepassword'),
    ('securepassword', 'other_password'),
    ('126549', '126549'),
    ('securepassword', '126549')
])
def test_hashing(real_password, entered_password):
    if real_password == entered_password:
        assert verify_password(entered_password, hash_password(real_password))
    else:
        assert not (verify_password(entered_password, hash_password(real_password)))


@pytest.fixture(scope='function')
def setup_db():
    # Подключаемся к базе данных
    db.connect()
    db.create_tables([UserModel])  # Создаём таблицу User для каждого теста

    user_repository = UserRepository()

    yield user_repository
    db.drop_tables([UserModel])
    db.close()


def test_create_user(setup_db):
    user_repository = setup_db
    user = user_repository.create_user("testuser", "user@example.com", hash_password("securepassword"))
    # Проверяем, что пользователь был успешно создан
    assert user.username == "testuser"
    assert user.email == "user@example.com"
    assert verify_password('securepassword', user.hashed_password)

    # Проверка на попытку создать пользователя с существующим email
    with pytest.raises(ValueError):
        user_repository.create_user("testuser2", "user@example.com", hash_password("otherpassword"))

    # Проверка на попытку создать пользователя с существующим username
    with pytest.raises(ValueError):
        user_repository.create_user("testuser", "other@example.com", hash_password("securepassword"))


def test_get_user_by_email(setup_db):
    user_repository = setup_db
    user_repository.create_user("testuser", "user@example.com", hash_password("securepassword"))

    # Проверяем, что можем получить пользователя по email
    user = user_repository.get_user_by_email("user@example.com")
    assert user.username == "testuser"
    assert user.email == "user@example.com"
    assert verify_password('securepassword', user.hashed_password)


def test_get_user_by_id(setup_db):
    user_repository = setup_db
    user_repository.create_user("testuser", "user@example.com", hash_password("securepassword"))

    # Проверяем, что можем получить пользователя по ID
    user = user_repository.get_user_by_id(1)
    assert user.username == "testuser"
    assert user.email == "user@example.com"
    assert verify_password('securepassword', user.hashed_password)


def test_get_all_users(setup_db):
    user_repository = setup_db
    user_repository.create_user("testuser", "user@example.com", hash_password("securepassword"))
    user_repository.create_user("testuser2", "next@example.com", hash_password("othersecurepassword"))

    users = user_repository.get_all_users()
    assert len(users) == 2
    assert users[0].username == "testuser"
    assert users[0].email == "user@example.com"
    assert verify_password('securepassword', users[0].hashed_password)
    assert users[1].username == "testuser2"
    assert users[1].email == "next@example.com"
    assert verify_password('othersecurepassword', users[1].hashed_password)


def test_update_user(setup_db):
    user_repository = setup_db
    user_repository.create_user("testuser1", "user1@example.com", hash_password("securepassword"))
    user_repository.create_user("testuser2", "user2@example.com", hash_password("securepassword"))
    user_repository.update_user(1, username="updateduser1", email="updated1@example.com")
    user_repository.update_user(2, hashed_password=hash_password("otherpassword"))
    user1 = user_repository.get_user_by_id(1)
    user2 = user_repository.get_user_by_id(2)
    assert user1.username == "updateduser1"
    assert user1.email == "updated1@example.com"
    assert verify_password('securepassword', user1.hashed_password)
    assert user2.username == "testuser2"
    assert user2.email == "user2@example.com"
    assert verify_password('otherpassword', user2.hashed_password)

    # Проверка на попытку обновить пользователя с существующим email
    with pytest.raises(ValueError):
        user_repository.update_user(1, email="user2@example.com")


def test_delete_user(setup_db):
    user_repository = setup_db
    user_repository.create_user("testuser", "user@example.com", hash_password("securepassword"))
    user_repository.create_user("testuser2", "next@example.com", hash_password("othersecurepassword"))
    user_repository.delete_user(1)

    assert user_repository.get_user_by_id(1) is None

    users = user_repository.get_all_users()
    assert len(users) == 1
    assert users[0].username == "testuser2"
    assert users[0].email == "next@example.com"
