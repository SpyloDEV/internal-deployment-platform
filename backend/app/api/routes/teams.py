from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.organization import TeamCreate, TeamRead, TeamUpdate
from app.services.team_service import TeamService

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(
    payload: TeamCreate, current_user: CurrentUser, session: DbSession
) -> TeamRead:
    team = await TeamService(session).create(
        user_id=current_user.id, data=payload.model_dump()
    )
    await session.commit()
    await session.refresh(team)
    return team


@router.get("", response_model=list[TeamRead])
async def list_teams(
    current_user: CurrentUser,
    session: DbSession,
    organization_id: str = Query(...),
) -> list[TeamRead]:
    return await TeamService(session).list(
        user_id=current_user.id, organization_id=organization_id
    )


@router.patch("/{team_id}", response_model=TeamRead)
async def update_team(
    team_id: str, payload: TeamUpdate, current_user: CurrentUser, session: DbSession
) -> TeamRead:
    team = await TeamService(session).update(
        user_id=current_user.id,
        team_id=team_id,
        data=payload.model_dump(exclude_unset=True),
    )
    await session.commit()
    await session.refresh(team)
    return team
