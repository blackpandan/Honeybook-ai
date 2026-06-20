from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import events, results, settings
from app.core.config import settings as cfg

app = FastAPI(
    title="HoneyBook AI Backend",
    description="Processes HoneyBook events via Zapier, enriches with OpenAI, returns structured results.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cfg.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router, prefix="/hb-event", tags=["Events"])
app.include_router(results.router, prefix="/hb-result", tags=["Results"])
app.include_router(settings.router, prefix="/settings", tags=["Settings"])


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
