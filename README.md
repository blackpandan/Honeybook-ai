# HoneyBook AI Backend

FastAPI backend that receives HoneyBook events from Zapier, enriches them with OpenAI, and returns structured results back to Zapier.

## Architecture

```
HoneyBook → Zapier → POST /hb-event → (background) OpenAI → DB
                                                               ↓
HoneyBook ← Zapier ←  GET /hb-result ←────────────────────────
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/hb-event` | Zapier sends HoneyBook data here |
| GET | `/hb-result?project_id=...` | Zapier polls for AI results |
| POST | `/settings` | Update runtime config |
| GET | `/health` | Health check |

## Quick Start

### 1. Clone and install
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set up environment
```bash
cp .env.example .env
# Fill in OPENAI_API_KEY and DATABASE_URL
```

### 3. Start Postgres (Docker)
```bash
docker-compose up -d
```

### 4. Initialize DB
```bash
python scripts/init_db.py
```

### 5. Run the server
```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Test locally
```bash
curl -X POST http://localhost:8000/hb-event \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Smith","email":"jane@example.com","budget":"8000","event_date":"2026-10-15"}'
```

## Deploying to AWS

When ready to deploy on AWS Lambda or ECS:

1. Set environment variables via AWS Secrets Manager or Parameter Store
2. Update `DATABASE_URL` to point to RDS instance
3. Change Zapier webhook URL from `localhost` → your AWS endpoint

**Only one thing changes in Zapier:** the URL.

## Project Structure

```
app/
  main.py              # FastAPI app + middleware
  core/
    config.py          # Pydantic settings (reads .env)
    database.py        # Async SQLAlchemy engine + session
  models/
    project.py         # DB model (one table: projects)
    schemas.py         # Pydantic request/response schemas
  routers/
    events.py          # POST /hb-event
    results.py         # GET /hb-result
    settings.py        # POST/GET /settings
  services/
    openai_service.py  # All OpenAI calls
    project_service.py # All DB read/write
scripts/
  init_db.py           # One-time table creation
tests/
  test_events.py       # Smoke tests
```
