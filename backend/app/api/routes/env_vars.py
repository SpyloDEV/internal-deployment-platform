from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DbSession
from app.schemas.common import Message
from app.schemas.env_var import EnvVarCreate, EnvVarRead, EnvVarUpdate
from app.services.env_var_service import EnvVarService

router = APIRouter(tags=["Environment Variables"])


@router.post(
    "/environments/{environment_id}/env-vars",
    response_model=EnvVarRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_env_var(
    environment_id: str,
    payload: EnvVarCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> EnvVarRead:
    env_var = await EnvVarService(session).create(
        environment_id=environment_id,
        user_id=current_user.id,
        data=payload.model_dump(),
    )
    await session.commit()
    await session.refresh(env_var)
    return env_var


@router.get("/environments/{environment_id}/env-vars", response_model=list[EnvVarRead])
async def list_env_vars(
    environment_id: str, current_user: CurrentUser, session: DbSession
) -> list[EnvVarRead]:
    return await EnvVarService(session).list(
        environment_id=environment_id, user_id=current_user.id
    )


@router.patch("/env-vars/{env_var_id}", response_model=EnvVarRead)
async def update_env_var(
    env_var_id: str,
    payload: EnvVarUpdate,
    current_user: CurrentUser,
    session: DbSession,
) -> EnvVarRead:
    env_var = await EnvVarService(session).update(
        env_var_id=env_var_id,
        user_id=current_user.id,
        data=payload.model_dump(exclude_unset=True),
    )
    await session.commit()
    await session.refresh(env_var)
    return env_var


@router.delete("/env-vars/{env_var_id}", response_model=Message)
async def delete_env_var(
    env_var_id: str, current_user: CurrentUser, session: DbSession
) -> Message:
    env_var = await EnvVarService(session).delete(
        env_var_id=env_var_id, user_id=current_user.id
    )
    await session.delete(env_var)
    await session.commit()
    return Message(message="Environment variable removed.")
