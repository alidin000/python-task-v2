import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def create_test_user(client):
    def _create_test_user(username, email, password="password"):
        response = client.post("/register/", json={"username": username, "email": email, "password": password})
        return response.json()
    return _create_test_user

@pytest.fixture
def get_auth_token(client, create_test_user):
    def _get_auth_token(username, password="password"):
        create_test_user(username=username, email=f"{username}@example.com")
        response = client.post("/login/", json={"username": username, "password": password})
        return response.json()["access_token"]
    return _get_auth_token

def test_register(client):
    response = client.post("/register/", json={"username": "testuser", "email": "testuser@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"

def test_login(client, create_test_user):
    create_test_user(username="testuser", email="testuser@example.com")
    response = client.post("/login/", json={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_post(client, get_auth_token):
    token = get_auth_token("postuser")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/posts/", json={"title": "Test Post", "content": "This is a test post"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"

def test_create_comment(client, get_auth_token):
    token = get_auth_token("commentuser")
    headers = {"Authorization": f"Bearer {token}"}
    post_response = client.post("/posts/", json={"title": "Test Post", "content": "This is a test post"}, headers=headers)
    post_id = post_response.json()["id"]
    comment_response = client.post(f"/posts/{post_id}/comments/", json={"content": "This is a test comment"}, headers=headers)
    assert comment_response.status_code == 200
    assert comment_response.json()["content"] == "This is a test comment"

def test_comments_daily_breakdown(client, get_auth_token):
    token = get_auth_token("analyticsuser")
    headers = {"Authorization": f"Bearer {token}"}
    
    post_response = client.post("/posts/", json={"title": "Analytics Post", "content": "This is an analytics post"}, headers=headers)
    post_id = post_response.json()["id"]

    client.post(f"/posts/{post_id}/comments/", json={"content": "Comment 1"}, headers=headers)
    client.post(f"/posts/{post_id}/comments/", json={"content": "Comment 2"}, headers=headers)

    created_comments_response = client.get(f"/posts/{post_id}/comments/", headers=headers)

    response = client.get("/api/comments-daily-breakdown?date_from=2023-01-01&date_to=2023-12-31", headers=headers)
    print("Analytics response:", response.json())  # Debugging line

    assert response.status_code == 200
    assert len(response.json()) > 0




def test_auto_response(client, get_auth_token):
    token = get_auth_token("autoresponseuser")
    headers = {"Authorization": f"Bearer {token}"}
    
    post_response = client.post("/posts/", json={"title": "Auto Response Post", "content": "This is an auto response post"}, headers=headers)
    post_id = post_response.json()["id"]
    
    auto_response_settings = {
        "enabled": True,
        "response_delay": 5,
        "response_template": "Thank you for your comment!"
    }
    
    response = client.post(f"/posts/{post_id}/auto-response/", json=auto_response_settings, headers=headers)
    print("Auto-response settings response:", response.json())  # Debugging line
    
    assert response.status_code == 200


