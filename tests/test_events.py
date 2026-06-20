"""
Run: pytest tests/ -v
Requires no real DB — uses SQLite in-memory via override.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_post_event_returns_202(monkeypatch):
    """Smoke test: Zapier payload accepted, project_id returned."""
    # Skip actual DB + AI by overriding services
    from app.routers import events
    import uuid

    async def fake_create(db, payload):
        class FakeProject:
            id = str(uuid.uuid4())
        return FakeProject()

    monkeypatch.setattr("app.routers.events.project_service.create_or_update_project", fake_create)
    monkeypatch.setattr("app.routers.events.process_project_in_background", lambda *a, **k: None)

    payload = {
        "client_id": "hb_001",
        "name": "Test Client",
        "email": "test@example.com",
        "budget": "5000",
        "event_date": "2026-08-01",
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/hb-event", json=payload)

    assert r.status_code == 202
    assert "project_id" in r.json()
