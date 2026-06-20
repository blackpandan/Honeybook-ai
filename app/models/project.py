from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)           # HoneyBook project ID
    client_id = Column(String, index=True, nullable=True)
    raw = Column(JSONB, nullable=False)                          # Full Zapier payload
    extracted = Column(JSONB, nullable=True)                     # AI-extracted fields
    summary = Column(Text, nullable=True)                        # AI summary
    followup = Column(Text, nullable=True)                       # AI follow-up message
    status = Column(String, default="pending")                   # pending | processed | error
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
