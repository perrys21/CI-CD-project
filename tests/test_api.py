from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "ci-cd-api"
    assert "timestamp_utc" in payload


def test_add() -> None:
    response = client.post("/add", json={"a": 2, "b": 3.5})
    assert response.status_code == 200
    assert response.json() == {
        "operation": "addition",
        "inputs": {"a": 2.0, "b": 3.5},
        "result": 5.5,
    }


def test_items() -> None:
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {
        "count": 3,
        "items": [
            {"id": "item-1", "name": "apple", "in_stock": True},
            {"id": "item-2", "name": "banana", "in_stock": True},
            {"id": "item-3", "name": "carrot", "in_stock": False},
        ],
    }
