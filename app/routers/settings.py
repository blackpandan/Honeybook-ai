from fastapi import APIRouter
from app.models.schemas import SettingsUpdate

router = APIRouter()

# In-memory for now; swap for DB-backed settings when needed
_runtime_settings: dict = {}


@router.post("")
async def update_settings(payload: SettingsUpdate):
    """
    Allows updating runtime settings without redeploying.
    Useful for swapping prompts or OpenAI models per client.
    """
    if payload.openai_model:
        _runtime_settings["openai_model"] = payload.openai_model
    if payload.custom_prompt:
        _runtime_settings["custom_prompt"] = payload.custom_prompt

    return {"status": "updated", "current_settings": _runtime_settings}


@router.get("")
async def get_settings():
    return {"current_settings": _runtime_settings}
