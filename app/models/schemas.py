from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any, Dict
from datetime import datetime


# ── Inbound from Zapier ──────────────────────────────────────────────────────

class HoneyBookEventPayload(BaseModel):
    """Exact shape Zapier sends to POST /hb-event"""
    client_id: Optional[str] = None
    project_id: Optional[str] = None          # used as DB primary key; auto-generated if missing
    name: Optional[str] = None
    email: Optional[str] = None
    budget: Optional[int] = None
    event_date: Optional[str] = None
    raw: Optional[Dict[str, Any]] = Field(default_factory=dict)


# ── AI-extracted fields ───────────────────────────────────────────────────────

class ExtractedFields(BaseModel):
    client_name: Optional[str] = None
    budget: Optional[str] = None
    event_date: Optional[str] = None
    missing_tasks: Optional[list[str]] = []
    followup_status: Optional[str] = None     # e.g. "needs_quote", "awaiting_contract"


# ── Outbound to Zapier ────────────────────────────────────────────────────────

class ProjectResult(BaseModel):
    """Shape returned by GET /hb-result"""
    project_id: str
    status: str
    summary: Optional[str] = None
    followup: Optional[str] = None
    fields: Optional[ExtractedFields] = None
    updated_at: Optional[datetime] = None


# ── Settings ─────────────────────────────────────────────────────────────────

class SettingsUpdate(BaseModel):
    openai_model: Optional[str] = None
    custom_prompt: Optional[str] = None
