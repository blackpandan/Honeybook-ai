import asyncio
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.schemas import HoneyBookEventPayload
from app.services import project_service, openai_service

router = APIRouter()


async def process_project_in_background(project_id: str, raw_data: dict):
    """Runs after the 200 is returned — calls OpenAI and saves results."""
    from app.core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        project = await project_service.get_project_by_id(db, project_id)
        if not project:
            return
        try:
            extracted = await openai_service.extract_fields(raw_data)
            result = await openai_service.generate_summary_and_followup(raw_data, extracted)
            await project_service.save_ai_results(
                db,
                project,
                extracted,
                summary=result.get("summary", ""),
                followup=result.get("followup", ""),
            )
        except Exception as e:
            await project_service.mark_error(db, project, str(e))


@router.post("", status_code=202)
async def receive_honeybook_event(
    payload: HoneyBookEventPayload,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Zapier hits this endpoint when a new HoneyBook project/inquiry arrives.
    We save immediately (202 Accepted) then process AI in the background.
    """
    project = await project_service.create_or_update_project(db, payload)

    background_tasks.add_task(
        process_project_in_background,
        project.id,
        payload.model_dump(),
    )

    return {
        "project_id": project.id,
        "status": "accepted",
        "message": "Processing started. Poll /hb-result for results.",
    }
