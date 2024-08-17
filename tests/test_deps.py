# tests/test_deps.py
import pytest
from fastapi import HTTPException
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import deps, auth, crud, schemas, models
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

def test_get_current_user(db):
    user_data = schemas.UserCreate(
        username="testuser", email="test@example.com", password="testpassword"
    )
    user = crud.create_user(db, user_data)
    token = auth.create_access_token(data={"sub": str(user.id)})
    retrieved_user = deps.get_current_user(token=token, db=db)
    assert retrieved_user.username == "testuser"

def test_get_current_user_invalid_token(db):
    invalid_token = "invalid.token.value"
    with pytest.raises(HTTPException) as exc_info:
        deps.get_current_user(token=invalid_token, db=db)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"

def test_get_current_user_invalid_user(db):
    token = auth.create_access_token(data={"sub": "9999"})  # Non-existent user ID
    with pytest.raises(HTTPException) as exc_info:
        deps.get_current_user(token=token, db=db)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"
