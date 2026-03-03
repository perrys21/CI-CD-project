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

## Manual inference pipeline (GitHub Actions)

1. Run the `CI` workflow on `main` so it publishes the `onnx-model` artifact.
2. In GitHub Actions, run `Manual Inference` via `Run workflow`.
3. Optionally provide `input_csv` (repo path). If empty, script uses sample Iris rows.
4. Download `inference-output` artifact from the workflow run.
