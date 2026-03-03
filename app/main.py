from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CI-CD API")


class AddRequest(BaseModel):
    a: float
    b: float


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ci-cd-api",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/add")
def add(payload: AddRequest) -> dict[str, float | str | dict[str, float]]:
    result = payload.a + payload.b
    return {
        "operation": "addition",
        "inputs": {"a": payload.a, "b": payload.b},
        "result": result,
    }


@app.get("/items")
def items() -> dict[str, int | list[dict[str, str | bool]]]:
    data = [
        {"id": "item-1", "name": "apple", "in_stock": True},
        {"id": "item-2", "name": "banana", "in_stock": True},
        {"id": "item-3", "name": "carrot", "in_stock": False},
    ]
    return {"count": len(data), "items": data}
