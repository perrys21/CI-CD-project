from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add() -> None:
    response = client.post("/add", json={"a": 2, "b": 3.5})
    assert response.status_code == 200
    assert response.json() == {"result": 5.5}


def test_items() -> None:
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"items": ["apple", "banana", "carrot"]}
