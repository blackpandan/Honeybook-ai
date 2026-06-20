"""
Run once to create all tables.
Usage: python scripts/init_db.py
"""
import asyncio
from app.core.database import engine, Base
import app.models.project  # noqa: F401 — ensures model is registered


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully.")


if __name__ == "__main__":
    asyncio.run(init())
