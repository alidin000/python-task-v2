# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app
from app import models, database
from sqlalchemy.orm import Session

client = TestClient(app)

# Dependency override for testing
def override_get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[database.get_db] = override_get_db

def test_register_user():
    response = client.post("/register/", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login_user():
    response = client.post("/token/", data={"username": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_post():
    # First, register and log in the user
    client.post("/register/", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    login_response = client.post("/token/", data={"username": "test@example.com", "password": "password"})
    token = login_response.json()["access_token"]

    # Now, create a post
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/posts/", json={"title": "Test Post", "content": "This is a test post."}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"

def test_create_comment():
    # Create a post first
    client.post("/register/", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    login_response = client.post("/token/", data={"username": "test@example.com", "password": "password"})
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    post_response = client.post("/posts/", json={"title": "Test Post", "content": "This is a test post."}, headers=headers)
    post_id = post_response.json()["id"]

    # Now, create a comment
    response = client.post(f"/posts/{post_id}/comments/", json={"content": "This is a test comment."}, headers=headers)
    assert response.status_code == 200
    assert response.json()["content"] == "This is a test comment."

def test_blocked_comment():
    # Create a post first
    client.post("/register/", json={"username": "testuser", "email": "test@example.com", "password": "password"})
    login_response = client.post("/token/", data={"username": "test@example.com", "password": "password"})
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    post_response = client.post("/posts/", json={"title": "Test Post", "content": "This is a test post."}, headers=headers)
    post_id = post_response.json()["id"]

    # Create a comment that should be blocked
    response = client.post(f"/posts/{post_id}/comments/", json={"content": "This comment contains bad language."}, headers=headers)
    assert response.status_code == 200
    assert response.json()["is_blocked"] is True

