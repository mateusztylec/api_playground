from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.config import settings
from typing import List, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.oatch2 import create_access_token
from app.database import get_db
from app.database import Base
from app import models
from alembic import command

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # sesja do database


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(
        bind=engine)  # creating all database, cos jak alembic ale nie aktualizuje db gdy coś w niej zmienisz
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # # run our code before we return our test
    # command.upgrade("head")
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)  # generuje po prostu obiekt taki sam jak w bibliotece response
    # command.downgrade("base")
    # Base.metadata.drop_all(bind=engine)
    # run out code after our test finished


@pytest.fixture
def test_user(client):
    user_data = {"email": "mati@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{"title": "first title",
                   "content": "first content",
                   "owner_id": test_user['id']
                   }, {
                      "title": "2nd title",
                      "content": "2nd content",
                      "owner_id": test_user['id']
                  }, {
                      "title": "3rd title",
                      "content": "3rd content",
                      "owner_id": test_user['id']
                  }, {
                      "title": "4th title",
                      "content": "4th content",
                      "owner_id": test_user2['id']
                  }]

    def create_post_model(post: dict):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts

@pytest.fixture
def test_user2(client):
    user_data = {"email": "mati123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user