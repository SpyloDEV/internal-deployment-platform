from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.environment import (
    EnvironmentCreate,
    EnvironmentRead,
    EnvironmentUpdate,
)
from app.services.environment_service import EnvironmentService

router = APIRouter(tags=["Environments"])


@router.post(
    "/services/{service_id}/environments",
    response_model=EnvironmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_environment(
    service_id: str,
    payload: EnvironmentCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> EnvironmentRead:
    environment = await EnvironmentService(session).create(
        service_id=service_id, user_id=current_user.id, data=payload.model_dump()
    )
    await session.commit()
    await session.refresh(environment)
    return environment


@router.get("/services/{service_id}/environments", response_model=list[EnvironmentRead])
async def list_environments(
    service_id: str, current_user: CurrentUser, session: DbSession
) -> list[EnvironmentRead]:
    return await EnvironmentService(session).list(
        service_id=service_id, user_id=current_user.id
    )


@router.get("/environments/{environment_id}", response_model=EnvironmentRead)
async def get_environment(
    environment_id: str, current_user: CurrentUser, session: DbSession
) -> EnvironmentRead:
    return await EnvironmentService(session).get(
        environment_id=environment_id, user_id=current_user.id
    )


@router.patch("/environments/{environment_id}", response_model=EnvironmentRead)
async def update_environment(
    environment_id: str,
    payload: EnvironmentUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> EnvironmentRead:
    environment = await EnvironmentService(session).update(
        environment_id=environment_id,
        user_id=current_user.id,
        data=payload.model_dump(exclude_unset=True),
    )
    await session.commit()
    await session.refresh(environment)
    return environment
