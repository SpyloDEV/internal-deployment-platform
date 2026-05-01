from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status

from app.api.dependencies import CurrentUser, DbSession
from app.core.security import decode_access_token
from app.schemas.deployment import DeploymentCreate, DeploymentLogRead, DeploymentRead
from app.services.deployment_service import DeploymentService

router = APIRouter(tags=["Deployments"])


@router.post(
    "/environments/{environment_id}/deployments",
    response_model=DeploymentRead,
    status_code=status.HTTP_201_CREATED,
)
async def trigger_deployment(
    environment_id: str,
    payload: DeploymentCreate,
    current_user: CurrentUser,
    session: DbSession,
) -> DeploymentRead:
    deployment = await DeploymentService(session).trigger(
        environment_id=environment_id,
        user_id=current_user.id,
        data=payload.model_dump(),
    )
    await session.commit()
    await session.refresh(deployment)
    return deployment


@router.get("/deployments", response_model=list[DeploymentRead])
async def list_deployments(
    current_user: CurrentUser,
    session: DbSession,
    service_id: str | None = Query(default=None),
    environment_id: str | None = Query(default=None),
) -> list[DeploymentRead]:
    return await DeploymentService(session).list(
        user_id=current_user.id, service_id=service_id, environment_id=environment_id
    )


@router.get("/deployments/{deployment_id}", response_model=DeploymentRead)
async def get_deployment(
    deployment_id: str, current_user: CurrentUser, session: DbSession
) -> DeploymentRead:
    return await DeploymentService(session).get(
        deployment_id=deployment_id, user_id=current_user.id
    )


@router.post("/deployments/{deployment_id}/cancel", response_model=DeploymentRead)
async def cancel_deployment(
    deployment_id: str, current_user: CurrentUser, session: DbSession
) -> DeploymentRead:
    deployment = await DeploymentService(session).cancel(
        deployment_id=deployment_id, user_id=current_user.id
    )
    await session.commit()
    await session.refresh(deployment)
    return deployment


@router.post("/deployments/{deployment_id}/rollback", response_model=DeploymentRead)
async def rollback_deployment(
    deployment_id: str, current_user: CurrentUser, session: DbSession
) -> DeploymentRead:
    deployment = await DeploymentService(session).rollback(
        deployment_id=deployment_id, user_id=current_user.id
    )
    await session.commit()
    await session.refresh(deployment)
    return deployment


@router.get("/deployments/{deployment_id}/logs", response_model=list[DeploymentLogRead])
async def deployment_logs(
    deployment_id: str, current_user: CurrentUser, session: DbSession
) -> list[DeploymentLogRead]:
    return await DeploymentService(session).logs(
        deployment_id=deployment_id, user_id=current_user.id
    )


@router.websocket("/ws/deployments/{deployment_id}/logs")
async def websocket_deployment_logs(
    websocket: WebSocket, deployment_id: str, token: str | None = Query(default=None)
) -> None:
    user_id = decode_access_token(token or "")
    if user_id is None:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    try:
        await websocket.send_json(
            {
                "deployment_id": deployment_id,
                "event": "connected",
                "message": "Live deployment log stream is ready.",
            }
        )
    except WebSocketDisconnect:
        return
    await websocket.close()
