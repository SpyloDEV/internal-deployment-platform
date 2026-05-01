from fastapi import APIRouter

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.health import HealthCheckRead, HealthCheckRequest
from app.services.health_service import HealthService

router = APIRouter(tags=["Health"])


@router.post(
    "/environments/{environment_id}/health-check", response_model=HealthCheckRead
)
async def run_health_check(
    environment_id: str,
    current_user: CurrentUser,
    session: DbSession,
    payload: HealthCheckRequest | None = None,
) -> HealthCheckRead:
    check = await HealthService(session).run_check(
        environment_id=environment_id,
        user_id=current_user.id,
        data=(payload or HealthCheckRequest()).model_dump(),
    )
    await session.commit()
    await session.refresh(check)
    return check


@router.get(
    "/environments/{environment_id}/health", response_model=HealthCheckRead | None
)
async def get_health(
    environment_id: str, current_user: CurrentUser, session: DbSession
) -> HealthCheckRead | None:
    return await HealthService(session).latest(
        environment_id=environment_id, user_id=current_user.id
    )


@router.get(
    "/environments/{environment_id}/health-history",
    response_model=list[HealthCheckRead],
)
async def health_history(
    environment_id: str, current_user: CurrentUser, session: DbSession
) -> list[HealthCheckRead]:
    return await HealthService(session).history(
        environment_id=environment_id, user_id=current_user.id
    )
