# tests/test_post.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_post():
    response = client.post("/token/", data={"username": "user@example.com", "password": "password"})
    token = response.json()

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/posts/", json={"title": "Test Post", "content": "This is a test."}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"

def test_comments_analytics():
    response = client.get("/api/comments-daily-breakdown?date_from=2020-02-02&date_to=2022-02-15")
    assert response.status_code == 200
    data = response.json()
    assert "2020-02-02" in data
