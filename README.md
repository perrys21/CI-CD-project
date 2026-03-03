# CI-CD API Project

## Run locally (Python)

```bash
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run tests

```bash
pytest
```

## Lint and format

```bash
ruff check .
black --check .
```

## Run with Docker Compose

```bash
docker compose up --build
```

API URL: http://localhost:8000
Docs: http://localhost:8000/docs
