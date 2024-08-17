import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, schemas, crud, database

# # Setup in-memory SQLite database for testing
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="function")
# def db():
#     models.Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         models.Base.metadata.drop_all(bind=engine)

def test_create_user(db):
    user = schemas.UserCreate(username="testuser", email="test@example.com", password="testpassword")
    db_user = crud.create_user(db, user)
    assert db_user.username == "testuser"
    assert db_user.email == "test@example.com"
    assert db_user.hashed_password != "testpassword"  # Ensure password is hashed

def test_get_user(db):
    user = schemas.UserCreate(username="testuser", email="test@example.com", password="testpassword")
    db_user = crud.create_user(db, user)
    fetched_user = crud.get_user(db, user_id=db_user.id)
    assert fetched_user.id == db_user.id

def test_get_user_by_email(db):
    user = schemas.UserCreate(username="testuser", email="test@example.com", password="testpassword")
    db_user = crud.create_user(db, user)
    fetched_user = crud.get_user_by_email(db, email="test@example.com")
    assert fetched_user.email == db_user.email

def test_create_post(db):
    user = schemas.UserCreate(username="testuser", email="test@example.com", password="testpassword")
    db_user = crud.create_user(db, user)
    post = schemas.PostCreate(title="Test Post", content="This is a test post")
    db_post = crud.create_post(db, post, user_id=db_user.id)
    assert db_post.title == "Test Post"
    assert db_post.owner_id == db_user.id

def test_create_comment(db):
    user = schemas.UserCreate(username="testuser", email="test@example.com", password="testpassword")
    db_user = crud.create_user(db, user)
    post = schemas.PostCreate(title="Test Post", content="This is a test post")
    db_post = crud.create_post(db, post, user_id=db_user.id)
    comment = schemas.CommentCreate(content="This is a test comment")
    db_comment = crud.create_comment(db, comment, post_id=db_post.id, is_blocked=False)
    assert db_comment.content == "This is a test comment"
    assert db_comment.post_id == db_post.id
    assert db_comment.is_blocked == False
