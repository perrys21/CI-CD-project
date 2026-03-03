from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CI-CD API")


class AddRequest(BaseModel):
    a: float
    b: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/add")
def add(payload: AddRequest) -> dict[str, float]:
    return {"result": payload.a + payload.b}


@app.get("/items")
def items() -> dict[str, list[str]]:
    return {"items": ["apple", "banana", "carrot"]}
