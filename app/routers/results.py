from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.schemas import ProjectResult, ExtractedFields
from app.services.project_service import get_project_by_id

router = APIRouter()


@router.get("", response_model=ProjectResult)
async def get_result(
    project_id: str = Query(..., description="The project ID returned by /hb-event"),
    db: AsyncSession = Depends(get_db),
):
    """
    Zapier polls this after sending an event.
    Returns AI-generated summary, follow-up message, and extracted fields.
    Status will be 'pending' until AI finishes (usually < 10s).
    """
    project = await get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found.")

    extracted = None
    if project.extracted:
        extracted = ExtractedFields(**project.extracted)

    return ProjectResult(
        project_id=project.id,
        status=project.status,
        summary=project.summary,
        followup=project.followup,
        fields=extracted,
        updated_at=project.updated_at,
    )
