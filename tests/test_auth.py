# tests/test_auth.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import auth, crud, schemas, models
from app.database import Base

# # Setup in-memory SQLite database for testing
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="function")
# def db():
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         Base.metadata.drop_all(bind=engine)

def test_create_access_token():
    data = {"sub": "testuser"}
    token = auth.create_access_token(data=data)
    assert isinstance(token, str)

def test_authenticate_user(db):
    user_data = schemas.UserCreate(
        username="testuser", email="test@example.com", password="testpassword"
    )
    user = crud.create_user(db, user_data)
    authenticated_user = auth.authenticate_user(
        db, username="testuser", password="testpassword"
    )
    assert authenticated_user
    assert authenticated_user.username == "testuser"

def test_authenticate_user_invalid_password(db):
    user_data = schemas.UserCreate(
        username="testuser", email="test@example.com", password="testpassword"
    )
    user = crud.create_user(db, user_data)
    authenticated_user = auth.authenticate_user(
        db, username="testuser", password="wrongpassword"
    )
    assert authenticated_user is False

def test_authenticate_user_invalid_username(db):
    authenticated_user = auth.authenticate_user(
        db, username="invaliduser", password="testpassword"
    )
    assert authenticated_user is False
