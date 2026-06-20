import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project
from app.models.schemas import HoneyBookEventPayload, ExtractedFields


async def create_or_update_project(db: AsyncSession, payload: HoneyBookEventPayload) -> Project:
    """Upsert a project record from Zapier payload."""
    project_id = payload.project_id or str(uuid.uuid4())

    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    raw_data = payload.model_dump()

    if project:
        project.raw = raw_data
        project.client_id = payload.client_id
        project.status = "pending"
        project.error_message = None
    else:
        project = Project(
            id=project_id,
            client_id=payload.client_id,
            raw=raw_data,
            status="pending",
        )
        db.add(project)

    await db.commit()
    await db.refresh(project)
    return project


async def save_ai_results(
    db: AsyncSession,
    project: Project,
    extracted: ExtractedFields,
    summary: str,
    followup: str,
) -> Project:
    """Persist AI results back to the project row."""
    project.extracted = extracted.model_dump()
    project.summary = summary
    project.followup = followup
    project.status = "processed"
    await db.commit()
    await db.refresh(project)
    return project


async def mark_error(db: AsyncSession, project: Project, error: str) -> Project:
    project.status = "error"
    project.error_message = error
    await db.commit()
    await db.refresh(project)
    return project


async def get_project_by_id(db: AsyncSession, project_id: str) -> Project | None:
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()
