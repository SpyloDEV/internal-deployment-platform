from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.incident import (
    IncidentCreate,
    IncidentRead,
    IncidentTimelineCreate,
    IncidentTimelineRead,
    IncidentUpdate,
)
from app.services.incident_service import IncidentService

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post("", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
async def create_incident(
    payload: IncidentCreate, current_user: CurrentUser, session: DbSession
) -> IncidentRead:
    incident = await IncidentService(session).create(
        user_id=current_user.id, data=payload.model_dump()
    )
    await session.commit()
    await session.refresh(incident)
    return incident


@router.get("", response_model=list[IncidentRead])
async def list_incidents(
    current_user: CurrentUser,
    session: DbSession,
    organization_id: str | None = Query(default=None),
) -> list[IncidentRead]:
    return await IncidentService(session).list(
        user_id=current_user.id, organization_id=organization_id
    )


@router.get("/{incident_id}", response_model=IncidentRead)
async def get_incident(
    incident_id: str, current_user: CurrentUser, session: DbSession
) -> IncidentRead:
    return await IncidentService(session).get(
        incident_id=incident_id, user_id=current_user.id
    )


@router.patch("/{incident_id}", response_model=IncidentRead)
async def update_incident(
    incident_id: str,
    payload: IncidentUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> IncidentRead:
    incident = await IncidentService(session).update(
        incident_id=incident_id,
        user_id=current_user.id,
        data=payload.model_dump(exclude_unset=True),
    )
    await session.commit()
    await session.refresh(incident)
    return incident


@router.post(
    "/{incident_id}/timeline",
    response_model=IncidentTimelineRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_incident_timeline(
    incident_id: str,
    payload: IncidentTimelineCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> IncidentTimelineRead:
    entry = await IncidentService(session).add_timeline(
        incident_id=incident_id, user_id=current_user.id, message=payload.message
    )
    await session.commit()
    await session.refresh(entry)
    return entry
